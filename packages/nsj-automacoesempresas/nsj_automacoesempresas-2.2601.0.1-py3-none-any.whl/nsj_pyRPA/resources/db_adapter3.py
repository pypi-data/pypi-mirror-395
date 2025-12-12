
from nsj_gcf_utils.db_adapter2 import DBAdapter2
from sqlalchemy import Table, insert

class DBAdapter3(DBAdapter2):
    def __init__(self, db_connection):
        super().__init__(db_connection)


    def executemany(self, modela_tabela : Table, records_for_insert: list) :
        cur = None
        try:
            cur = self._db.execute(insert(modela_tabela), records_for_insert)
            return cur.rowcount
        finally:
            if cur is not None:
                cur.close()