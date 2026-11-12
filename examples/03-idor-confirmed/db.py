# Example data layer, written for this repository. The queries below
# are the ones the disproof pass read: get_invoice() fetches by ID
# alone, with no owner column in the WHERE clause, while
# invoices_for_owner() scopes its query by owner.

import sqlite3
from types import SimpleNamespace

DB = sqlite3.connect("invoices.db", check_same_thread=False)
DB.row_factory = sqlite3.Row


def _row_to_object(row):
    if row is None:
        return None
    return SimpleNamespace(**dict(row))


def get_user(user_id):
    row = DB.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    return _row_to_object(row)


def get_invoice(invoice_id):
    row = DB.execute(
        "SELECT * FROM invoices WHERE id = ?", (invoice_id,)
    ).fetchone()
    return _row_to_object(row)


def invoices_for_owner(owner_id):
    rows = DB.execute(
        "SELECT * FROM invoices WHERE owner_id = ?", (owner_id,)
    ).fetchall()
    return [_row_to_object(row) for row in rows]
