from __future__ import annotations

import random
from datetime import datetime
from typing import TYPE_CHECKING

import pytz

from plugins import command_wrapper

if TYPE_CHECKING:
    from models.message import Message


@command_wrapper()
async def acher(msg: Message) -> None:
    await msg.reply("lo acher che bontà ♫")


@command_wrapper(aliases=("aeth", "eterno"))
async def aethernum(msg: Message) -> None:
    await msg.reply("__eterno__ indeciso :^)")


@command_wrapper(aliases=("alphawittem", "wittem"))
async def alpha(msg: Message) -> None:
    await msg.reply("Italian luck jajaja")


@command_wrapper(aliases=("acii",))
async def altcauseiminsecure(msg: Message) -> None:
    await msg.reply(
        (
            "A, wi, we. La fortuna viene a me. "
            "Wi, we, wa. La fortuna viene qua. "
            "A, we, wi. La fortuna non va lì"
        )
    )


@command_wrapper()
async def annika(msg: Message) -> None:
    if msg.room is None or not msg.room.is_private:
        return

    await msg.reply("enjoy ur italian joke punishment room")


@command_wrapper()
async def azyzyz(msg: Message) -> None:
    text = "CAIO AZ" + "YZ" * random.randint(1, 5)
    await msg.reply(text)


@command_wrapper()
async def ciarizardmille(msg: Message) -> None:
    user = random.choice(
        [
            "duck",
            "test2017",
            "parnassius",
            "parna",
            "inflikted",
            "infli",
            "trev",
            "silver97",
            "silver",
            "usy",
            "useless trainer",
        ]
    )
    text = f"beh comunque ormai lo avete capito che sono un alt di {user}"
    await msg.reply(text)


@command_wrapper(aliases=("cinse", "cobse", "conse"))
async def consecutio(msg: Message) -> None:
    text = "opss{} ho lasciato il pc acceso tutta notte".format(
        "s" * random.randint(0, 3)
    )
    await msg.reply(text)


@command_wrapper()
async def duck(msg: Message) -> None:
    await msg.reply("quack")


@command_wrapper(aliases=("ed",))
async def edgummet(msg: Message) -> None:
    await msg.reply("soccontro")


@command_wrapper(aliases=("francy",))
async def francyy(msg: Message) -> None:
    await msg.reply("aiuto ho riso irl")


@command_wrapper()
async def haund(msg: Message) -> None:
    await msg.reply("( ͡° ͜ʖ ͡°)")


@command_wrapper()
async def howkings(msg: Message) -> None:
    await msg.reply("Che si vinca o si perda, v0lca merda :3")


@command_wrapper(aliases=("infli",))
async def inflikted(msg: Message) -> None:
    letters = {1: "I", 2: "N", 3: "F", 4: "L", 5: "I", 6: "K", 7: "T", 8: "E", 9: "D"}
    shuffled = sorted(letters, key=lambda x: random.random() * x / len(letters))
    text = ""
    for i in shuffled:
        text += letters[i]
    await msg.reply(f"ciao {text}")


@command_wrapper()
async def lange(msg: Message) -> None:
    await msg.reply("Haund mi traduci questo post?")


@command_wrapper()
async def mammalu(msg: Message) -> None:
    await msg.reply("clicca la stab")


@command_wrapper()
async def maurizio(msg: Message) -> None:
    await msg.reply("MAURIZIO used ICE PUNCH!")


@command_wrapper(aliases=("gr",))
async def megagr(msg: Message) -> None:
    await msg.reply("GRRRRRR")


@command_wrapper()
async def milak(msg: Message) -> None:
    await msg.reply("I just salmonella gurl")


@command_wrapper()
async def mister(msg: Message) -> None:
    await msg.reply("Master")


@command_wrapper()
async def mistercantiere(msg: Message) -> None:
    await msg.reply("MasterCantiere")


@command_wrapper(aliases=("azyz",))
async def oizys(msg: Message) -> None:
    await msg.reply("no")


@command_wrapper(aliases=("parna", "pota"))
async def parnassius(msg: Message) -> None:
    await msg.reply("allora, intanto ti calmi")


@command_wrapper(aliases=("palt0", "palto", "plato"))
async def plat0(msg: Message) -> None:
    text = "oh {} non mi spoilerare".format(
        random.choice(["basta", "senti", "smettila"])
    )
    tz = pytz.timezone("Europe/Rome")
    timestamp = datetime.now(tz)
    if 3 <= timestamp.hour <= 5:
        text += ", che mi sono appena svegliato"
    await msg.reply(text)


@command_wrapper(aliases=("rospe",))
async def r0spe(msg: Message) -> None:
    await msg.reply("buondì")


@command_wrapper(aliases=("boiler",))
async def roiler(msg: Message) -> None:
    await msg.reply("ehm volevo dire")


@command_wrapper(aliases=("silver",))
async def silver97(msg: Message) -> None:
    tier = random.choice(msg.conn.tiers)["name"]
    await msg.reply(f"qualcuno mi passa un team {tier}")


@command_wrapper()
async def smilzo(msg: Message) -> None:
    await msg.reply("mai na gioia")


@command_wrapper(aliases=("spec",))
async def specn(msg: Message) -> None:
    await msg.reply("Vi muto tutti")


@command_wrapper(aliases=("cul1", "culone", "kul1", "swcul1", "swkul1"))
async def swculone(msg: Message) -> None:
    await msg.reply("hue")


@command_wrapper(aliases=("quas",))
async def thequasar(msg: Message) -> None:
    await msg.reply("Basta con le pupazzate")


@command_wrapper(aliases=("3v", "vvv"))
async def trev(msg: Message) -> None:
    await msg.reply("gioco di merda")


@command_wrapper()
async def ultrasuca(msg: Message) -> None:
    await msg.reply("@Ultrasuca left")


@command_wrapper(aliases=("useless", "usy"))
async def uselesstrainer(msg: Message) -> None:
    await msg.reply("kek")


@command_wrapper(aliases=("volca",))
async def v0lca(msg: Message) -> None:
    await msg.reply("Porco mele...")
