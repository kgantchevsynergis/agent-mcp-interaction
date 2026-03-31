import sqlite3
import json

DB_PATH = "geo.db"

def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS points (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            lat         REAL NOT NULL,
            lng         REAL NOT NULL,
            category    TEXT,
            properties  TEXT DEFAULT '{}',
            created_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS routes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            wkt         TEXT NOT NULL,
            distance_m  REAL,
            category    TEXT,
            properties  TEXT DEFAULT '{}',
            created_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS zones (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            wkt         TEXT NOT NULL,
            area_m2     REAL,
            category    TEXT,
            properties  TEXT DEFAULT '{}',
            created_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_points_lat_lng  ON points (lat, lng);
        CREATE INDEX IF NOT EXISTS idx_points_category ON points (category);
        CREATE INDEX IF NOT EXISTS idx_routes_category ON routes (category);
        CREATE INDEX IF NOT EXISTS idx_zones_category  ON zones (category);
    """)

def seed_data(conn: sqlite3.Connection) -> None:
    # --- Points (Vienna landmarks) ---
    points = [
        ("Stephansdom",        48.2085, 16.3731, "landmark",  {"wiki": "Stephansdom"}),
        ("Prater Riesenrad",   48.2167, 16.3963, "landmark",  {"year_built": 1897}),
        ("Naschmarkt",         48.1994, 16.3663, "market",    {"open": "Mon-Sat"}),
        ("Hauptbahnhof",       48.1851, 16.3762, "transport", {"type": "railway"}),
        ("Westbahnhof",        48.1966, 16.3388, "transport", {"type": "railway"}),
        ("Karlsplatz",         48.2005, 16.3695, "transport", {"type": "metro_hub"}),
    ]
    conn.executemany(
        "INSERT INTO points (name, lat, lng, category, properties) VALUES (?,?,?,?,?)",
        [(n, la, lo, cat, json.dumps(p)) for n, la, lo, cat, p in points],
    )

    # --- Routes (WKT LINESTRING — coordinates are lng lat) ---
    routes = [
        (
            "Ring Road",
            "LINESTRING(16.3563 48.2032, 16.3620 48.2008, 16.3695 48.2005, 16.3762 48.2023, 16.3800 48.2058)",
            3200,
            "road",
            {"lanes": 4},
        ),
        (
            "U1 Metro Line",
            "LINESTRING(16.3762 48.1851, 16.3731 48.1984, 16.3695 48.2005, 16.3720 48.2133, 16.3742 48.2310)",
            8500,
            "metro",
            {"line": "U1"},
        ),
        (
            "Donaukanal Path",
            "LINESTRING(16.3800 48.1950, 16.3840 48.2020, 16.3880 48.2100, 16.3920 48.2180)",
            4100,
            "cycling",
            {"surface": "asphalt"},
        ),
    ]
    conn.executemany(
        "INSERT INTO routes (name, wkt, distance_m, category, properties) VALUES (?,?,?,?,?)",
        [(n, w, d, cat, json.dumps(p)) for n, w, d, cat, p in routes],
    )

    # --- Zones (WKT POLYGON — coordinates are lng lat, first = last to close) ---
    zones = [
        (
            "Innere Stadt (1st district)",
            "POLYGON((16.3580 48.2000, 16.3800 48.2000, 16.3800 48.2150, 16.3580 48.2150, 16.3580 48.2000))",
            None,
            "district",
            {"bezirk": 1},
        ),
        (
            "Prater Park",
            "POLYGON((16.3900 48.1980, 16.4200 48.1980, 16.4200 48.2300, 16.3900 48.2300, 16.3900 48.1980))",
            None,
            "park",
            {"green": True},
        ),
        (
            "Airport Noise Zone",
            "POLYGON((16.5500 48.1000, 16.6000 48.1000, 16.6000 48.1500, 16.5500 48.1500, 16.5500 48.1000))",
            None,
            "restriction",
            {"max_db": 65},
        ),
    ]
    conn.executemany(
        "INSERT INTO zones (name, wkt, area_m2, category, properties) VALUES (?,?,?,?,?)",
        [(n, w, a, cat, json.dumps(p)) for n, w, a, cat, p in zones],
    )

if __name__ == "__main__":
    with sqlite3.connect(DB_PATH) as conn:
        init_db(conn)
        seed_data(conn)
        print(f"Database ready: {DB_PATH}")
        print(f"  points : {conn.execute('SELECT COUNT(*) FROM points').fetchone()[0]}")
        print(f"  routes : {conn.execute('SELECT COUNT(*) FROM routes').fetchone()[0]}")
        print(f"  zones  : {conn.execute('SELECT COUNT(*) FROM zones').fetchone()[0]}")
