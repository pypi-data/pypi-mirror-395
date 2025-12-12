from david8.core.base_dialect import BaseDialect as _BaseDialect
from david8.param_styles import NumericParamStyle, PyFormatParamStyle
from david8.protocols.dialect import ParamStyleProtocol

from .core.query_builder import QueryBuilder as _QueryBuilder
from .protocols.query_builder import QueryBuilderProtocol


def get_qb(
    param_style: ParamStyleProtocol | NumericParamStyle = None,
    is_quote_mode: bool = False,
) -> QueryBuilderProtocol:
    dialect = _BaseDialect(param_style or PyFormatParamStyle(), is_quote_mode)
    return _QueryBuilder(dialect)
