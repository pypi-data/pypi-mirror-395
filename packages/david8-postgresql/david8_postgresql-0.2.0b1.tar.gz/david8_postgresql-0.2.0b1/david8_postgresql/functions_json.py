import dataclasses
import json

from david8.core.arg_convertors import to_col_or_expr
from david8.core.fn_generator import FnCallableFactory as _Factory
from david8.core.fn_generator import Function as Fn
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import ExprProtocol, FunctionProtocol


@dataclasses.dataclass(slots=True)
class _JsonValuesFn(Fn):
    operator: str
    column: str | ExprProtocol
    values: tuple[str, ...]

    def _render_operator_expr(self, dialect: DialectProtocol) -> str:
        return f"{to_col_or_expr(self.column, dialect)}{self.operator}"


@dataclasses.dataclass(slots=True)
class _ExtractField(_JsonValuesFn):
    def _get_sql(self, dialect: DialectProtocol) -> str:
        op_sql = self._render_operator_expr(dialect)
        items = self.operator.join(f"'{v}'" for v in self.values)
        return f"{op_sql}{items}"


@dataclasses.dataclass(slots=True)
class _DelKey(_JsonValuesFn):
    def _get_sql(self, dialect: DialectProtocol) -> str:
        op_sql = self._render_operator_expr(dialect)
        return f"{op_sql}'{self.values[0]}'"


@dataclasses.dataclass(slots=True)
class _JsonbSet(Fn):
    column: str | ExprProtocol
    path: list[str]
    value: str | int | dict

    def _get_sql(self, dialect: DialectProtocol) -> str:
        sql = to_col_or_expr(self.column, dialect)
        paths = ''.join(('{', ','.join(self.path), '}'))
        if isinstance(self.value, dict):
            value = ''.join(("'", json.dumps(self.value), "'"))
        elif isinstance(self.value, int):
            value = f"'{self.value}'::jsonb"
        else:
            value = f'\'"{self.value}"\'::jsonb'

        return f"jsonb_set({sql}, '{paths}', {value})"


@dataclasses.dataclass(slots=True)
class _ExtractFieldFactory(_Factory):
    def __call__(self, column: str | ExprProtocol, *paths: str) -> FunctionProtocol:
        return _ExtractField(name=self.name, column=column, operator='->', values=paths)


@dataclasses.dataclass(slots=True)
class _HasKeyFactory(_Factory):
    def __call__(self, column: str | ExprProtocol, key: str) -> FunctionProtocol:
        return _ExtractField(name=self.name, column=column, operator='?', values=(key, ))


@dataclasses.dataclass(slots=True)
class _DelKeyFactory(_Factory):
    def __call__(self, column: str | ExprProtocol, key: str) -> FunctionProtocol:
        return _DelKey(name=self.name, column=column, operator='-', values=(key, ))


@dataclasses.dataclass(slots=True)
class _JsonbSetFactory(_Factory):
    def __call__(self, column: str | ExprProtocol, path: list[str], value: str | int | dict) -> FunctionProtocol:
        return _JsonbSet(name='jsonb_set', column=column, path=path, value=value)


extract_field = _ExtractFieldFactory()
has_key = _HasKeyFactory()
del_key = _DelKeyFactory()
jsonb_set = _JsonbSetFactory()
