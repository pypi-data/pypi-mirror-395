"""Climeon API wrapper, used to access the Climeon API from Python.

Authentication credentials will be fetched from environment variables
``API_USER`` and ``API_PASS`` or programmatically at client instantiation or
else through user interaction via Climeon Live Azure B2C.
"""

# pylint: disable=broad-exception-raised

# Standard modules
from datetime import datetime, timedelta, timezone
from getpass import getpass
from hashlib import sha1
from io import StringIO
import lzma
import json
from logging import getLogger, disable, CRITICAL
from os import getenv, path, listdir, remove, makedirs
import pickle
from tempfile import gettempdir
import time
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from pytz import timezone as ZoneInfo

# External modules
import dateparser
import msal
import numpy as np
import pandas as pd
import requests
import tzlocal

# Climeon modules
try:
    from .identifiers import powerblock, module, hp_system
    from .logreader.synonyms import correct_name
    from .plotting import STATE_VARIABLES
except ImportError:
    # Expected import error during autosummary documentation import
    from identifiers import powerblock, module, hp_system
    from logreader.synonyms import correct_name
    from plotting import STATE_VARIABLES

# Check for parquet support
try:
    pd.io.parquet.get_engine("auto")
    PARQUET_SUPPORT = True
except ImportError:
    PARQUET_SUPPORT = False

# Silent Pandas future warnings
try:
    pd.set_option("future.no_silent_downcasting", True)
    pd.options.mode.chained_assignment = None
except Exception: # pylint: disable=broad-exception-caught
    # Older pandas version, nothing to silence
    pass

# API details
PROD_URL = "https://api.climeonlive.com/api/v1"
DEV_URL = "https://climeonliveapi-staging.azurewebsites.net/api/v1"
LOCAL_URL = "http://localhost:44358/api/v1"

# MSAL settings
CLIENT_ID = "fe8152ab-d22c-4f61-9a24-17bb397bee75"
AUTHORITY = "https://climeonlive.b2clogin.com/climeonlive.onmicrosoft.com/"
POLICY_ROPC = "B2C_1_ropc"
POLICY_SIGN_IN = "B2C_1_SignIn"
AUTHORITY_SIGN_IN = AUTHORITY + POLICY_SIGN_IN
AUTHORITY_ROPC = AUTHORITY + POLICY_ROPC
MSAL_SCOPE = ["https://climeonlive.onmicrosoft.com/backend/read"]

# Offline cache settings
BASE_FOLDER = getenv("APPDATA", gettempdir())
OFFLINE_FOLDER = path.join(BASE_FOLDER, "ClimeonLive")
OFFLINE_NAME = "%s_%s_%s_%s_%s"
OFFLINE_TOKEN = path.join(OFFLINE_FOLDER, "token.pickle")
FOLDER_SIZE_LIMIT = 2*1024*1024*1024

# Analytics max interval default settings
MAX_RESULTS = 10000
MAX_ERROR = MAX_RESULTS * 100
SQL_INTERVALS = {
    "PT100MS": 0.1,
    "PT1S": 1,
    "PT10S": 10,
    "PT1M": 60,
    "PT10M": 600,
    "PT1H": 3600,
    "PT12H": 43200,
    "PT24H": 86400
}

AGGREGATION_METHODS = ["first", "avg", "min", "max"]

AUTH_FAIL = "AuthenticationFailed"

# Global client
CLIENT = None # pylint: disable=invalid-name

class Client():
    """Climeon API client.

        Parameters:
            user (str): User mail to login with. If not supplied it will
                        be fetched from environment variable ``API_USER``, if
                        not set the user will be prompted via Azure B2C.
            passwd (str): User password. If not supplied it will be
                          fetched from environment variable ``API_PASS``,
                          if not set the user will be prompted via Azure B2C.
            prod (bool): Boolean indicating if the production or development
                         API should be used. Defaults to ``True``.
            plotly (bool): Boolean indicating if plotting library should be
                           set to plotly. Defaults to ``True``.
    """
    # pylint: disable=too-many-public-methods

    def __init__(self, user=None, passwd=None, prod=True, plotly=True):
        self.logger = getLogger(__name__)
        self.user = user or getenv("API_USER")
        self.passwd = passwd or getenv("API_PASS")
        self.url = PROD_URL if prod else DEV_URL
        self.session = requests.Session()
        ropc = self.user and self.passwd
        authority = AUTHORITY_ROPC if ropc else AUTHORITY_SIGN_IN
        self.app = msal.PublicClientApplication(CLIENT_ID,
                                                authority=authority,
                                                validate_authority=False)
        if plotly:
            pd.options.plotting.backend = "plotly"
        token_expire = time.time() - 60*60*3
        if not path.exists(OFFLINE_FOLDER):
            makedirs(OFFLINE_FOLDER)
        if path.exists(OFFLINE_TOKEN) and path.getmtime(OFFLINE_TOKEN) > token_expire:
            with open(OFFLINE_TOKEN, "rb") as token_file:
                token = pickle.load(token_file)
            auth = "Bearer %s" % token
            self.headers = {"authorization": auth}
        else:
            self.login()

    def login(self):
        """Logs in the user to Climeon API."""
        result = None
        if self.user and self.passwd:
            result = self._login_password()
        else:
            result = self._login_silent()
        if not result:
            result = self._login_interactive()
        if "error" in result:
            raise Exception(result["error_description"])
        token = result["access_token"]
        with open(OFFLINE_TOKEN, "wb") as token_file:
            pickle.dump(token, token_file)
        auth = "Bearer %s" % token
        self.headers = {"authorization": auth}

    def _login_password(self):
        self.logger.debug("Logging in with user %s", self.user)
        return self.app.acquire_token_by_username_password(self.user, self.passwd, MSAL_SCOPE)

    def _login_silent(self):
        self.logger.debug("Silent login")
        accounts = self.app.get_accounts()
        account = accounts[0] if accounts else None
        return self.app.acquire_token_silent(MSAL_SCOPE, account=account)

    def _login_interactive(self):
        self.logger.debug("Interactive login")
        try:
            disable(CRITICAL) # Disable logging
            result = self.app.acquire_token_interactive(
                MSAL_SCOPE,
                auth_uri_callback=auth_uri_callback
            )
            disable(0) # Enable logging again
            return result
        except Exception: # pylint: disable=broad-except
            disable(0) # Enable logging again
            return self.fallback_login()

    def fallback_login(self):
        """Fallback in case interactive MSAL login can't be used."""
        self.logger.warning("Falling back on python input")
        self.user = input("Climeon live user email: ")
        self.passwd = getpass("Password: ")
        self.app = msal.PublicClientApplication(CLIENT_ID,
                                                authority=AUTHORITY_ROPC,
                                                validate_authority=False)
        return self._login_password()

    def _http(self, method, endpoint, body, retry):
        headers = self.headers
        if body:
            headers["Content-Type"] = "application/json-patch+json"
            headers["accept"] = "text/plain"
        try:
            res = self.session.request(method, endpoint, headers=headers, data=body)
        except ConnectionError as exception:
            if retry:
                return self._http(method, endpoint, body, False)
            raise exception
        auth_fail = res.text.startswith(AUTH_FAIL) or res.status_code == 401
        if auth_fail and retry:
            self.login()
            return self._http(method, endpoint, body, False)
        if not res.ok:
            raise Exception(res.text)
        return res

    def get(self, endpoint):
        """General purpose GET method."""
        req_url = self.url + endpoint
        return self._http("GET", req_url, None, True)

    def post(self, endpoint, body):
        """General purpose POST method."""
        req_url = self.url + endpoint
        json_body = json.dumps(body)
        return self._http("POST", req_url, json_body, True)


    # Analytics

    def analytics(self, machine_id, date_from, date_to, variables,
                  aggregation=None, interval=None):
        """Get aggregated logfile data from the Analytics database.

        Parameters:
            machine_id (str): Module or powerblock id e.g. "0100000016".
            date_from (str, datetime): Datetime to get data from.
            date_to (str, datetime): Datetime to get data to.
            variables (list): Variables to get.
            aggregation (list, optional): Aggregation methods to use. Can be
                                          any of ``first``, ``avg``, ``min`` or
                                          ``max``, or a list of aggregation
                                          methods, one for each variable.
                                          Defaults to ``avg`` for all variables.
            interval (str, optional): Interval size specified in ISO-8601
                                      duration format:
                                      https://en.wikipedia.org/wiki/ISO_8601
                                      Defaults to a reasonable interval.
                                      Can be any of ``PT100MS``, ``PT1S``,
                                      ``PT10S``, ``PT1M``, ``PT10M``, ``PT1H``,
                                      ``PT12H``, ``PT24H``.

        Returns:
            DataFrame: A Pandas DataFrame.
        """
        # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        date_from, date_to = parse_dates(date_from, date_to)
        interval = parse_interval(date_from, date_to, interval)
        now = datetime.now(date_to.tzinfo)
        last_hour = date_to.replace(year=now.year, month=now.month, day=now.day,
                                    hour=now.hour, minute=0, second=0, microsecond=0)
        # To allow local cache to be updated after hourly logfile has been
        # uploaded, set date_to accordingly.
        date_to = min(date_to, last_hour)
        if interval not in SQL_INTERVALS:
            raise ValueError("Interval must be one of %s" % list(SQL_INTERVALS.keys()))
        var = format_variables(variables, aggregation)
        filename = offline_name(machine_id, date_from, date_to, var, interval)
        dataframe = load_dataframe(filename)
        if not dataframe is None:
            return dataframe
        estimated_result = (date_to - date_from).total_seconds() / SQL_INTERVALS[interval]
        if estimated_result > MAX_ERROR:
            error_text = "Chosen interval %s would request too large of a " \
                         "dataset (%d rows). Increase interval or decrease " \
                         "timerange. Maximum amount of rows to return is %d." \
                         % (interval, int(estimated_result), MAX_ERROR)
            raise ValueError(error_text)
        body = {
            "searchSpan": {
                "from": date_iso_utc(date_from),
                "to": date_iso_utc(date_to)
            },
            "interval": interval,
            "parameters": [{
                "id": machine_id,
                "aggregateVariables": var
            }]
        }
        response = self.post("/Analytics", body)
        raw_data = response.json()
        dataframe = json_to_dataframe(raw_data[machine_id])
        if dataframe.empty:
            return dataframe
        rec_int = raw_data[machine_id]["interval"]
        if interval != rec_int:
            self.logger.info("Requested interval %s could not be fetched, "
                             "got interval %s instead. Use logfile data to "
                             "get higher resolution.", interval, rec_int)
        dataframe = format_dataframe(dataframe, date_from.tzinfo, rec_int)
        save_dataframe(dataframe, filename)
        return dataframe

    def analytics_variables(self, machine_id):
        """Get all available variables for a machine."""
        endpoint = "/Analytics/variables/%s" % machine_id
        response = self.get(endpoint)
        return response.json()

    def telemetry(self, machine_id, date_from, date_to, variables,
                  aggregation=None, interval=None):
        """Get telemetry data from the ADX database.

        Parameters:
            machine_id (str): module or powerblock id e.g. "0100000016".
            date_from (str, datetime): Datetime to get data from.
            date_to (str, datetime): Datetime to get data to.
            variables (list): List of variables to fetch.
            aggregation (list, optional): Aggregation methods to use. Can be
                                          any of ``first``, ``avg``, ``min``, ``max``
                                          or a list of aggregation methods, one
                                          each variable. Defaults to ``avg`` for
                                          all variables.
            interval (str, optional): Interval size specified in ISO-8601
                                      duration format:
                                      https://en.wikipedia.org/wiki/ISO_8601
                                      Defaults to a reasonable interval.
                                      Can be any of ``PT1M``, ``PT10M``, ``PT1H``,
                                      ``PT12H``, ``PT24H``
        Returns:
            DataFrame: A Pandas DataFrame.
        """
        #pylint: disable=too-many-arguments,too-many-positional-arguments
        date_from, date_to = parse_dates(date_from, date_to)
        var = format_variables(variables, aggregation)
        interval = parse_interval(date_from, date_to, interval)
        aggregation = aggregation or "avg"
        body = {
            "id": [
                machine_id
            ],
            "searchSpan": {
                "from": date_iso_utc(date_from),
                "to": date_iso_utc(date_to)
            },
            "variables": var,
            "interval": interval
        }
        response = self.post("/Analytics/adx/query", body)
        raw_data = response.json()
        if "error" in raw_data:
            raise Exception(raw_data["error"]["message"])
        dataframe = json_to_dataframe(raw_data[machine_id])
        dataframe = format_dataframe(dataframe, date_from.tzinfo, interval, False)
        return dataframe


    # Config

    def config_query(self, query):
        """Get config history for a specific module/powerblock or config name."""
        endpoint = "/Config/%s" % query
        response = self.get(endpoint)
        return convert_timestamps(response.json())

    def config_changes(self):
        """Get config changes for specified machine."""
        response = self.get("/Config/changes")
        return convert_timestamps(response.json())

    def config_info(self):
        """Get config information."""
        response = self.get("/Config/info")
        return response.json()


    # Modules

    def modules(self):
        """Get info for all registered modules."""
        response = self.get("/Modules")
        return response.json()

    def module_info(self, module_id):
        """Get info for a specific module."""
        endpoint = "/Modules/%s" % module_id
        response = self.get(endpoint)
        return response.json()

    def modules_telemetry(self):
        """Get all modules latest telemetry."""
        response = self.get("/Modules/telemetry")
        return convert_timestamps(response.json())

    def module_telemetry(self, module_id):
        """Get latest module telemetry for a specific module."""
        endpoint = "/Modules/%s/telemetry/" % module_id
        response = self.get(endpoint)
        return convert_timestamps([response.json()])[0]

    def module_alerts(self, module_id):
        """Get current alerts for a specific module."""
        endpoint = "/Modules/%s/alerts/" % module_id
        response = self.get(endpoint)
        return convert_timestamps(response.json())

    def module_alert_history(self, module_id):
        """Get alert history for a specific module."""
        endpoint = "/Modules/%s/alertHistory/" % module_id
        response = self.get(endpoint)
        return convert_timestamps(response.json())

    def list_blackbox(self, module_id, date):
        """List all blackbox timestamps for a date."""
        date = parse_datetime(date)
        date_str = date.strftime("%y%m%d")
        endpoint = "/Modules/%s/data/blackbox/%s" % (module_id, date_str)
        try:
            response = self.get(endpoint)
        except Exception: # pylint: disable=broad-except
            return []
        t_s = response.json()
        d_t = datetime(date.year, date.month, date.day, tzinfo=date.tzinfo)
        return [d_t + timedelta(hours=int(t[0:2]), minutes=int(t[2:])) for t in t_s]

    def blackbox(self, module_id, date_from, date_to=None, variables=None):
        """Get blackbox file for a timestamp or a date range."""
        date_from, date_to = parse_dates(date_from, date_to)
        date_range = pd.date_range(date_from, date_to, freq="d").tolist()
        dataframe = pd.DataFrame()
        for date in date_range:
            for dt in self.list_blackbox(module_id, date):
                endpoint = "/Modules/%s/data/blackbox/%s/%s" % \
                    (module_id, dt.strftime("%y%m%d"), dt.strftime("%H%M"))
                response = self.get(endpoint)
                data_str = response.text
                header_idx = data_str.index("Timestamp")
                df = pd.read_csv(StringIO(data_str[header_idx:]))
                df = format_dataframe(df, date_from.tzinfo, "PT100MS")
                df = df.resample("100ms").aggregate("first")
                dataframe = pd.concat([dataframe, df])
        if dataframe.empty:
            return dataframe
        if variables:
            dataframe = dataframe[variables]
        return dataframe[date_from:date_to]


    # PowerBlocks

    def powerblocks(self):
        """Get info for all registered powerblocks."""
        response = self.get("/PowerBlocks")
        return response.json()

    def powerblock_info(self, powerblock_id):
        """Get info for a specific powerblock."""
        endpoint = "/PowerBlocks/%s" % powerblock_id
        response = self.get(endpoint)
        return response.json()

    def powerblock_alerts(self, powerblock_id):
        """Get current alerts for a specific powerblock."""
        endpoint = "/PowerBlocks/%s/alerts/" % powerblock_id
        response = self.get(endpoint)
        return convert_timestamps(response.json())

    def powerblock_alert_history(self, powerblock_id):
        """Get alert history for a specific powerblock."""
        endpoint = "/PowerBlocks/%s/alertHistory/" % powerblock_id
        response = self.get(endpoint)
        return convert_timestamps(response.json())

    def powerblock_parameters(self, powerblock_id, date):
        """Get parameter file for a specific powerblock and date."""
        date_str = date.strftime("%y%m%d")
        endpoint = "/PowerBlocks/%s/parameters/%s" % (powerblock_id, date_str)
        response = self.get(endpoint)
        return response.text


    # Users

    def users(self):
        """Get info for all registered users."""
        response = self.get("/Users")
        return response.json()


    # SecurityGroups

    def security_groups(self):
        """Get info for all registered security groups."""
        response = self.get("/SecurityGroups")
        return response.json()


    # Other

    def alert_info(self):
        """Get info for all alerts."""
        response = self.get("/Other/alertinfo")
        return response.json()


    # Helpers

    def logfile_raw(self, machine_id, date):
        """Retrieves log file for a specific module and date."""
        date_str = date.strftime("%y%m%d")
        if module(machine_id):
            endpoint = "/Modules/%s" % machine_id
        elif powerblock(machine_id):
            endpoint = "/PowerBlocks/%s" % machine_id
        elif machine_id == "0900000001":
            endpoint = "/Other/backbone"
        elif hp_system(machine_id):
            endpoint = "/HPSystems/%s" % machine_id
        else:
            error = "Bad id supplied %s" % machine_id
            raise ValueError(error)
        endpoint = endpoint + "/data/%s?unpack=False" % date_str
        response = self.get(endpoint)
        try:
            return lzma.decompress(response.content).decode("utf-8")
        except lzma.LZMAError:
            return response.text

    def download_logfile(self, machine_id, date, directory="."):
        """Download a logfile to disk."""
        date_str = date.strftime("%y%m%d")
        log_file = self.logfile_raw(machine_id, date)
        log_path = "%s/%s_%s.csv" % (directory, machine_id, date_str)
        with open(log_path, mode="w+", encoding="utf-8") as file_stream:
            file_stream.write(log_file)
        return log_path

    def logfile(self, machine_id, date_from, date_to=None, variables=None):
        """Get logfile for a machine/date.

        Parameters:
            machine_id (str): module or powerblock id e.g. "0100000016".
            date_from (str, datetime): Datetime to get data from.
            date_to (str, datetime, optional): Datetime to get data to.
            variables (list, optional): List of strings with variable names.
                                        Defaults to all available variables.
                                        Any other variables will be dropped.

        Returns:
            DataFrame: A Pandas DataFrame.
        """
        date_from, date_to = parse_dates(date_from, date_to)
        var = format_variables(variables, "avg") if variables else None
        filename = offline_name(machine_id, date_from.date(), date_to.date(), var, "")
        dataframe = load_dataframe(filename)
        if not dataframe is None:
            return dataframe
        # Make sure potential part days are included in date list
        diff = (date_to + timedelta(days=1, seconds=-1)).date() - date_from.date()
        date_list = [date_from + timedelta(days=d) for d in range(diff.days)]
        dataframe = pd.concat([self.logfile_cached(machine_id, d) for d in date_list])
        if dataframe.empty:
            return None
        dataframe = dataframe[~dataframe.index.duplicated(keep="last")]
        if variables:
            dataframe = dataframe[variables]
        freq = parse_freq(dataframe)
        if freq:
            dataframe = dataframe.asfreq(freq)
        save_dataframe(dataframe, filename)
        return dataframe

    def logfile_cached(self, machine_id, date):
        """Fetch and cache a single logfile"""
        filename = offline_name(machine_id, date, date, "", "PT1S")
        dataframe = load_dataframe(filename)
        if not dataframe is None:
            return dataframe
        try:
            data_str = self.logfile_raw(machine_id, date)
        except Exception: # pylint: disable=broad-except
            return pd.DataFrame()
        if "Timestamp" not in data_str:
            return pd.DataFrame()
        header_idx = data_str.index("Timestamp")
        dataframe = pd.read_csv(StringIO(data_str[header_idx:]))
        dataframe = format_dataframe(dataframe, date.tzinfo, "PT1S")
        freq = parse_freq(dataframe)
        if freq:
            return dataframe.asfreq(freq)
        save_dataframe(dataframe, filename)
        return dataframe

    def get_machines(self):
        """Get all registered modules/powerblocks."""
        powerblocks = self.powerblocks()
        machines = [m["moduleId"] for p in powerblocks for m in p["modules"]]
        machines.extend([p["powerBlockId"] for p in powerblocks])
        machines.sort()
        return machines

def offline_name(machine_id, date_from, date_to, variables, interval):
    """Get offline name for log data."""
    if variables:
        var = "".join(sorted([v["name"] + v["aggregation"] for v in variables]))
    else:
        var = ""
    name_raw = OFFLINE_NAME % (machine_id, date_from, date_to, var, interval)
    filename = sha1(bytes(name_raw, "utf-8")).hexdigest()
    return path.join(OFFLINE_FOLDER, filename)

def save_dataframe(dataframe, filename):
    """Save dataframe to disk. Tries both parquet and pickle."""
    files = [path.join(OFFLINE_FOLDER, f) for f in listdir(OFFLINE_FOLDER)]
    folder_size = sum(path.getsize(f) for f in files if path.isfile(f))
    if folder_size > FOLDER_SIZE_LIMIT:
        oldest_file = min(files, key=path.getctime)
        remove(oldest_file)
    if PARQUET_SUPPORT:
        dataframe.to_parquet(filename + ".parquet")
    else:
        dataframe.to_pickle(filename + ".pickle")

def load_dataframe(filename):
    """Load a dataframe from disk. Tries both parquet and pickle."""
    if path.exists(filename + ".parquet") and PARQUET_SUPPORT:
        dataframe = pd.read_parquet(filename + ".parquet")
    elif path.exists(filename + ".pickle"):
        dataframe = pd.read_pickle(filename + ".pickle")
    else:
        return None
    freq = parse_freq(dataframe)
    if freq:
        return dataframe.asfreq(freq)
    return dataframe

def parse_datetime(date_str):
    """Parse a datetime string."""
    date = None
    if date_str is None:
        return date_str
    if isinstance(date_str, str):
        date = dateparser.parse(date_str)
    if date is None:
        date = pd.to_datetime(date_str).to_pydatetime()
    if date.tzinfo is None:
        # Timezone naive, use locale
        date = date.astimezone(tzlocal.get_localzone())
    if isinstance(date_str, str) and "day" in date_str:
        # Ensure that strings like "today" returns a somewhat reproducible
        # datetime. Otherwise caching becomes futile.
        date = datetime(date.year, date.month, date.day, tzinfo=date.tzinfo)
    return date

def format_variables(variables, aggregation):
    """Format a list of variables and aggregation to Analytics/ADX format"""
    if isinstance(aggregation, str):
        aggregation = [aggregation] * len(variables)
    default = ["first" if v in STATE_VARIABLES else "avg" for v in variables]
    aggregation = aggregation or default
    if len(aggregation) != len(variables):
        error_text = "Aggregation specification does not match amount of " \
                     "variables. (%d aggregation values, %d variables)" \
                     % (len(aggregation), len(variables))
        raise ValueError(error_text)
    if not all(a in AGGREGATION_METHODS for a in aggregation):
        raise ValueError("Aggregation methods must be one of %s" % AGGREGATION_METHODS)
    var = [{"name": v, "aggregation": a} for v, a in zip(variables, aggregation)]
    return var

def date_iso_utc(date):
    """Convert date to timezone aware, UTC, ISO formatted string."""
    return date.astimezone(timezone.utc).isoformat()

def json_to_dataframe(raw_data):
    """Convert raw json data to a dataframe."""
    names = [p["name"] for p in raw_data["properties"]]
    columns = [
        p["name"] if names.count(p["name"]) < 2 else p["name"] + "_" + p["aggregation"]
        for p in raw_data["properties"]
    ]
    columns.insert(0, "Timestamp")
    data = [p["values"] for p in raw_data["properties"]]
    data.insert(0, raw_data["timestamps"])
    data = list(map(list, zip(*data)))
    dataframe = pd.DataFrame(data, columns=columns)
    return dataframe

def format_dataframe(dataframe, original_tz, interval, correct_names=True):
    """Clean up and properly timestamp dataframe."""
    # pylint: disable=too-many-locals
    dataframe = dataframe[dataframe.columns[~dataframe.columns.str.contains("^Unnamed")]]
    dataframe = dataframe.fillna(np.nan).infer_objects(copy=False)
    dataframe = dataframe.replace(-32768, np.nan).infer_objects(copy=False)
    dataframe = dataframe.replace(np.inf, np.nan).infer_objects(copy=False)
    dataframe = dataframe.replace(-np.inf, np.nan).infer_objects(copy=False)
    correct_mapper = {c: correct_name(c) for c in dataframe.columns}
    if correct_names:
        dataframe.rename(columns=correct_mapper, inplace=True)
    dup_mapper = {c.lower(): c for c in reversed(dataframe.columns)}
    dup_mapper = {c: dup_mapper[c.lower()] for c in dataframe.columns}
    dataframe.rename(columns=dup_mapper, inplace=True)
    dup_col = dataframe.columns.duplicated()
    if any(dup_col):
        dup_idx = [i for i, d in enumerate(dup_col) if d]
        ndup_idx = [i for i, d in enumerate(dup_col) if not d]
        df_dup = dataframe.iloc[:, dup_idx]
        df_ndup = dataframe.iloc[:, ndup_idx]
        dataframe = df_ndup.combine_first(df_dup)
    ts_1 = parse_datetime(dataframe["Timestamp"][0])
    ts_2 = parse_datetime(dataframe["Timestamp"][1]) if len(dataframe.index) > 1 else None
    ts_utc = "Timestamp UTC [-]" if "Timestamp UTC [-]" in dataframe else "Timestamp UTC"
    if ts_2 and ts_2 - ts_1 < timedelta(seconds=0.5) and ts_utc in dataframe:
        # Blackbox file, need to use Timestamp column to maintain resolution
        t_z = timezone.utc
        utc_1 = parse_datetime(dataframe[ts_utc][0])
        utc_offset = utc_1 - ts_1
        dataframe["Timestamp"] = pd.to_datetime(dataframe["Timestamp"], errors="coerce")
        dataframe["Timestamp"] = dataframe["Timestamp"] + utc_offset
    elif ts_utc in dataframe:
        t_z = timezone.utc
        dataframe["Timestamp"] = pd.to_datetime(dataframe[ts_utc], utc=True, errors="coerce")
    else:
        t_z = ZoneInfo("Europe/Stockholm")
        dataframe["Timestamp"] = pd.to_datetime(dataframe["Timestamp"], errors="coerce")
    dataframe = dataframe.set_index("Timestamp")
    dataframe = dataframe.loc[pd.notnull(dataframe.index)]
    if dataframe.index.tz is None:
        dataframe.index = dataframe.index.tz_localize(t_z)
    dataframe.index = dataframe.index.tz_convert(original_tz)
    if interval != "PT100MS":
        # Add missing timestamps as NaN
        pd_interval = pandas_interval(interval)
        dataframe = dataframe.resample(pd_interval).first()
    # Remove duplicate timestamps
    dataframe = dataframe[~dataframe.index.duplicated(keep="last")]
    freq = parse_freq(dataframe)
    if freq:
        dataframe = dataframe.asfreq(freq)
    return dataframe

def parse_freq(df):
    """Parse frequency of a dataframe index."""
    if df.empty:
        return None
    if df.index.freq is not None:
        return df.index.freq
    if len(df.index) < 2:
        return None
    if len(df.index) == 2:
        freq = _infer_freq(df.index)
    else:
        freq = pd.infer_freq(df.index) or _infer_freq(df.index)
    if freq == pd.Timedelta("100ms"):
        return None
    return freq

def _infer_freq(index):
    return pd.to_timedelta(np.median(np.diff(index))).round("100ms")

def parse_dates(date_from, date_to):
    """Parse and sanity check datetime range."""
    date_from = parse_datetime(date_from)
    date_to = parse_datetime(date_to) if date_to else date_from + timedelta(days=1)
    if not date_from < date_to:
        raise ValueError("Start date must be earlier than end date.")
    return date_from, date_to

def parse_interval(date_from, date_to, interval=None, max_results=MAX_RESULTS):
    """Figure out a reasonable interval for a time range."""
    if interval and interval != "highres":
        return interval
    diff = (date_to - date_from).total_seconds()
    for sql_interval, seconds in SQL_INTERVALS.items():
        result = diff / seconds
        if result < max_results:
            return sql_interval
    raise ValueError("Could not find a valid interval for this range.")

def pandas_interval(interval):
    """Translate from ISO-8601 interval to pandas interval."""
    if interval == "PT100MS":
        return "100ms"
    return interval[2:].replace("M", "min").lower()

def convert_timestamps(raw_list):
    """Replaces all str timestamp with datetime timestamp."""
    for entry in raw_list:
        if entry["timestamp"] == "0001-01-01T00:00:00":
            entry["timestamp"] = datetime(1, 1, 1, tzinfo=timezone.utc)
        else:
            entry["timestamp"] = pd.to_datetime(entry["timestamp"]).to_pydatetime()
    return raw_list

def auth_uri_callback(_):
    """Called if interactive login fails."""
    raise Exception("Could not launch browser")

def global_client():
    """Returns a global reusable API client to simplify API function calls"""
    global CLIENT # pylint: disable=global-statement
    if CLIENT is None:
        CLIENT = Client()
    return CLIENT

def analytics(machine_id, date_from, date_to, variables, aggregation=None,
              interval=None):
    """Get aggregated logfile data from the Analytics database.

    Parameters:
        machine_id (str): Module or powerblock id e.g. "0100000016".
        date_from (str, datetime): Datetime to get data from.
        date_to (str, datetime): Datetime to get data to.
        variables (list): Variables to get.
        aggregation (list, optional): Aggregation methods to use. Can be
                                      any of ``first``, ``avg``, ``min`` or
                                      ``max``, or a list of aggregation
                                      methods, one for each variable.
                                      Defaults to ``avg`` for all variables.
        interval (str, optional): Interval size specified in ISO-8601
                                  duration format:
                                  https://en.wikipedia.org/wiki/ISO_8601
                                  Defaults to a reasonable interval.
                                  Can be any of ``PT100MS``, ``PT1S``,
                                  ``PT10S``, ``PT1M``, ``PT10M``, ``PT1H``,
                                  ``PT12H``, ``PT24H``.

    Returns:
        DataFrame: A Pandas DataFrame.
    """
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    return global_client().analytics(machine_id, date_from, date_to, variables,
                                     aggregation, interval)

def logfile(machine_id, date_from, date_to=None, variables=None):
    """Get logfile for a machine/date.

    Parameters:
        machine_id (str): module or powerblock id e.g. "0100000016".
        date_from (str, datetime): Datetime to get data from.
        date_to (str, datetime, optional): Datetime to get data to.
        variables (list, optional): List of strings with variable names.
                                    Defaults to all available variables.
                                    Any other variables will be dropped.
                                    Useful if a long timerange is used to
                                    not exhaust memory.

    Returns:
        DataFrame: A Pandas DataFrame.
    """
    return global_client().logfile(machine_id, date_from, date_to, variables)

def blackbox(machine_id, date_from, date_to=None, variables=None):
    """Get all blackbox data for a machine and date range.

    Parameters:
        machine_id (str): module or powerblock id e.g. "0100000016".
        date_from (str, datetime): Datetime to get data from.
        date_to (str, datetime, optional): Datetime to get data to.
        variables (list, optional): List of strings with variable names.
                                    Defaults to all available variables.

    Returns:
        DataFrame: A Pandas DataFrame.
    """
    return global_client().blackbox(machine_id, date_from, date_to, variables)
