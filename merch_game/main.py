#
# Copyright 2023, Canonical Ltd.
#

import random

from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from pathlib import Path


class Token(BaseModel):
    value: str


app = FastAPI()

AVAIL_TOKENS_FILE = Path('avail-tokens.txt')
AVAIL_TOKENS = list()

USED_TOKENS_FILE = Path('used-tokens.txt')
USED_TOKENS = list()


# Generate a set of new tokens available for use
if not AVAIL_TOKENS_FILE.exists():
    with open(AVAIL_TOKENS_FILE, 'w+') as f:
        for i in range(0, 1000):
            token = str(uuid4())[:8]
            f.write(f"{token}\n")
            AVAIL_TOKENS.append(token)
else:
    with open(AVAIL_TOKENS_FILE, 'r') as f:
        for line in f.readlines():
            AVAIL_TOKENS.append(line.strip())


# Load any used tokens
if USED_TOKENS_FILE.exists():
    with open(USED_TOKENS_FILE, 'r') as f:
        for line in f.readlines():
            USED_TOKENS.append(line.strip())


@app.get('/')
async def root():
    return {"version": 0.1}


@app.post('/token')
def create_token() -> Token:
    """Generates a new token to hand out for the game.

    A token is allocated for the request and returned to
    the user in order to use a game.

    :return: a game Token that is valid for redemption
    """
    token = Token(value=str(random.choice(AVAIL_TOKENS)))
    with open(USED_TOKENS_FILE, 'w+') as f:
        f.write(f"{token.value}\n")
        USED_TOKENS.append(token.value)

    return token


@app.get('/validate/{token}')
def validate_token(token: str):
    """Validates the provided token

    Validates the provided token and determines whether
    it is a valid token or not

    :param token: the token to validate
    :return: a json value if the token is valid
    """
    return {"valid": token in USED_TOKENS}
