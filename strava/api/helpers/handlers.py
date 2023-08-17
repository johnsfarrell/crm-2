from django.http import JsonResponse
from strava.api.helpers.crud import _create, _read, _update, _delete


def generate_handlers(table, required_fields, optional_fields):
    def create(body):
        return create_handler(body, table, required_fields, optional_fields)

    def read(body):
        return read_handler(body, table)

    def update(body):
        return update_handler(body, table, required_fields, optional_fields)

    def delete(body):
        return delete_handler(body, table)

    return (create, read, update, delete)


def create_handler(body, table, required_fields, optional_fields):
    if not all([field in body for field in required_fields]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    contents = {
        field: body[field]
        for field in required_fields + optional_fields
        if field in body
    }

    res = _create(table, contents)

    return (
        JsonResponse({"res": res, "table": table, "contents": contents}, status=200)
        if res
        else JsonResponse({}, status=400)
    )


def read_handler(body, table):
    res = _read(table, body["id"] if "id" in body else None)

    if not res:
        return JsonResponse({}, status=400)

    return JsonResponse(res, status=200)


def update_handler(body, table, required_fields, optional_fields):
    if not all([field in body for field in required_fields]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    res = _update(
        table,
        body["id"],
        {
            field: body[field]
            for field in required_fields + optional_fields
            if field in body
        },
    )

    return JsonResponse(res, status=200) if res else JsonResponse({}, status=400)


def delete_handler(body, table):
    if "id" not in body:
        return JsonResponse({"error": "No id provided"}, status=400)

    res = _delete(table, body["id"])

    return JsonResponse(res, status=200) if res else JsonResponse({}, status=400)
