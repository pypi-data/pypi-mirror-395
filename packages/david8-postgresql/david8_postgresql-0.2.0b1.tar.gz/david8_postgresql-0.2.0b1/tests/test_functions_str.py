from david8.expressions import param, val
from david8.protocols.sql import FunctionProtocol
from parameterized import parameterized

from david8_postgresql.functions_str import concat
from tests.base_test import BaseTest


class TestFunctionsStr(BaseTest):

    @parameterized.expand([
        (
            concat('col1', 1, 'col2', 0.5, concat(val('static'), param(2))).as_('new_field'),
            "SELECT concat(col1 || '1' || col2 || '0.5' || concat('static' || %(p1)s)) AS new_field",
            'SELECT concat("col1" || \'1\' || "col2" || \'0.5\' || concat(\'static\' || %(p1)s)) AS "new_field"',
            {'p1': 2}
        ),
    ])
    def test_concat(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str, exp_params: dict):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)
        self.assertEqual(query.get_parameters(), exp_params)
