from sqlalchemy import select, insert, update, delete
from sqlalchemy.sql import Select
from sqlalchemy.engine import Connection
from sqlalchemy import DateTime, Integer, BigInteger, String
from sqlalchemy import func
from typing import Any
from pydbinterface import DBInterface
import datetime
from .sqlalchemy_data_mapper import DataMapper
import time

class PostgresDAL(DBInterface):
    def __init__(self, mapper: DataMapper, connection: Connection):
        self.mapper = mapper
        self.connection = connection
        self._transaction = None
    def _build_statement(self, base_stmt, where):
        if where is None:
            return base_stmt
        elif isinstance(where, Select):
            return where
        elif isinstance(where, dict):
            stmt = base_stmt
            for k, v in where.items():
                stmt = stmt.where(self.mapper.table.c[k] == v)
            return stmt
        else:
            raise TypeError("The 'where' parameter must be a dict or SQLAlchemy Select")

    def _execute_statement(self, stmt, fetch='all'):
        try:
            result = self.connection.execute(stmt)
            if not self._transaction:
                self.commit_transaction()
        except Exception:
            self.rollback_transaction()
            raise Exception("Error executing statement")
        match fetch:
            case 'one':
                return result.fetchone()
            case 'scalar':
                return result.scalar()
            case _:
                return result.fetchall()
    
    def create(self, data: Any) -> Any:
        if not isinstance(data, dict):
            raise TypeError("The 'data' parameter must be a dict")
        data = self.mapper.dict_to_row(data)
        if 'created_at' in self.mapper.table.c:
            data['created_at'] = self.set_date(self.mapper.table.c['created_at'].type)
        
        stmt = insert(self.mapper.table).values(**data).returning(self.mapper.table)
        result = self._execute_statement(stmt, fetch='one')
        if result is not None:
            return dict(result._mapping)  # type: ignore

    def read(self, where: Any) -> Any:
        base_stmt = select(self.mapper.table)
        stmt = self._build_statement(base_stmt, where)
        results = self._execute_statement(stmt, fetch='all')
        if results is None:
            return []
        return [dict(row._mapping) for row in results]

    def update(self, where: Any, data: Any) -> Any:
        if not isinstance(data, dict):
            raise TypeError("The 'data' parameter must be a dict")
        data = self.mapper.dict_to_row(data)
        if 'updated_at' in self.mapper.table.c:
            data['updated_at'] = self.set_date(self.mapper.table.c['updated_at'].type)
        
        base_stmt = update(self.mapper.table).values(**data).returning(self.mapper.table)
        stmt = self._build_statement(base_stmt, where)
        results = self._execute_statement(stmt, fetch='all')
        if results is None:
            return []
        return [dict(row._mapping) for row in results]

    def delete(self, where: Any) -> Any:
        base_stmt = delete(self.mapper.table).returning(self.mapper.table)
        stmt = self._build_statement(base_stmt, where)
        results = self._execute_statement(stmt, fetch='all')
        if results is None:
            return []
        return [dict(row._mapping) for row in results]

    def begin_transaction(self):
        if hasattr(self.connection, 'begin'):
            self._transaction = self.connection.begin()
        else:
            raise NotImplementedError("The connection does not support explicit transactions.")

    def commit_transaction(self):
        if self._transaction:
            self._transaction.commit()
            self._transaction = None
        else:
            self.connection.commit()

    def rollback_transaction(self):
        if self._transaction:
            self._transaction.rollback()
            self._transaction = None
        else:
            self.connection.rollback()

    def count(self, where: Any = None) -> int:
        base_stmt = select(func.count()).select_from(self.mapper.table)
        stmt = self._build_statement(base_stmt, where)
        count_value = self._execute_statement(stmt, fetch='scalar')
        if not isinstance(count_value, int):
            return 0
        return count_value

    @staticmethod
    def set_date(column_type):
        if isinstance(column_type, (DateTime, String)):
            return datetime.datetime.now(datetime.timezone.utc)
        if isinstance(column_type, (Integer, BigInteger)):
            return int(time.time())