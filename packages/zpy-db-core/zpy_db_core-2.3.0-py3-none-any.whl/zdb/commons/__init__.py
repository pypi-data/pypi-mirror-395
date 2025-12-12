from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum
from typing import Union, Any, List, Dict, Callable, Optional, TypeVar
from dataclasses import dataclass

from zpy.logger import zL
from zpy.app import zapp_context as ctx

T = TypeVar('T')


def show_info(fn: str, params: Union[List[Any], Dict[Any, Any]], ret_type: Enum, v_model):
    print("\n|-------------------------------------------------|\n")
    print(f"   Function Called: {fn} ")
    print("            Params: {}".format(params))
    print("       Return Type: {}".format(ret_type.name))
    print(f"        Ref  Model: {v_model}")
    print("\n|-------------------------------------------------|\n")


@dataclass
class ZDBConfig:
    user: str
    password: str
    database: str
    host: str
    port: int = 3306
    autocommit: bool = False
    raise_on_warnings = True
    service: str = None  # Use for Oracle


parser_types = [
    None,
    lambda x: float(x),
    lambda x: str(x),
    lambda x: int(x),
    lambda x: Decimal(str(x).strip(' "')),
    lambda x: bool(x),
    lambda x: x
]


class DBTypes(Enum):
    cursor = 1
    float = 2
    string = 3
    integer = 4
    decimal = 5
    bool = 6
    single_item = 7
    out_integer = 4
    out_bool = 6


def get_map_type(r_type: DBTypes) -> Callable:
    return parser_types[r_type.value - 1]


def build_params(dict_params: dict, list_params: List[Any]) -> List[Any]:
    if dict_params is not None:
        return list(dict_params.values())
    if list_params is not None:
        return list_params
    return []


def process_exception(throw: bool, e: Exception):
    if throw is True:
        raise e
    zL.e("Failed when try to call function or stored procedure.", exc_info=e)


class ZDatabase(ABC):
    @classmethod
    @abstractmethod
    def setup(cls, config: dict, verbose: bool = False):
        """
        Setup connection arguments using dictionary
        """
        ...

    @classmethod
    @abstractmethod
    def setup_of(cls, config: ZDBConfig, verbose: bool = False):
        """
        Setup connection data
        """
        ...

    @classmethod
    @abstractmethod
    def from_of(cls, user: str, password: str, host: str, db_name: str, verbose: bool = False):
        """
        Setup connection data
        """
        ...

    def new_connect(self) -> Any:
        ...

    def __validate_config(self) -> Union[dict, str]:
        ...

    def call(self, name: str, ret_type: DBTypes, params: dict = None, list_params: List[Any] = None, model: Any = None,
             connection=None, jsonfy: bool = False, throw=False) -> Any:
        """Stored procedure caller

        Args:
            name (str): Stored procedure name
            ret_type (DBTypes): Type of data returned from stored procedure
            params (dict, optional): params for the procedure. Defaults to None.
            list_params (List[Any], optional): positional list params to the procedure. Defaults to None.
            model (Any, optional): model for build returned data. Defaults to None.
            connection ([type], optional): connection database. Defaults to None.
            jsonfy (bool, optional): return data in dict format if model is null. Defaults to False.
            throw (bool,optional)

        Returns:
            Any: processed data
        """
        ...

    def exec(self, fn_name: str, ret_type: DBTypes, params: dict = None, list_params: List[Any] = None,
             model: Any = None,
             connection=None, jsonfy: bool = False, throw=False) -> Any:
        """Function executor

        Args:
            fn_name (str): Stored procedure name
            ret_type (DBTypes): Type of data returned from stored procedure
            params (dict, optional): params for the procedure. Defaults to None.
            list_params (List[Any], optional): positional list params to the procedure. Defaults to None.
            model (Any, optional): model for build returned data. Defaults to None.
            connection ([type], optional): connection database. Defaults to None.
            jsonfy (bool, optional): return data in dcit format if model is null. Defaults to False.
            throw (bool,optional)
        Returns:
            Any: processed data
        """
        ...

    @abstractmethod
    def init_local_client(self, path: str):
        """
        Initialize local client
        """
        ...

    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        ...

    @abstractmethod
    def get_connection(self) -> Any:
        ...


class ZDBPool(ABC):

    @abstractmethod
    def setup_db(self, db: ZDatabase) -> None:
        ...

    @abstractmethod
    def get_db(self):
        ...

    @abstractmethod
    def setup_extras(self, config: dict) -> None:
        ...

    @abstractmethod
    def get_pool_connection(self) -> Any:
        ...

    @abstractmethod
    def release_connection(self, connection) -> bool:
        ...

    @abstractmethod
    def close_pool(self):
        pass

    @abstractmethod
    def initialize_pool(
            self,
            max_connections: int = 5,
            min_connections: int = 1,
    ) -> bool:
        ...


@dataclass
class ZDBWrapper:
    connection: Any
    db: ZDatabase
    name: str
    verbose: bool

    def configure(self, connection: Any):
        if self.connection:
            self.release()
        self.connection = connection

    def has_connection(self) -> bool:
        return self.connection is not None

    def release(self):
        if not self.connection:
            return
        try:
            self.connection.close()
            self.connection = None
            if self.verbose:
                ctx().logger.info(f"Connection of {self.name} closed")
        except Exception as e:
            ctx().logger.err("An error occurred while releasing connections", exc_info=e)


class ZDBConnectionManager:

    def __init__(self, verbose: bool = False, auto_commit: bool = True):
        self.dbs: Dict[str, ZDBWrapper] = {}
        self.count = 0
        self.verbose = verbose
        self.auto_commit = auto_commit

    def add(self, name: str, db: ZDatabase) -> 'ZDBConnectionManager':
        """
        Add new database configuration.
        @param name: database identifier name
        @param db: database configuration instance
        @return: manager
        """
        self.dbs[name] = ZDBWrapper(None, db, name, self.verbose)
        return self

    def __configure(self, name: str):
        if name not in self.dbs:
            return
        if self.dbs.get(name).has_connection():
            ctx().logger.warn(f"Warning: Already exist a connection opened for {name} database.")
            return
        self.dbs.get(name).configure(
            self.dbs.get(name).db.new_connect()
        )
        self.count = self.count + 1
        if self.verbose:
            ctx().logger.info(f"New connection opened for {name} database.")

    def open_for(self, dbs: List[str]) -> None:
        """
        Open db connections for specified database configurations.
        @param dbs: Db names to open connections.
        @return: None
        """
        for name in dbs:
            self.__configure(name)

    def open_single(self, name: str) -> None:
        """
        Open db connections for all database configurations.
        @return: None
        """
        self.__configure(name)

    def open(self) -> None:
        """
        Open db connections for all database configurations.
        @return: None
        """
        for name in self.dbs.keys():
            self.__configure(name)

    def release_for(self, name: str) -> None:
        """
        Release specific opened connections
        @return: None
        """
        db = self.dbs.get(name, None)
        if db and db.has_connection():
            if self.auto_commit:
                self.commit_for(name)
            db.release()

    def release(self) -> None:
        """
        Release all opened connections
        @return: None
        """
        for name in self.dbs.keys():
            if self.auto_commit:
                self.commit_for(name)
            self.dbs.get(name).release()

    def count_connections(self) -> int:
        """
        Count all opened connections
        @return: total of open connections
        """
        return self.count

    def has_connections(self, name: str) -> bool:
        """
        Verify if database provided has opened connection.
        @param name: database name
        @return: true if it has connection
        """
        if name in self.dbs:
            return self.dbs.get(name).has_connection()
        return False

    def connection(self, name: str) -> [Any]:
        """
        Retrieve connection for database name provided.
        @param name: database name
        @return: connection
        """
        if name in self.dbs:
            if self.dbs.get(name).has_connection():
                return self.dbs.get(name).connection
        return None

    def commit_for(self, name: str) -> None:
        """
        Commit to specified database
        @param name: database name
        @return: connection
        """
        if name in self.dbs:
            if self.dbs.get(name).has_connection():
                self.dbs.get(name).connection.commit()

    def commit(self) -> None:
        """
        Commit all connections
        @return: connection
        """
        for db_name in self.dbs.keys():
            self.commit_for(db_name)

    def force_connection(self, name: str) -> Optional[Any]:
        """
        Force connection retrieve.
        If not existing opened connection for database provided,
        will try to open and return connection
        @param name: database name
        @return: connection
        """
        if name in self.dbs:
            if self.dbs.get(name).has_connection():
                return self.dbs.get(name).connection
            self.open_single(name)
            if self.dbs.get(name).has_connection():
                return self.dbs.get(name).connection
        return None

    def database(self, name: str, db_type: T = None) -> Union[T, Any]:
        """
        Retrieve database by name
        @param name: database name
        @param db_type: Database type
        @return:
        """
        if name in self.dbs:
            return self.dbs.get(name).db
        return None

    def __del__(self):
        self.release()
