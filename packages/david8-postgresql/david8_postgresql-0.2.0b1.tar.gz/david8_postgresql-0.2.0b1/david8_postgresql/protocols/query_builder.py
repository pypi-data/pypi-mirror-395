from david8.protocols.query_builder import QueryBuilderProtocol as _QueryBuilderProtocol
from david8.protocols.sql import AliasedProtocol, ExprProtocol, FunctionProtocol

from .dml import SelectProtocol, UpdateProtocol


class QueryBuilderProtocol(_QueryBuilderProtocol):
    def update(self) -> UpdateProtocol:
        pass

    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        pass
