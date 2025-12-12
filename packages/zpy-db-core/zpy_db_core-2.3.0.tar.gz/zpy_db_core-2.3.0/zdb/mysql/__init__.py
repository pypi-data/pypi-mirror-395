import copy
from dataclasses import asdict

from typing import Optional, Any, List, Callable, TypeVar, Generic

from mysql.connector import MySQLConnection
from mysql import connector
import mysql

from zdb.commons import show_info, DBTypes, get_map_type, ZDatabase, ZDBConfig, build_params, process_exception
from zpy.utils.funcs import safely_exec

T = TypeVar("T")


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


def __fn_extract_data(result_set, rows, column_names, ret_type: DBTypes, model, jsonfy=False) -> Any:
    """
        Inner Data Builder
    """
    if ret_type == DBTypes.cursor:
        if model is not None:
            return [_instantiate_model(model, dict(zip(column_names, r))) for r in rows]
        if jsonfy is True:
            return [dict(zip(column_names, r)) for r in rows]
        return rows
    else:
        if len(rows) > 0:
            parser = get_map_type(ret_type)
            if model is not None:
                return _instantiate_model(model, dict(zip(column_names, rows[0])))
            if jsonfy is True:
                return dict(zip(column_names, rows[0]))
            if ret_type == DBTypes.single_item:
                return rows[0]
            return parser(rows[0][0])
        return None


def extract_data(result_set, ret_type: DBTypes, cursor, model, jsonfy=False) -> Any:
    """
        Data Builder for custom stored procedures
    """
    for result in cursor.stored_results():
        colum_names = result.column_names
        rows = result.fetchall()
        if not ret_type:
            return rows
        return __fn_extract_data(result_set, rows, colum_names, ret_type, model, jsonfy)
    return result_set


def fn_extract_data(result_set, ret_type: DBTypes, cursor, model, jsonfy=False) -> Any:
    """
        Data Builder for custom functions
    """
    colum_names = cursor.column_names
    rows = cursor.fetchall()
    if not ret_type:
        return rows
    return __fn_extract_data(result_set, rows, colum_names, ret_type, model, jsonfy)


class ZMySQL(ZDatabase):

    def __init__(self, dict_config: Optional[dict] = None, config: Optional[ZDBConfig] = None,
                 verbose: bool = False):
        self.dict_config = dict_config
        self.config = config
        self.verbose = verbose

    @classmethod
    def setup(cls, config: dict, verbose: bool = False):
        return cls(config, config=None, verbose=verbose)

    @classmethod
    def setup_of(cls, config: ZDBConfig, verbose: bool = False):
        return cls(config=config, verbose=verbose)

    @classmethod
    def from_of(cls, user: str, password: str, host: str, db_name: str, verbose: bool = False):
        return cls({
            'user': user,
            'password': password,
            'host': host,
            'database': db_name,
            'raise_on_warnings': False
        }, verbose=verbose)

    def new_connect(self) -> MySQLConnection:
        final_config = self.__validate_config()
        if final_config is None:
            raise ValueError("The value of db configuration can not be null.")
        return connector.connect(**final_config)

    def call(self, name: str, ret_type: Optional[DBTypes] = None, params: Optional[dict] = None,
             list_params: Optional[List[Any]] = None,
             model: Optional[Any] = None,
             connection=None, jsonfy: bool = False, throw: bool = True) -> Any:
        """Stored procedure caller

        Args:
            name (str): Stored procedure name
            ret_type (DBTypes): Type of data returned from stored procedure
            params (dict, optional): params for the procedure. Defaults to None.
            list_params (List[Any], optional): positional list params to the procedure. Defaults to None.
            model (Any, optional): model for build returned data. Defaults to None.
            connection ([type], optional): connection database. Defaults to None.
            jsonfy (bool, optional): return data in dict format if model is null. Defaults to False.
            throw (bool, optional): raise exceptions

        Returns:
            Any: processed data
        """
        return self.__call(lambda c, fn, p: c.callproc(fn, p), extract_data, name, ret_type, params, list_params, model,
                           connection, jsonfy, throw)

    def __call(self, runner: Callable, extractor: Callable, name: str, ret_type: DBTypes, params: dict = None,
               list_params: List[Any] = None,
               model: Any = None,
               connection=None, jsonfy: bool = False, throw: bool = True) -> Any:
        cn = connection
        connection_passed = True
        if connection is None:
            connection_passed = False
            cn = self.new_connect()

        cursor = None
        if cn is not None:
            cursor = cn.cursor()

        if cn is None or cursor is None:
            raise Exception("Can't get db connection")
        if self.verbose:
            show_info(name, params, ret_type, model)
        try:
            result_set = runner(cursor, name, build_params(dict_params=params, list_params=list_params))
            return extractor(result_set, ret_type, cursor, model, jsonfy)
        except mysql.connector.Error as error:
            process_exception(throw, error)
        except Exception as e:
            process_exception(throw, e)
        finally:
            if not connection_passed:
                safely_exec(lambda c: c.close(), args=[cursor])
                if cn.is_connected():
                    safely_exec(lambda c: c.commit(), args=[cn])
                    safely_exec(lambda c: c.close(), args=[cn])
        return None

    def exec(self, fn_name: str, ret_type: DBTypes = None, params: dict = None, list_params: List[Any] = None,
             model: Any = None,
             connection=None, jsonfy: bool = False, throw: bool = True) -> Any:
        """Function executor

        Args:
            fn_name (str): Stored procedure name
            ret_type (DBTypes): Type of data returned from stored procedure
            params (dict, optional): params for the procedure. Defaults to None.
            list_params (List[Any], optional): positional list params to the procedure. Defaults to None.
            model (Any, optional): model for build returned data. Defaults to None.
            connection ([type], optional): connection database. Defaults to None.
            jsonfy (bool, optional): return data in dict format if model is null. Defaults to False.
            throw: (bool, optional): raise exceptions

        Returns:
            Any: processed data
        """
        return self.__call(lambda c, fn, p: c.execute(f'SELECT {fn}', p), fn_extract_data, fn_name, ret_type, params,
                           list_params, model,
                           connection, jsonfy, throw)

    def __validate_config(self) -> dict:
        if self.config is not None:
            return asdict(self.config)
        return self.dict_config

    def init_local_client(self, path: str):
        raise NotImplementedError("Not implemented for MySQL!")

    def connect(self):
        raise NotImplementedError("Not implemented for MySQL!")

    def close(self) -> None:
        raise NotImplementedError("Not implemented for MySQL!")

    def is_connected(self) -> bool:
        raise NotImplementedError("Not implemented for MySQL!")

    def get_connection(self) -> Any:
        raise NotImplementedError("Not implemented for MySQL!")


class ZDBMediator(Generic[T]):
    SINGLE_NAME_DS: str = 'MAIN'

    def __init__(self, common_config: dict, verbose: bool = False):
        self.common_config = common_config
        self.verbose = verbose
        self.data_sources = []

    def __default_configured(self) -> bool:
        return len(list(filter(lambda x: x['default'] is True, self.data_sources))) > 0

    def __name_configured(self, name: str) -> bool:
        return len(list(filter(lambda x: x['name'] == name, self.data_sources))) > 0

    @classmethod
    def of(cls, common_config: dict, verbose=False):
        return cls(common_config, verbose)

    @classmethod
    def single(cls, config: dict, verbose=False):
        instance = cls(config, verbose)
        instance.add_ds(config, True, verbose, name=cls.SINGLE_NAME_DS)
        return instance

    def add_ds(self, config: dict, default: bool = False, verbose=False, name: str = None):
        _name = config["database"]
        if name is not None:
            _name = name
        if self.__name_configured(_name) is True:
            raise ValueError(f'name already configured')
        if default is True and self.__default_configured() is True:
            default = False

        self.data_sources.append(
            {
                "instance": ZMySQL.setup(config, verbose),
                "name": _name,
                "config": config,
                "default": default
            }
        )

    def add_common_with(self, database: str, user: str, password: str, default: bool = False, name: str = None):
        _name = database
        if name is not None:
            _name = name
        if self.__name_configured(_name) is True:
            raise ValueError(f'name already configured')
        if default is True and self.__default_configured() is True:
            default = False
        _config = copy.copy(self.common_config)
        _config.update({"user": user, "password": password, "database": database})
        self.data_sources.append(
            {
                "instance": ZMySQL.setup(_config, self.verbose),
                "name": _name,
                "config": _config,
                "default": default
            }
        )

    def get(self, name: str) -> ZMySQL:
        ds = list(filter(lambda x: x['name'] == name, self.data_sources))
        if ds is None or len(ds) == 0:
            raise ValueError(f"Datasource with name: {name} is not configured")
        return ds[0]["instance"]

    def default(self) -> ZMySQL:
        ds = list(filter(lambda x: x['default'] is True, self.data_sources))
        if ds is None:
            raise ValueError(f"Datasource by default not configured")
        return ds[0]["instance"]

    def notify(self):
        ...

    def add(self, config: dict, is_default: bool = False, name: str = None):
        self.add_ds(config, is_default, self.verbose, name)
        return self

    def add_common(self, database: str, user: str, password: str, is_default: bool = False, name: str = None):
        self.add_common_with(database, user, password, is_default, name)
        return self

    def build(self):
        """
        Will be removed
        """
        return self


class ZMySQLCluster:
    reader: ZMySQL = None
    writer: ZMySQL = None

    def __init__(self):
        ...
