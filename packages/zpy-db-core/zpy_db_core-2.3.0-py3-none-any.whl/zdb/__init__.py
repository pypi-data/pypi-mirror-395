from typing import Any, Tuple

from zpy.utils.funcs import safely_exec

from zdb.commons import ZDatabase


class ZDBTransact:

    def __init__(self, db: ZDatabase, init_cursor=False):
        self.db = db
        self.session = None
        self.cursor = None
        self.init_cursor = init_cursor

    def __enter__(self):
        self.session = self.db.new_connect()
        if self.init_cursor is True:
            self.cursor = self.session.cursor()
        return self

    def run(self, statement: str, params: Tuple[Any] = None):
        if not self.init_cursor:
            raise ValueError("Current cursor is not initialized")
        self.cursor.execute(statement, params)

    def query(self, statement: str, params: Tuple[Any] = None):
        if not self.init_cursor:
            raise ValueError("Current cursor is not initialized")
        self.cursor.execute(statement, params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.session.rollback()
        else:
            self.session.commit()
        safely_exec(lambda x: x.close(), [self.session])
        if self.init_cursor:
            safely_exec(lambda x: x.close(), [self.cursor])
