# Example code, written for this repository. Invoice downloads in a
# small billing app. The change under review added the download route.

from flask import Flask, session, abort, send_file
import db

app = Flask(__name__)


def current_user():
    uid = session.get("user_id")
    if uid is None:
        abort(401)
    return db.get_user(uid)


@app.get("/invoices/<int:invoice_id>/download")
def download_invoice(invoice_id):
    user = current_user()  # logged in: yes. Entitled to this invoice: unchecked.
    invoice = db.get_invoice(invoice_id)
    if invoice is None:
        abort(404)
    return send_file(invoice.pdf_path)


@app.get("/invoices")
def list_invoices():
    user = current_user()
    # The list route scopes by owner in the query itself.
    return {"invoices": [i.id for i in db.invoices_for_owner(user.id)]}
