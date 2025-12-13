import datetime
from sqlite3 import dbapi2 as sqlite


class GeoLookup:
    def __init__(self, path: str) -> None:
        if path is None:
            self.db = None
            return
        self.db = sqlite.connect(path)
        self.cursor = self.db.cursor()
        self.cache = {}
        self.query = '''
          SELECT country, datestamp FROM ipgeo
            WHERE ip_address = ?
            AND datestamp >= ?
            AND datestamp <= ?;
        '''
        self.prefix = 'urn:iso:std:3166:-2:'

    def lookup_country(self, ip_address: str, date: datetime) -> str:
        if self.db is None:
            return ''
        time_now = date.timestamp()
        time_max = time_now + 86400 * 180
        time_min = time_max - 86400 * 180
        args = (ip_address, time_min, time_max)
        self.cursor.execute(self.query, args)
        row = self.cursor.fetchone()
        if row is None:
            return ''
        return self.prefix + row[0]
