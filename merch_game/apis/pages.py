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

from typing import Union

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from merch_game.apis.tokens import validate_token

templates = Jinja2Templates(directory="templates")
pages_router = APIRouter()


@pages_router.get("/")
async def home(request: Request, token: Union[str, None] = None):
    valid = False
    if token:
        data = validate_token(token)
        valid = data.get("valid", False)

    return templates.TemplateResponse(
        "pages/homepage.html", {"request": request, "token": token, "valid": valid}
    )
