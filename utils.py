from __future__ import annotations

import os
import random
import re
import string
from html import escape
from typing import Any, Dict, Optional

import htmlmin  # type: ignore
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.sql import func

import databases.database as d
from database import Database
from typedefs import Role, RoomId, UserId


def create_token(
    rooms: Dict[str, str], expire_minutes: int = 30, admin: Optional[str] = None
) -> str:
    token_id = os.urandom(16).hex()
    expiry = f"+{expire_minutes} minute"

    values = []
    if admin is not None:
        values.append(
            d.Tokens(
                token=token_id,
                room=None,
                rank=admin,
                expiry=func.datetime("now", expiry),
            )
        )
    for room in rooms:
        values.append(
            d.Tokens(
                token=token_id,
                room=room,
                rank=rooms[room],
                expiry=func.datetime("now", expiry),
            )
        )

    db = Database.open()
    with db.get_session() as session:
        session.add_all(values)  # type: ignore  # sqlalchemy

    return token_id


def to_user_id(user: str) -> UserId:
    userid = UserId(re.sub(r"[^a-z0-9]", "", user.lower()))
    return userid


def to_room_id(room: str, fallback: RoomId = RoomId("lobby")) -> RoomId:
    roomid = RoomId(re.sub(r"[^a-z0-9-]", "", room.lower()))
    if not roomid:
        roomid = fallback
    return roomid


def remove_accents(text: str) -> str:
    text = re.sub(r"à", "a", text)
    text = re.sub(r"è|é", "e", text)
    text = re.sub(r"ì", "i", text)
    text = re.sub(r"ò", "o", text)
    text = re.sub(r"ù", "u", text)
    text = re.sub(r"À", "A", text)
    text = re.sub(r"È|É", "E", text)
    text = re.sub(r"Ì", "I", text)
    text = re.sub(r"Ò", "O", text)
    text = re.sub(r"Ù", "U", text)
    return text


def has_role(role: Role, user: str, strict_voice_check: bool = False) -> bool:
    """Checks if a user has a PS role or higher.

    Args:
        role (Role): PS role (i.e. "voice", "driver").
        user (str): User to check.
        strict_voice_check (bool): True if custom rank symbols should not be
            considered voice. Defaults to False.

    Returns:
        bool: True if user meets the required criteria.
    """
    roles: Dict[Role, str] = {
        "admin": "~&",
        "owner": "~&#",
        "bot": "*",
        "host": "★",
        "mod": "~&#@",
        "driver": "~&#@%",
        "player": "☆",
        "voice": "~&#@%+",
        "prizewinner": "^",
    }
    if user:
        if user[0] in roles[role]:
            return True
        if (
            role == "voice"
            and not strict_voice_check
            and user[0] not in "*★☆^ "
            and user[0] not in string.ascii_letters + string.digits
        ):
            return True
    return False


def html_escape(text: Optional[str]) -> str:
    if text is None:
        return ""
    return escape(text).replace("\n", "<br>")


def is_youtube_link(url: str) -> bool:
    """Returns True if url is a youtube link, based on PS' regex."""
    # Note: You should let PS display youtube links natively with "!show {url}".
    youtube_regex = r"^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)(\/|$)"
    return re.match(youtube_regex, url, re.IGNORECASE) is not None


def linkify(text: str) -> str:
    """Transforms a text containing URLs into HTML code.

    Args:
        text (str): Raw text.

    Returns:
        str: Escaped HTML, possibly containing <a> tags.
    """
    # Partially translated from https://github.com/smogon/pokemon-showdown, chat parser.
    # The original code is released under the MIT License.

    # linkify requires a custom translation table because "/" is left unescaped.
    table = {ord(char): escape(char) for char in "&<>\"'"}
    table[ord("\n")] = "<br>"
    text = text.translate(table)

    # pylint: disable=line-too-long
    url_regex = r'(?i)(?:(?:https?:\/\/[a-z0-9-]+(?:\.[a-z0-9-]+)*|www\.[a-z0-9-]+(?:\.[a-z0-9-]+)+|\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com?|org|net|edu|info|us|jp|[a-z]{2,3}(?=[:/])))(?::[0-9]+)?(?:\/(?:(?:[^\s()&<>]|&amp;|&quot;|\((?:[^\\s()<>&]|&amp;)*\))*(?:[^\s()[\]{}".,!?;:&<>*`^~\\]|\((?:[^\s()<>&]|&amp;)*\)))?)?|[a-z0-9.]+@[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,})(?![^ ]*&gt;)'
    return re.sub(url_regex, lambda m: _linkify_uri(m.group()), text)


def _linkify_uri(uri: str) -> str:
    # Partially translated from https://github.com/smogon/pokemon-showdown, chat parser.
    # The original code is released under the MIT License.

    if re.match(r"^[a-z0-9.]+@", uri, re.IGNORECASE):
        fulluri = f"mailto:{uri}"
    else:
        fulluri = re.sub(r"^([a-z]*[^a-z:])", r"http://\1", uri)
        if uri.startswith("https://docs.google.com/") or uri.startswith(
            "docs.google.com/"
        ):
            if uri.startswith("https"):
                uri = uri[8:]
            if uri.endswith("?usp=sharing") or uri.endswith("&usp=sharing"):
                uri = uri[:-12]
            if uri.endswith("#gid=0"):
                uri = uri[:-6]

            slash_index = uri.rindex("/")
            if len(uri) - slash_index > 18:
                slash_index = len(uri)
            if slash_index - 4 > 22:
                uri = (
                    uri[:19]
                    + '<small class="message-overflow">'
                    + uri[19 : slash_index - 4]
                    + "</small>"
                    + uri[slash_index - 4 :]
                )
    return f'<a href="{fulluri}">{uri}</a>'


def render_template(  # type: ignore[misc]  # allow any
    template_name: str, **template_vars: Any
) -> str:
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_name)
    html = template.render(**template_vars)
    return htmlmin.minify(html, convert_charrefs=False)  # type: ignore[no-any-return]


def to_obfuscated_html(text: Optional[str]) -> str:
    """Converts a string to HTML code and adds invisible obfuscation text."""
    if text is None:
        return ""

    obfuscated = ""
    for ch in text:
        obfuscated += html_escape(ch)
        randstr = ""
        for _ in range(random.randrange(3, 10)):
            randstr += random.choice(string.ascii_letters + string.digits)
        obfuscated += f'<span style="position: absolute; top: -999vh">{randstr}</span>'
    return obfuscated


def get_language_id(language_name: str) -> int:
    table = {
        # "Japanese": 1,
        # "Traditional Chinese": 4,
        "French": 5,
        "German": 6,
        "Spanish": 7,
        "Italian": 8,
        "English": 9,
        # "Simplified Chinese": 12,
    }
    if language_name in table:
        return table[language_name]
    return table["English"]  # Default to English if language is not available.


AVATAR_IDS: Dict[str, str] = {
    "1": "lucas",
    "2": "dawn",
    "3": "youngster-gen4",
    "4": "lass-gen4dp",
    "5": "camper",
    "6": "picnicker",
    "7": "bugcatcher",
    "8": "aromalady",
    "9": "twins-gen4dp",
    "10": "hiker-gen4",
    "11": "battlegirl-gen4",
    "12": "fisherman-gen4",
    "13": "cyclist-gen4",
    "14": "cyclistf-gen4",
    "15": "blackbelt-gen4dp",
    "16": "artist-gen4",
    "17": "pokemonbreeder-gen4",
    "18": "pokemonbreederf-gen4",
    "19": "cowgirl",
    "20": "jogger",
    "21": "pokefan-gen4",
    "22": "pokefanf-gen4",
    "23": "pokekid",
    "24": "youngcouple-gen4dp",
    "25": "acetrainer-gen4dp",
    "26": "acetrainerf-gen4dp",
    "27": "waitress-gen4",
    "28": "veteran-gen4",
    "29": "ninjaboy",
    "30": "dragontamer",
    "31": "birdkeeper-gen4dp",
    "32": "doubleteam",
    "33": "richboy-gen4",
    "34": "lady-gen4",
    "35": "gentleman-gen4dp",
    "36": "madame-gen4dp",
    "37": "beauty-gen4dp",
    "38": "collector",
    "39": "policeman-gen4",
    "40": "pokemonranger-gen4",
    "41": "pokemonrangerf-gen4",
    "42": "scientist-gen4dp",
    "43": "swimmer-gen4dp",
    "44": "swimmerf-gen4dp",
    "45": "tuber",
    "46": "tuberf",
    "47": "sailor",
    "48": "sisandbro",
    "49": "ruinmaniac",
    "50": "psychic-gen4",
    "51": "psychicf-gen4",
    "52": "gambler",
    "53": "guitarist-gen4",
    "54": "acetrainersnow",
    "55": "acetrainersnowf",
    "56": "skier",
    "57": "skierf-gen4dp",
    "58": "roughneck-gen4",
    "59": "clown",
    "60": "worker-gen4",
    "61": "schoolkid-gen4dp",
    "62": "schoolkidf-gen4",
    "63": "roark",
    "64": "barry",
    "65": "byron",
    "66": "aaron",
    "67": "bertha",
    "68": "flint",
    "69": "lucian",
    "70": "cynthia-gen4",
    "71": "bellepa",
    "72": "rancher",
    "73": "mars",
    "74": "galacticgrunt",
    "75": "gardenia",
    "76": "crasherwake",
    "77": "maylene",
    "78": "fantina",
    "79": "candice",
    "80": "volkner",
    "81": "parasollady-gen4",
    "82": "waiter-gen4dp",
    "83": "interviewers",
    "84": "cameraman",
    "85": "reporter",
    "86": "idol",
    "87": "cyrus",
    "88": "jupiter",
    "89": "saturn",
    "90": "galacticgruntf",
    "91": "argenta",
    "92": "palmer",
    "93": "thorton",
    "94": "buck",
    "95": "darach",
    "96": "marley",
    "97": "mira",
    "98": "cheryl",
    "99": "riley",
    "100": "dahlia",
    "101": "ethan",
    "102": "lyra",
    "103": "twins-gen4",
    "104": "lass-gen4",
    "105": "acetrainer-gen4",
    "106": "acetrainerf-gen4",
    "107": "juggler",
    "108": "sage",
    "109": "li",
    "110": "gentleman-gen4",
    "111": "teacher",
    "112": "beauty",
    "113": "birdkeeper",
    "114": "swimmer-gen4",
    "115": "swimmerf-gen4",
    "116": "kimonogirl",
    "117": "scientist-gen4",
    "118": "acetrainercouple",
    "119": "youngcouple",
    "120": "supernerd",
    "121": "medium",
    "122": "schoolkid-gen4",
    "123": "blackbelt-gen4",
    "124": "pokemaniac",
    "125": "firebreather",
    "126": "burglar",
    "127": "biker-gen4",
    "128": "skierf",
    "129": "boarder",
    "130": "rocketgrunt",
    "131": "rocketgruntf",
    "132": "archer",
    "133": "ariana",
    "134": "proton",
    "135": "petrel",
    "136": "eusine",
    "137": "lucas-gen4pt",
    "138": "dawn-gen4pt",
    "139": "madame-gen4",
    "140": "waiter-gen4",
    "141": "falkner",
    "142": "bugsy",
    "143": "whitney",
    "144": "morty",
    "145": "chuck",
    "146": "jasmine",
    "147": "pryce",
    "148": "clair",
    "149": "will",
    "150": "koga",
    "151": "bruno",
    "152": "karen",
    "153": "lance",
    "154": "brock",
    "155": "misty",
    "156": "ltsurge",
    "157": "erika",
    "158": "janine",
    "159": "sabrina",
    "160": "blaine",
    "161": "blue",
    "162": "red",
    "163": "red",
    "164": "silver",
    "165": "giovanni",
    "166": "unknownf",
    "167": "unknown",
    "168": "unknown",
    "169": "hilbert",
    "170": "hilda",
    "171": "youngster",
    "172": "lass",
    "173": "schoolkid",
    "174": "schoolkidf",
    "175": "smasher",
    "176": "linebacker",
    "177": "waiter",
    "178": "waitress",
    "179": "chili",
    "180": "cilan",
    "181": "cress",
    "182": "nurseryaide",
    "183": "preschoolerf",
    "184": "preschooler",
    "185": "twins",
    "186": "pokemonbreeder",
    "187": "pokemonbreederf",
    "188": "lenora",
    "189": "burgh",
    "190": "elesa",
    "191": "clay",
    "192": "skyla",
    "193": "pokemonranger",
    "194": "pokemonrangerf",
    "195": "worker",
    "196": "backpacker",
    "197": "backpackerf",
    "198": "fisherman",
    "199": "musician",
    "200": "dancer",
    "201": "harlequin",
    "202": "artist",
    "203": "baker",
    "204": "psychic",
    "205": "psychicf",
    "206": "cheren",
    "207": "bianca",
    "208": "plasmagrunt-gen5bw",
    "209": "n",
    "210": "richboy",
    "211": "lady",
    "212": "pilot",
    "213": "workerice",
    "214": "hoopster",
    "215": "scientistf",
    "216": "clerkf",
    "217": "acetrainerf",
    "218": "acetrainer",
    "219": "blackbelt",
    "220": "scientist",
    "221": "striker",
    "222": "brycen",
    "223": "iris",
    "224": "drayden",
    "225": "roughneck",
    "226": "janitor",
    "227": "pokefan",
    "228": "pokefanf",
    "229": "doctor",
    "230": "nurse",
    "231": "hooligans",
    "232": "battlegirl",
    "233": "parasollady",
    "234": "clerk",
    "235": "clerk-boss",
    "236": "backers",
    "237": "backersf",
    "238": "veteran",
    "239": "veteranf",
    "240": "biker",
    "241": "infielder",
    "242": "hiker",
    "243": "madame",
    "244": "gentleman",
    "245": "plasmagruntf-gen5bw",
    "246": "shauntal",
    "247": "marshal",
    "248": "grimsley",
    "249": "caitlin",
    "250": "ghetsis-gen5bw",
    "251": "depotagent",
    "252": "swimmer",
    "253": "swimmerf",
    "254": "policeman",
    "255": "maid",
    "256": "ingo",
    "257": "alder",
    "258": "cyclist",
    "259": "cyclistf",
    "260": "cynthia",
    "261": "emmet",
    "262": "hilbert-dueldisk",
    "263": "hilda-dueldisk",
    "264": "hugh",
    "265": "rosa",
    "266": "nate",
    "267": "colress",
    "268": "beauty-gen5bw2",
    "269": "ghetsis",
    "270": "plasmagrunt",
    "271": "plasmagruntf",
    "272": "iris-gen5bw2",
    "273": "brycenman",
    "274": "shadowtriad",
    "275": "rood",
    "276": "zinzolin",
    "277": "cheren-gen5bw2",
    "278": "marlon",
    "279": "roxie",
    "280": "roxanne",
    "281": "brawly",
    "282": "wattson",
    "283": "flannery",
    "284": "norman",
    "285": "winona",
    "286": "tate",
    "287": "liza",
    "288": "juan",
    "289": "guitarist",
    "290": "steven",
    "291": "wallace",
    "292": "bellelba",
    "293": "benga",
    "294": "ash",
    "#bw2elesa": "elesa-gen5bw2",
    "#teamrocket": "teamrocket",
    "#yellow": "yellow",
    "#zinnia": "zinnia",
    "#clemont": "clemont",
    "#wally": "wally",
    "breeder": "pokemonbreeder",
    "breederf": "pokemonbreederf",
    "1001": "#1001",
    "1002": "#1002",
    "1003": "#1003",
    "1005": "#1005",
    "1010": "#1010",
}
