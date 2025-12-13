from david8.protocols.dml import SelectProtocol as _SelectProtocol
from david8.protocols.dml import UpdateProtocol as _UpdateProtocol


class SelectProtocol(_SelectProtocol):
    def for_key_share(self) -> 'SelectProtocol':
        pass

    def for_key_share_nw(self) -> 'SelectProtocol':
        """
        FOR KEY SHARE NOWAIT
        """

    def for_key_share_sl(self) -> 'SelectProtocol':
        """
        FOR KEY SHARE SKIP LOCKED
        """

    def for_share(self) -> 'SelectProtocol':
        pass

    def for_share_nw(self) -> 'SelectProtocol':
        """
        FOR SHARE NOWAIT
        """

    def for_share_sl(self) -> 'SelectProtocol':
        """
        FOR SHARE SKIP LOCKED
        """

    def for_update(self) -> 'SelectProtocol':
        pass

    def for_update_nw(self) -> 'SelectProtocol':
        """
        FOR UPDATE NOWAIT
        """

    def for_update_sl(self) -> 'SelectProtocol':
        """
        FOR UPDATE SKIP LOCKED
        """

    def for_nk_update(self) -> 'SelectProtocol':
        """
        FOR NO KEY UPDATE
        """

    def for_nk_update_nw(self) -> 'SelectProtocol':
        """
        FOR NO KEY UPDATE NOWAIT
        """

    def for_nk_update_sl(self) -> 'SelectProtocol':
        """
        FOR NO KEY UPDATE SKIP LOCKED
        """

class UpdateProtocol(_UpdateProtocol):
    def returning(self, *args: str) -> 'UpdateProtocol':
        pass

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> 'UpdateProtocol':
        pass
