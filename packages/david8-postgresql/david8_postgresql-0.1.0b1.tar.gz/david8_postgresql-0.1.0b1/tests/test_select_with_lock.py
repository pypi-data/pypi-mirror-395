from parameterized import parameterized

from david8_postgresql.protocols.dml import SelectProtocol
from tests.base_test import BaseTest


class TestSelectWithLock(BaseTest):
    @parameterized.expand([
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_key_share(),
            'SELECT * FROM users LIMIT 1 FOR KEY SHARE',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_key_share_nw(),
            'SELECT * FROM users LIMIT 1 FOR KEY SHARE NOWAIT',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_key_share_sl(),
            'SELECT * FROM users LIMIT 1 FOR KEY SHARE SKIP LOCKED',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_share(),
            'SELECT * FROM users LIMIT 1 FOR SHARE',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_share_nw(),
            'SELECT * FROM users LIMIT 1 FOR SHARE NOWAIT',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_share_sl(),
            'SELECT * FROM users LIMIT 1 FOR SHARE SKIP LOCKED',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_update(),
            'SELECT * FROM users LIMIT 1 FOR UPDATE',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_update_nw(),
            'SELECT * FROM users LIMIT 1 FOR UPDATE NOWAIT',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_update_sl(),
            'SELECT * FROM users LIMIT 1 FOR UPDATE SKIP LOCKED',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_nk_update(),
            'SELECT * FROM users LIMIT 1 FOR NO KEY UPDATE',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_nk_update_nw(),
            'SELECT * FROM users LIMIT 1 FOR NO KEY UPDATE NOWAIT',
        ),
        (
            BaseTest.qb
            .select('*')
            .from_table('users')
            .limit(1)
            .for_nk_update_sl(),
            'SELECT * FROM users LIMIT 1 FOR NO KEY UPDATE SKIP LOCKED',
        ),
    ])
    def test_select_with_lock_mode(self, query: SelectProtocol, exp_sql: str):
        self.assertEqual(query.get_sql(), exp_sql)
