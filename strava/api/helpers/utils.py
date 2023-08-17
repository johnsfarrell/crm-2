import random


def create_id():
    return random.randint(1, 1000000000)


def bearer(token):
    return f"Bearer {token}"
