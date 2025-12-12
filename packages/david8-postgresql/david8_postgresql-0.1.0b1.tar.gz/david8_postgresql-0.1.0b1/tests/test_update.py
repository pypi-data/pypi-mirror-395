from david8.expressions import col, val
from david8.predicates import eq, eq_c
from david8.protocols.dml import UpdateProtocol
from parameterized import parameterized

from tests.base_test import BaseTest


class TestUpdate(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb
            .update()
            .table('movie')
            .set_('name', 'aliens')
            .where(eq('movie', ''))
            .returning('id', 'name'),
            'UPDATE movie SET name = %(p1)s WHERE movie = %(p2)s RETURNING id, name',
            {'p1': 'aliens', 'p2': ''},
        ),
        (
            BaseTest.qb_w
            .update()
            .table('movie')
            .set_('name', 'aliens')
            .where(eq('movie', ''))
            .returning('id', 'name'),
            'UPDATE "movie" SET "name" = %(p1)s WHERE "movie" = %(p2)s RETURNING "id", "name"',
            {'p1': 'aliens', 'p2': ''},
        ),
        (
            BaseTest.qb
            .update()
            .table('movie', 'm', 'art')
            .set_('name', BaseTest.qb.select(val('aliens')))
            .set_('directed_by', BaseTest.qb.select(val('James Cameron')))
            .where(eq('movie', ''))
            .returning('id', 'name'),
            "UPDATE art.movie AS m SET name = (SELECT 'aliens'), directed_by = (SELECT 'James Cameron')"
            " WHERE movie = %(p1)s RETURNING id, name",
            {'p1': ''},
        ),
        (
            BaseTest.qb
            .update()
            .table('movie')
            .set_('name', col('new_name'))
            .where(eq('movie', ''))
            .returning('id', 'name'),
            'UPDATE movie SET name = new_name WHERE movie = %(p1)s RETURNING id, name',
            {'p1': ''},
        ),
    ])
    def test_update_returning(self, query: UpdateProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)

    @parameterized.expand([
        (
            BaseTest.qb
            .update()
            .table('users', alias='u')
            .set_('age', 27)
            .from_table('data', alias='d')
            .where(eq_c('u.ud', 'd.id')),
            'UPDATE users AS u SET age = %(p1)s FROM data AS d WHERE u.ud = d.id',
            {'p1': 27},
        ),
        (
            BaseTest.qb_w
            .update()
            .table('users', alias='u')
            .set_('age', 27)
            .from_table('data', alias='d')
            .where(eq_c('u.ud', 'd.id')),
            'UPDATE "users" AS "u" SET "age" = %(p1)s FROM "data" AS "d" WHERE "u"."ud" = "d"."id"',
            {'p1': 27},
        ),
    ])
    def test_update_from_table(self, query: UpdateProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
