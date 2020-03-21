from typing import Optional

import utils

import database


async def create_tour(
    self,
    room: str,
    *,
    formatid: str = "customgame",
    generator: str = "elimination",
    playercap: Optional[int] = None,
    generatormod: str = "",
    name: str = "",
    autostart: float = 2,
    autodq: float = 1.5,
    allow_scouting: bool = False,
    rules=[]
) -> None:
    tournew = "/tour new {formatid}, {generator}, {playercap}, {generatormod}, {name}"
    await self.send_message(
        room,
        tournew.format(
            formatid=formatid,
            generator=generator,
            playercap=str(playercap) if playercap else "",
            generatormod=generatormod,
            name=name,
        ),
    )
    if autostart is not None:
        await self.send_message(room, "/tour autostart {}".format(autostart))
    if autodq is not None:
        await self.send_message(room, "/tour autodq {}".format(autodq))
    if not allow_scouting:
        await self.send_message(room, "/tour scouting off")
    if rules:
        await self.send_message(room, "/tour rules {}".format(",".join(rules)))


async def randpoketour(self, room: str, user: str, arg: str) -> None:
    if room is None or not utils.is_driver(user):
        return

    if arg.strip() == "":
        return await self.send_message(room, "Inserisci almeno un Pokémon")

    megas = [
        "abomasnow",
        "absol",
        "aerodactyl",
        "aggron",
        "alakazam",
        "altaria",
        "ampharos",
        "audino",
        "banette",
        "beedrill",
        "blastoise",
        "blaziken",
        "camerupt",
        "diancie",
        "gallade",
        "garchomp",
        "gardevoir",
        "gengar",
        "glalie",
        "gyarados",
        "heracross",
        "houndoom",
        "kangaskhan",
        "latias",
        "latios",
        "lopunny",
        "lucario",
        "manectric",
        "mawile",
        "medicham",
        "metagross",
        "pidgeot",
        "pinsir",
        "rayquaza",
        "sableye",
        "salamence",
        "sceptile",
        "scizor",
        "sharpedo",
        "slowbro",
        "steelix",
        "swampert",
        "tyranitar",
        "venusaur",
    ]
    megas_xy = ["charizard", "mewtwo"]
    megastones = [
        "Abomasite",
        "Absolite",
        "Aerodactylite",
        "Aggronite",
        "Alakazite",
        "Altarianite",
        "Ampharosite",
        "Audinite",
        "Banettite",
        "Beedrillite",
        "Blastoisinite",
        "Blazikenite",
        "Cameruptite",
        "Charizardite X",
        "Charizardite Y",
        "Crucibellite",
        "Diancite",
        "Galladite",
        "Garchompite",
        "Gardevoirite",
        "Gengarite",
        "Glalitite",
        "Gyaradosite",
        "Heracronite",
        "Houndoominite",
        "Kangaskhanite",
        "Latiasite",
        "Latiosite",
        "Lopunnite",
        "Lucarionite",
        "Manectite",
        "Mawilite",
        "Medichamite",
        "Metagrossite",
        "Mewtwonite X",
        "Mewtwonite Y",
        "Pidgeotite",
        "Pinsirite",
        "Sablenite",
        "Salamencite",
        "Sceptilite",
        "Scizorite",
        "Sharpedonite",
        "Slowbronite",
        "Steelixite",
        "Swampertite",
        "Tyranitarite",
        "Venusaurite",
    ]

    formatid = "nationaldex"
    name = "!RANDPOKE TOUR"
    rules = []
    bans = ["All Pokemon"]
    unbans = []
    if "," in arg:
        sep = ","
    else:
        sep = " "
    allow_megas = True
    for item in arg.split(sep):
        if utils.to_user_id(item) in ["nomega", "nomegas"]:
            allow_megas = False
            name += " (no mega)"
            continue
        unbans.append(item.strip() + "-base")

    if allow_megas:
        for item in arg.split(sep):
            if utils.to_user_id(item) in megas:
                unbans.append(item.strip() + "-Mega-base")
            if utils.to_user_id(item) in megas_xy:
                unbans.append(item.strip() + "-Mega-X-base")
                unbans.append(item.strip() + "-Mega-Y-base")
    else:
        bans.extend(megastones)

    rules.extend(["-" + i for i in bans])
    rules.extend(["+" + i for i in unbans])

    await create_tour(
        self, room, formatid=formatid, name=name, autostart=12, rules=rules
    )


commands = {"randpoketour": randpoketour}
