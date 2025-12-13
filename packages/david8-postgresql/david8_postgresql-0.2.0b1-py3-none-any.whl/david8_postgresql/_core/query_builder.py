from david8.core.base_query_builder import BaseQueryBuilder as _BaseQueryBuilder
from david8.protocols.sql import AliasedProtocol, ExprProtocol, FunctionProtocol

from ..protocols.dml import SelectProtocol, UpdateProtocol
from ..protocols.query_builder import QueryBuilderProtocol
from .dml import Select, Update


class QueryBuilder(_BaseQueryBuilder, QueryBuilderProtocol):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        return Select(select_columns=args, dialect=self._dialect)

    def update(self) -> UpdateProtocol:
        return Update(dialect=self._dialect)
