# Copyright (c) 2023 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from pydantic import BaseModel
from fastapi import APIRouter
from uuid import uuid4
from pathlib import Path


class Token(BaseModel):
    value: str


tokens_router = APIRouter()

AVAIL_TOKENS_FILE = Path('avail-tokens.txt')
AVAIL_TOKENS = list()

USED_TOKENS_FILE = Path('used-tokens.txt')
USED_TOKENS = list()


# Generate a set of new tokens available for use
if not AVAIL_TOKENS_FILE.exists():
    with open(AVAIL_TOKENS_FILE, 'a') as f:
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


# @app.get('/')
# async def root():
#     return {"version": 0.1}

@tokens_router.post('/token')
def create_token() -> Token:
    """Generates a new token to hand out for the game.

    A token is allocated for the request and returned to
    the user in order to use a game.

    :return: a game Token that is valid for redemption
    """
    token = Token(value=str(random.choice(AVAIL_TOKENS)))
    with open(USED_TOKENS_FILE, 'a') as f:
        f.write(f"{token.value}\n")
        USED_TOKENS.append(token.value)

    return token


@tokens_router.get('/validate/{token}')
def validate_token(token: str):
    """Validates the provided token

    Validates the provided token and determines whether
    it is a valid token or not

    :param token: the token to validate
    :return: a json value if the token is valid
    """
    return {"valid": token in USED_TOKENS}
