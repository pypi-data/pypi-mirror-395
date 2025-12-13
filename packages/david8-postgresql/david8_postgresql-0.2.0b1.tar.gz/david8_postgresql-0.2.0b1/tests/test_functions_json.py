from david8.protocols.sql import FunctionProtocol
from parameterized import parameterized

from david8_postgresql.functions_json import del_key, extract_field, has_key, jsonb_set
from tests.base_test import BaseTest


class TestFunctionsJson(BaseTest):

    @parameterized.expand([
        (
            extract_field('meta', 'version', 'name'),
            "SELECT meta->'version'->'name'",
            "SELECT \"meta\"->'version'->'name'",
        ),
        (
            extract_field('meta', 'version', 'name'),
            "SELECT meta->'version'->'name'",
            "SELECT \"meta\"->'version'->'name'",
        ),
    ])
    def test_extract_field(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)

    @parameterized.expand([
        (
            has_key('meta', 'version'),
            "SELECT meta?'version'",
            "SELECT \"meta\"?'version'",
        ),
    ])
    def test_has_key(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)

    @parameterized.expand([
        (
            del_key('meta', 'version'),
            "SELECT meta-'version'",
            "SELECT \"meta\"-'version'",
        ),
    ])
    def test_del_key(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)

    @parameterized.expand([
        (
            jsonb_set('meta', ['version', 'name'], 'Xia'),
            "SELECT jsonb_set(meta, '{version,name}', '\"Xia\"'::jsonb)",
            'SELECT jsonb_set("meta", \'{version,name}\', \'"Xia"\'::jsonb)',
        ),
        (
            jsonb_set('meta', ['version', 'major'], 22),
            "SELECT jsonb_set(meta, '{version,major}', '22'::jsonb)",
            'SELECT jsonb_set("meta", \'{version,major}\', \'22\'::jsonb)',
        ),
        (
            jsonb_set('meta', ['version'], {'name': 'Xia', 'major': 22}),
            'SELECT jsonb_set(meta, \'{version}\', \'{"name": "Xia", "major": 22}\')',
            'SELECT jsonb_set("meta", \'{version}\', \'{"name": "Xia", "major": 22}\')',
        ),
    ])
    def test_jsonb_set(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)
