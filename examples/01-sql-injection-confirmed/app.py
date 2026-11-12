# Example code, written for this repository. A small search endpoint.
# The change under review added the keyword search below; it used to
# return the caller's own items only.

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB = sqlite3.connect("catalog.db", check_same_thread=False)


@app.get("/search")
def search_items():
    q = request.args.get("q", "")
    # NEW in this change: keyword search across the whole catalog.
    query = (
        "SELECT id, name, price FROM items "
        "WHERE name LIKE '%" + q + "%' AND discontinued = 0"
    )
    rows = DB.execute(query).fetchall()
    return jsonify([{"id": r[0], "name": r[1], "price": r[2]} for r in rows])


@app.get("/items/<int:item_id>")
def get_item(item_id):
    row = DB.execute(
        "SELECT id, name, price FROM items WHERE id = ?", (item_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": row[0], "name": row[1], "price": row[2]})
