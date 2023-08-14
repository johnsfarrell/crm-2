from crm.settings import db
from strava.utils import create_id


def _read(col: str, id: str) -> dict or None:
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


def _create(col: str, body) -> bool:
    try:
        db.child(col).child(create_id()).set(body)
        return True
    except:
        return False
