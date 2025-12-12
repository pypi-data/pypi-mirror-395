import dataclasses

from david8.core.base_dml import BaseSelect, BaseUpdate, TargetTableConstruction, log_and_reset
from david8.protocols.dialect import DialectProtocol

from ..protocols.dml import SelectProtocol, UpdateProtocol


@dataclasses.dataclass(slots=True)
class Select(BaseSelect, SelectProtocol):
    row_lock_mode: str = ''

    def for_key_share(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR KEY SHARE'
        return self

    def for_key_share_nw(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR KEY SHARE NOWAIT'
        return self

    def for_key_share_sl(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR KEY SHARE SKIP LOCKED'
        return self

    def for_share(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR SHARE'
        return self

    def for_share_nw(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR SHARE NOWAIT'
        return self

    def for_share_sl(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR SHARE SKIP LOCKED'
        return self

    def for_update(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR UPDATE'
        return self

    def for_update_nw(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR UPDATE NOWAIT'
        return self

    def for_update_sl(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR UPDATE SKIP LOCKED'
        return self

    def for_nk_update(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR NO KEY UPDATE'
        return self

    def for_nk_update_nw(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR NO KEY UPDATE NOWAIT'
        return self

    def for_nk_update_sl(self) -> 'SelectProtocol':
        self.row_lock_mode = 'FOR NO KEY UPDATE SKIP LOCKED'
        return self

    @log_and_reset
    def get_sql(self, dialect: DialectProtocol = None) -> str:
        """
        TODO: move to _get_sql() on david8 side
        """
        dialect = dialect or self.dialect
        with_query = self._with_queries_to_sql(dialect)
        select = self._columns_to_sql(dialect)
        from_ref = self._from_to_sql(dialect)
        joins = self._joins_to_sql(dialect)
        where = self.where_construction.get_sql(dialect)
        group_by = self._group_by_to_sql(dialect)
        having = self._having_to_sql(dialect)
        union = self._union_to_sql(dialect)
        order_by = self._order_by_to_sql()

        limit = f' LIMIT {self.limit_value}' if self.limit_value else ''
        sql =  f'{with_query}SELECT {select}{from_ref}{joins}{where}{group_by}{order_by}{having}{limit}{union}'
        return f'{sql} {self.row_lock_mode}' if self.row_lock_mode else sql


@dataclasses.dataclass(slots=True)
class Update(BaseUpdate, UpdateProtocol):
    returning_columns: tuple[str, ...] = dataclasses.field(default_factory=tuple)
    from_table_constr: TargetTableConstruction = dataclasses.field(default_factory=TargetTableConstruction)
    from_table_alias: str = ''

    def _from_table_to_sql(self, dialect: DialectProtocol) -> str:
        if not self.from_table_constr.from_table:
            return ''

        from_table = f' FROM {self.from_table_constr.get_sql(dialect)}'
        if self.from_table_alias:
            from_table = f'{from_table} AS {dialect.quote_ident(self.from_table_alias)}'

        return from_table

    def _get_sql(self, dialect: DialectProtocol) -> str:
        table = self._table_to_sql(dialect)
        set_columns = self._set_construction_to_sql(dialect)
        from_ = self._from_table_to_sql(dialect)
        where = self.where_construction.get_sql(dialect)
        if self.returning_columns:
            returning = f' RETURNING {", ".join(dialect.quote_ident(r) for r in self.returning_columns)}'
        else:
            returning = ''

        return f'UPDATE {table}{set_columns}{from_}{where}{returning}'

    def returning(self, *args: str) -> 'UpdateProtocol':
        self.returning_columns += args
        return self

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> 'UpdateProtocol':
        self.from_table_constr.set_source(table_name, db_name)
        self.from_table_alias = alias
        return self
