from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import TYPE_CHECKING

import utils
from handlers import handler_wrapper

if TYPE_CHECKING:
    from connection import Connection


@handler_wrapper(["challstr"])
async def challstr(conn: Connection, roomid: str, *args: str) -> None:
    if len(args) < 1:
        return

    challstring = "|".join(args)

    payload = (
        "act=login&"
        f"name={conn.username}"
        f"&pass={conn.password}"
        f"&challstr={challstring}"
    ).encode()

    req = urllib.request.Request(
        "https://play.pokemonshowdown.com/action.php",
        payload,
        {"User-Agent": "Mozilla"},
    )
    resp = urllib.request.urlopen(req)

    assertion = json.loads(resp.read().decode("utf-8")[1:])["assertion"]

    if assertion:
        await conn.send_message("", f"/trn {conn.username},0,{assertion}", False)


@handler_wrapper(["updateuser"])
async def updateuser(conn: Connection, roomid: str, *args: str) -> None:
    if len(args) < 4:
        return

    user = args[0]
    # named = args[1]
    avatar = args[2]
    # settings = args[3]

    username = user.split("@")[0]
    if utils.to_user_id(username) != utils.to_user_id(conn.username):
        return

    if conn.avatar and avatar != conn.avatar:
        await conn.send_message("", f"/avatar {conn.avatar}", False)

    if conn.statustext:
        await conn.send_message("", f"/status {conn.statustext}", False)

    for public_room in conn.rooms:
        await conn.send_message("", f"/join {public_room}", False)

    for private_room in conn.private_rooms:
        await conn.send_message("", f"/join {private_room}", False)
