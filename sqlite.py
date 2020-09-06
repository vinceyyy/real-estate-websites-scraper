import sqlite3


class DataRow:
    """One row of dict data: {"name": name, "address": address, "area": area, "type": typ,
                    "units": units, "year": year, "developer": dev, "agency": agency}
    """
    def __init__(self, datarow):
        self.name = datarow["name"]
        self.address = datarow["address"]
        self.area = datarow["area"]
        self.type = datarow["type"]
        self.units = datarow["units"]
        self.year = datarow["year"]
        self.developer = datarow["developer"]
        self.agency = datarow["agency"]

    def write_sqlite(self, database):
        """Write one row of dict data into sqlite database.

        Args:
            database (string): name of target database, will create one if no exists
        """
        self.database = database
        with sqlite3.connect(f"{self.database}.sqlite") as conn:
            cur = conn.cursor()

            # setup
            cur.executescript('''
            CREATE TABLE IF NOT EXISTS Area (
                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                area    TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS Type (
                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                type    TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS Developer (
                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                developer    TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS Agency (
                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                agency    TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS Building (
                id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name        TEXT UNIQUE,
                address     TEXT,
                units       INTEGER,
                year        INTEGER,
                area_id     INTEGER,
                developer_id        INTEGER,    
                type_id     INTEGER,
                agency_id      INTEGER,
                FOREIGN KEY (area_id) REFERENCES Area(id),
                FOREIGN KEY (developer_id) REFERENCES Developer(id),
                FOREIGN KEY (type_id) REFERENCES Type(id),
                FOREIGN KEY (agency_id) REFERENCES Agency(id)
            )
            ''')

            cur.execute('''INSERT OR IGNORE INTO Area (area)
            VALUES ( ? )''', (self.area, ))
            cur.execute('SELECT id FROM Area WHERE area = ? ', (self.area, ))
            area_id = cur.fetchone()[0]

            cur.execute('''INSERT OR IGNORE INTO Type (type)
            VALUES ( ? )''', (self.type, ))
            cur.execute('SELECT id FROM Type WHERE type = ? ', (self.type, ))
            type_id = cur.fetchone()[0]

            cur.execute('''INSERT OR IGNORE INTO Developer (developer)
            VALUES ( ? )''', (self.developer, ))
            cur.execute('SELECT id FROM Developer WHERE developer = ? ',
                        (self.developer, ))
            developer_id = cur.fetchone()
            if developer_id is not None:
                developer_id = developer_id[0]

            cur.execute('''INSERT OR IGNORE INTO Agency (agency)
            VALUES ( ? )''', (self.agency, ))
            cur.execute('SELECT id FROM Agency WHERE agency = ? ',
                        (self.agency, ))
            agency_id = cur.fetchone()
            if agency_id is not None:
                agency_id = agency_id[0]

            cur.execute('''INSERT OR REPLACE INTO Building
            (name, address, units, year, area_id, developer_id, type_id, agency_id) VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )''',
                        (self.name, self.address, self.units, self.year, area_id, developer_id, type_id, agency_id))

            
    def commit_sqlite(self, database):
        self.database = database
        with sqlite3.connect(f"{self.database}.sqlite") as conn:
            cur = conn.cursor()
            conn.commit()
