from dataclasses import asdict
from typing import TypeVar
from marshmallow_objects import models
from typing import Any, Dict, List, Optional, Union

from zpy.logger import zL
from zpy.utils.funcs import safely_exec, safely_exec_with
from zdb.commons import process_exception
from enum import Enum
import cx_Oracle
import logging


def _instantiate_model(model, data: dict) -> Any:
    """
    Helper function to instantiate a model with data, handling both regular classes
    and marshmallow_objects models with compatibility for marshmallow 3.x and 4.x
    """
    try:
        # Try direct instantiation first (works for most cases)
        return model(**data)
    except TypeError as e:
        # If it fails due to 'context' or similar marshmallow issues,
        # try alternative approaches for marshmallow_objects compatibility
        if "context" in str(e) or "unexpected keyword argument" in str(e):
            try:
                # For marshmallow_objects with marshmallow 4.x:
                # Create schema instance directly without context
                if hasattr(model, '__schema_class__'):
                    # This is a marshmallow_objects Model
                    schema_class = model.__schema_class__
                    schema_instance = schema_class()
                    loaded_data = schema_instance.load(data)
                    # Create instance with loaded data
                    instance = object.__new__(model)
                    for key, value in loaded_data.items():
                        setattr(instance, key, value)
                    return instance
                # Fallback to load if available
                elif hasattr(model, 'load'):
                    return model.load(data)
            except Exception:
                pass
        raise e

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"

from zdb.commons import ZDatabase, ZDBConfig, ZDBPool, show_info, parser_types
from zdb.utils import get_current_schema

T = TypeVar("T")


class OracleType(Enum):
    cursor = cx_Oracle.CURSOR
    number = cx_Oracle.NUMBER
    string = cx_Oracle.STRING
    integer = cx_Oracle.NUMBER
    decimal = cx_Oracle.NUMBER
    bool = cx_Oracle.BOOLEAN


class OracleParam(Enum):
    LIST_INTEGER = "LIST_INTEGER"
    LIST_STR = "LIST_VARCHAR"
    LIST_CLOB = "LIST_CLOB"


class ZParam:
    def __init__(
            self,
            value: Union[List[int], List[float], List[str], List[Any]],
            param_type: OracleParam,
            key: str,
            origin: str = None,
    ) -> None:
        self.value = value
        self.param_type = param_type
        self.key = key
        self.origin = origin


class IntList(ZParam):
    def __init__(self, value: List[int], key: str, origin: str = None) -> None:
        super().__init__(value, OracleParam.LIST_INTEGER, key, origin)


class StrList(ZParam):
    def __init__(self, value: List[str], key: str, origin: str = None) -> None:
        super().__init__(value, OracleParam.LIST_STR, key, origin)


class ClobList(ZParam):
    def __init__(self, value: List[Any], key: str, origin: str) -> None:
        super().__init__(value, OracleParam.LIST_CLOB, key, origin)


def get_str_connection(config: dict = None, mode="TSN") -> Union[dict, str]:
    if config is None:
        raise Exception("The data for the connection was not provided")
    server = config["host"]
    port = config["port"]
    service = config["service"]
    user = config["user"]
    password = config["password"]
    if mode == "DSN":
        return "{0}:{1}/{2}".format(server, port, service)
    return "{0}/{1}@{2}:{3}/{4}".format(user, password, server, port, service)


def extract_of_result_data(
        result_set, ret_type: OracleType, model=None, jsonfy=False
):
    """
    New version of result set processor
    """
    if ret_type == OracleType.cursor:
        columns = [field[0] for field in result_set.description]
        if model is not None:
            return [_instantiate_model(model, dict(zip(columns, r))) for r in result_set]
        if jsonfy is True:
            return [dict(zip(columns, row)) for row in result_set]
        return result_set.fetchall()
    elif OracleType.number:
        return safely_exec_with(lambda x: float(result_set), result_set, args=[result_set])
    elif OracleType.integer:
        return safely_exec_with(lambda x: int(result_set), result_set, args=[result_set])
    elif OracleType.decimal:
        return safely_exec_with(lambda x: parser_types[4](x), result_set, args=[result_set])
    else:
        return parser_types[2](result_set)


def make_custom_param(
        connection: Any,
        param_type: OracleParam,
        value: Union[List[int], List[float], List[str], List[Any]],
        schema: str = None,
):
    """
    Make custom param
    """
    db_schema = (
        "" if (schema is None or schema.replace(" ", "") == "") else f"{schema}."
    )
    list_type = connection.gettype(f"{db_schema}{param_type.value}")
    return list_type.newobject(value)


class ZOracle(ZDatabase):
    __local_client_initialized: bool = False
    __local_client_path: str = None
    __config_connection: dict = None
    __connection = None
    __is_connected: bool = False

    __schemas: List[Dict] = None
    __env: str = None
    __verbose: bool = False

    def __init__(
            self,
            config: dict = None,
            local_client_path: str = None,
            schemas: List[Dict] = None,
            env: str = None,
            verbose: bool = False,
    ) -> None:
        self.__local_client_path = local_client_path
        self.__config_connection = config
        self.__schemas = schemas
        self.__env = env
        self.__verbose = verbose

    @classmethod
    def setup(cls, config: dict,
              local_client_path: str = None,
              schemas: List[Dict] = None,
              env: str = None,
              verbose: bool = False):
        return cls(config, local_client_path, schemas, env, verbose)

    @classmethod
    def setup_of(cls, config: ZDBConfig, local_client_path: str = None,
                 schemas: List[Dict] = None,
                 env: str = None,
                 verbose: bool = False, ):
        return cls(asdict(config), local_client_path, schemas, env, verbose)

    @classmethod
    def from_of(cls, user: str, password: str, host: str, db_name: str, verbose: bool = False):
        raise NotImplementedError("Not implemented for Oracle!")

    def new_connect(self) -> Any:
        str_connection = self.__validate_config(self.__config_connection)
        return cx_Oracle.connect(str_connection)

    def init_local_client(self, path: str = None):
        if self.__local_client_initialized:
            return
        value = path if self.__local_client_path is None else self.__local_client_path
        try:
            if value is None:
                raise Exception("Local client path not provided.")
            cx_Oracle.init_oracle_client(lib_dir=value)
            self.__local_client_initialized = True
        except Exception as e:
            self.__local_client_initialized = False
            logging.exception(e)

    def __validate_config(self, config: dict = None, mode="TSN") -> Union[dict, str]:
        values = (
            config if self.__config_connection is None else self.__config_connection
        )
        return get_str_connection(values, mode)

    def connect(self, config: dict = None):
        """
        Start oracle connection
        """
        if self.__is_connected:
            return True
        try:
            str_connection = self.__validate_config(config)
            self.__connection = cx_Oracle.connect(str_connection)
            self.__is_connected = True
            return True
        except Exception as e:
            raise e

    def close(self):
        if self.__is_connected:
            self.__connection.close()
            self.__is_connected = False

    def is_connected(self) -> bool:
        return self.__is_connected

    def get_connection(self):
        return self.__connection

    def call(
            self,
            fn: str,
            ret_type: OracleType,
            params: Optional[Dict] = None,
            custom_params: Optional[List[ZParam]] = None,
            model: Optional[models.Model] = None,
            connection=None,
            jsonfy=False,
            throw=False
    ) -> Optional[Any]:
        """
        Execute or call oracle functions - FN v0.0.1 | Core v0.0.7

        New feature for call oracle db functions
        Use this function instead function 'call'

        Parameters
        ----------
        fn : str | required
            Function name with package name: PO_LINES_PKG.FN_GET_LINE

        ret_type : OracleType | required
            The return type of oracle db function

        params : Dict | Optional
            Set parameter that the oracle funtion expects

        custom_params : Optional[List[ZParam, IntList, StrList, ClobList]] | Optional
            Custom Set parameter that the oracle funtion expects, see avaialble custom types

        model : marshmallow_objects.models.Model | Optional
            Model specification where the db data will be volcated

        connection : DB Connection | Optional
            The db connection object, if it is not passed by params, it tries to get a global instance

        jsonfy : bool | Optional
            Return data in dict format

        throw : bool | Optional
            raise exception or not
        Raises
        ------
        NotValueProvided
            Connection

        Returns
        -------
        result set : Union[List[Model],int,float,str]
            The result set of oracle db function
        """
        cursor = None
        connection_provided = True
        db_schema = None

        if connection is not None:
            cursor = connection.cursor()
        else:
            connection_provided = False
            connection = self.new_connect()
            cursor = connection.cursor()
        if connection is None:
            raise Exception("Can't get db connection")

        if self.__schemas is not None:
            db_schema = get_current_schema(self.__schemas, self.__env, self.__env)

        if custom_params is not None and len(custom_params) > 0:
            if params is None:
                params = {}
            # * Find the current env for extract the schema
            for custom in custom_params:
                params[custom.key] = make_custom_param(
                    connection,
                    param_type=custom.param_type,
                    value=custom.value,
                    schema=db_schema,
                )

        fn = (
            fn
            if db_schema is None or db_schema.replace(" ", "") == ""
            else f"{db_schema}.{fn}"
        )
        if self.__verbose:
            show_info(fn, params, ret_type, model)
        try:
            result_set = (
                cursor.callfunc(fn, ret_type.value, keywordParameters=params)
                if params is not None
                else cursor.callfunc(fn, ret_type.value)
            )
            return extract_of_result_data(result_set, ret_type, model, jsonfy)
        except Exception as e:
            process_exception(throw, e)
        finally:
            safely_exec(lambda l: l.close(), args=[cursor])
            if connection_provided is False:
                safely_exec(lambda l: l.commit(), args=[connection])
                safely_exec(lambda l: l.close(), args=[connection])

        return None

    def exec(self, fn_name: str, ret_type: OracleType, params: dict = None, list_params: List[Any] = None,
             model: Any = None,
             connection=None, jsonfy: bool = False, throw=False) -> Any:
        raise NotImplementedError("")


class ZDBOraclePool(ZDBPool):

    def __init__(self, db: ZDatabase = None, config: dict = None):
        self.db = db
        if db is None:
            self.db = ZOracle.setup(config)
        self.config = config
        self.__pool = None
        self.__max = 5
        self.__min = 1
        self.__threading = False
        self.__homogeneous = True
        self.__pool_created: bool = False
        if config is not None:
            self.setup_extras(config)

    def setup_db(self, db: ZDatabase) -> None:
        self.db = db

    def setup_extras(self, config: dict) -> None:
        self.config = config
        try:
            self.__max = config.get("max_connections", 5)
            self.__min = config.get("min_connections", 1)
            self.__threading = config.get("threading", False)
            self.__homogeneous = config.get("homogeneous", True)
        except Exception as e:
            zL.e("An error occurred when setup config", exc_info=e)

    def initialize_pool(
            self,
            max_connections: int = None,
            min_connections: int = None
    ) -> bool:
        if self.__pool_created:
            return False
        zL.i("Initializing Pool...")
        self.__pool = cx_Oracle.SessionPool(
            user=self.config.get("user"),
            password=self.config.get("password"),
            dsn=get_str_connection(self.config, mode="DSN"),
            homogeneous=self.__homogeneous,
            encoding="UTF-8",
            max=self.__max if max_connections is None else max_connections,
            min=self.__min if min_connections is None else min_connections,
            threaded=self.__threading,
        )
        self.__pool_created = True
        zL.i("Pool Started Successfully...")
        return True

    def close_pool(self, force: bool = False):
        try:
            if self.__pool_created:
                self.__pool.close(force=force)
                self.__pool_created = False
                zL.i("Pool Closed Successfully")
        except Exception as e:
            zL.e("An error occurred when try close pool", exc_info=e)

    def get_pool_connection(self):
        if self.__pool_created:
            return self.__pool.acquire()
        zL.w("DB Pool not initialized, try to initialize pool connection...")
        try:
            self.initialize_pool()
            self.__pool_created = True
            return self.__pool.acquire()
        except Exception as e:
            zL.e("Unable to initialize the connections pool...", exc_info=e)
            self.__pool_created = False

    def release_connection(self, connection) -> bool:
        try:
            if self.__pool_created:
                self.__pool.release(connection)
                return True
        except Exception as e:
            zL.e("An error occurred when try to release connection", exc_info=e)
            return False

    def get_db(self):
        return self.db
