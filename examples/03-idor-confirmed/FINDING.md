# Pass 1: finding

```
ID: F1
Class: authorization (IDOR)
Location: invoices.py, download_invoice()
Claim: Any logged-in user can download any invoice by changing the ID
  in the URL, because the handler checks that a user is logged in and
  never checks that the invoice belongs to them.
Flow: invoice_id from the URL -> db.get_invoice() -> send_file(pdf_path)
Preconditions: A valid account. Invoice IDs are sequential.
Evidence: The change adds the route with an authentication check only.
  The list route in the same file scopes its query by owner; the new
  route does not scope and does not compare owners.
Confidence: medium (the ownership check might live in db.get_invoice;
  not verified in this pass)
```
