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

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from merch_game.apis import pages, tokens


def include_router(application):
    application.include_router(pages.pages_router)
    application.include_router(tokens.tokens_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="templates"), name="static")
    app.mount("/images", StaticFiles(directory="static/images"), name="images")


def start_application():
    application = FastAPI(title="OpenInfra Sunbeam Merch Game", version="0.1")
    include_router(application)
    configure_static(application)
    return application


app = start_application()


@app.get("/version")
async def root():
    return {"version": 0.1}
