from crm.settings import db
from strava.api.helpers.utils import create_id


def _create(col: str, body) -> bool:
    try:
        db.child(col).child(body["id"] if "id" in body else create_id()).set(body)
        return True
    except:
        return False


def _read(col: str, id: str) -> dict or None:
    if not id:
        docs = db.child(col).get()
        return docs.val()
    doc = db.child(col).child(id).get()
    return doc.val()


def _update(col: str, id: str, body) -> bool:
    try:
        db.child(col).child(id).update(body)
        return True
    except:
        return False


def _delete(col: str, id: str) -> bool:
    try:
        db.child(col).child(id).remove()
        return True
    except:
        return False
