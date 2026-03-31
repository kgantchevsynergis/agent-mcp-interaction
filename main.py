import sqlite3
import json
from fastmcp import FastMCP

DB_PATH = "geo.db"
mcp = FastMCP("Kalo's MCP")

@mcp.tool
def get_points():
    """Return all saved points of interest with name, coordinates, and category."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT name, lat, lng, category FROM points").fetchall()
    conn.close()
    return json.dumps([dict(r) for r in rows])

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8472)
    
    # debug print for real mcp server mcp inspector is waht you want to use but for this test its okay.
    # print(get_points())

