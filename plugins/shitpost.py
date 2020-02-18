import json
import random

import utils


async def shitpost(self, room, user, arg):
    if room is not None and not utils.is_voice(user):
        return

    message = utils.remove_accents(arg.strip())
    if len(message) > 50:
        await self.send_reply(room, user, "Testo troppo lungo")
        return

    text0 = ""
    text1 = ""
    text2 = ""

    if message == "":
        if not utils.is_private(self, room):
            return
        message = "SHITPOST"

    if not utils.is_private(self, room) and ("x" in message or "X" in message):
        message = "lolno"

    message = list(message)
    for i in message:
        if i in LETTERS:
            if text0 != "":
                text0 += " "
                text1 += " "
                text2 += " "
            text0 += LETTERS[i][0]
            text1 += LETTERS[i][1]
            text2 += LETTERS[i][2]

    html = '<pre style="margin: 0; overflow-x: auto">{}<br>{}<br>{}</pre>'

    await self.send_htmlbox(room, user, html.format(text0, text1, text2))


async def memes(self, room, user, arg):
    if room is None or not utils.is_private(self, room):
        return

    await self.send_message(room, random.choice(MEMES))


# fmt: off
LETTERS = {
    "a": [
        "┌─┐",
        "├─┤",
        "┴ ┴",
    ],
    "b": [
        "┌┐ ",
        "├┴┐",
        "└─┘",
    ],
    "c": [
        "┌─┐",
        "│  ",
        "└─┘",
    ],
    "d": [
        "┌┬┐",
        " ││",
        "─┴┘",
    ],
    "e": [
        "┌─┐",
        "├┤ ",
        "└─┘",
    ],
    "f": [
        "┌─┐",
        "├┤ ",
        "└  ",
    ],
    "g": [
        "┌─┐",
        "│ ┬",
        "└─┘",
    ],
    "h": [
        "┬ ┬",
        "├─┤",
        "┴ ┴",
    ],
    "i": [
        "┬",
        "│",
        "┴",
    ],
    "j": [
        " ┬",
        " │",
        "└┘",
    ],
    "k": [
        "┬┌─",
        "├┴┐",
        "┴ ┴",
    ],
    "l": [
        "┬  ",
        "│  ",
        "┴─┘",
    ],
    "m": [
        "┌┬┐",
        "│││",
        "┴ ┴",
    ],
    "n": [
        "┌┐┌",
        "│││",
        "┘└┘",
    ],
    "o": [
        "┌─┐",
        "│ │",
        "└─┘",
    ],
    "p": [
        "┌─┐",
        "├─┘",
        "┴  ",
    ],
    "q": [
        "┌─┐ ",
        "│─┼┐",
        "└─┘└",
    ],
    "r": [
        "┬─┐",
        "├┬┘",
        "┴└─",
    ],
    "s": [
        "┌─┐",
        "└─┐",
        "└─┘",
    ],
    "t": [
        "┌┬┐",
        " │ ",
        " ┴ ",
    ],
    "u": [
        "┬ ┬",
        "│ │",
        "└─┘",
    ],
    "v": [
        "┬  ┬",
        "└┐┌┘",
        " └┘ ",
    ],
    "w": [
        "┬ ┬",
        "│││",
        "└┴┘",
    ],
    "x": [
        "─┐ ┬",
        "┌┴┬┘",
        "┴ └─",
    ],
    "y": [
        "┬ ┬",
        "└┬┘",
        " ┴ ",
    ],
    "z": [
        "┌─┐",
        "┌─┘",
        "└─┘",
    ],
    "A": [
        "╔═╗",
        "╠═╣",
        "╩ ╩",
    ],
    "B": [
        "╔╗ ",
        "╠╩╗",
        "╚═╝",
    ],
    "C": [
        "╔═╗",
        "║  ",
        "╚═╝",
    ],
    "D": [
        "╔╦╗",
        " ║║",
        "═╩╝",
    ],
    "E": [
        "╔═╗",
        "╠╣ ",
        "╚═╝",
    ],
    "F": [
        "╔═╗",
        "╠╣ ",
        "╚  ",
    ],
    "G": [
        "╔═╗",
        "║ ╦",
        "╚═╝",
    ],
    "H": [
        "╦ ╦",
        "╠═╣",
        "╩ ╩",
    ],
    "I": [
        "╦",
        "║",
        "╩",
    ],
    "J": [
        " ╦",
        " ║",
        "╚╝",
    ],
    "K": [
        "╦╔═",
        "╠╩╗",
        "╩ ╩",
    ],
    "L": [
        "╦  ",
        "║  ",
        "╩═╝",
    ],
    "M": [
        "╔╦╗",
        "║║║",
        "╩ ╩",
    ],
    "N": [
        "╔╗╔",
        "║║║",
        "╝╚╝",
    ],
    "O": [
        "╔═╗",
        "║ ║",
        "╚═╝",
    ],
    "P": [
        "╔═╗",
        "╠═╝",
        "╩  ",
    ],
    "Q": [
        "╔═╗ ",
        "║═╬╗",
        "╚═╝╚",
    ],
    "R": [
        "╦═╗",
        "╠╦╝",
        "╩╚═",
    ],
    "S": [
        "╔═╗",
        "╚═╗",
        "╚═╝",
    ],
    "T": [
        "╔╦╗",
        " ║ ",
        " ╩ ",
    ],
    "U": [
        "╦ ╦",
        "║ ║",
        "╚═╝",
    ],
    "V": [
        "╦  ╦",
        "╚╗╔╝",
        " ╚╝ ",
    ],
    "W": [
        "╦ ╦",
        "║║║",
        "╚╩╝",
    ],
    "X": [
        "═╗ ╦",
        "╔╩╦╝",
        "╩ ╚═",
    ],
    "Y": [
        "╦ ╦",
        "╚╦╝",
        " ╩ ",
    ],
    "Z": [
        "╔═╗",
        "╔═╝",
        "╚═╝",
    ],
    "0": [
        "╔═╗",
        "║ ║",
        "╚═╝",
    ],
    "1": [
        "╗",
        "║",
        "╩",
    ],
    "2": [
        "╔═╗",
        "╔═╝",
        "╚═╝",
    ],
    "3": [
        "╔═╗",
        " ═╣",
        "╚═╝",
    ],
    "4": [
        "╦ ╦",
        "╚═╣",
        "  ╩",
    ],
    "5": [
        "╔═╗",
        "╚═╗",
        "╚═╝",
    ],
    "6": [
        "╔═╗",
        "╠═╗",
        "╚═╝",
    ],
    "7": [
        "═╗",
        " ║",
        " ╩",
    ],
    "8": [
        "╔═╗",
        "╠═╣",
        "╚═╝",
    ],
    "9": [
        "╔═╗",
        "╚═╣",
        "╚═╝",
    ],
    " ": [
        "  ",
        "  ",
        "  ",
    ],
    "!": [
        "║",
        "║",
        "▫",
    ],
    "\"": [
        "╚╚",
        "  ",
        "  ",
    ],
    "£": [
        "╔═╗",
        "╬═ ",
        "╩══",
    ],
    "$": [
        "╔╬╗",
        "╚╬╗",
        "╚╬╝",
    ],
    "%": [
        "▫ ╦ ",
        " ╔╝ ",
        " ╩ ▫",
    ],
    "\\": [
        "╦ ",
        "╚╗",
        " ╩",
    ],
    "(": [
        "╔",
        "║",
        "╚",
    ],
    ")": [
        "╗",
        "║",
        "╝",
    ],
    "=": [
        "  ",
        "══",
        "══",
    ],
    "\"": [
        "╚",
        " ",
        " ",
    ],
    "?": [
        "╔═╗",
        " ╔╝",
        " ▫ ",
    ],
    "/": [
        " ╦",
        "╔╝",
        "╩ ",
    ],
    "|": [
        "║",
        "║",
        "║",
    ],
    "-": [
        "  ",
        "══",
        "  ",
    ],
    "+": [
        " ║ ",
        "═╬═",
        " ║ ",
    ],
    ":": [
        "╗",
        " ",
        "╗",
    ],
    ".": [
        " ",
        " ",
        "╗",
    ],
    "_": [
        "   ",
        "   ",
        "═══",
    ],
    "[": [
        "╔",
        "║",
        "╚",
    ],
    "]": [
        "╗",
        "║",
        "╝",
    ],
    "{": [
        "╔",
        "╣",
        "╚",
    ],
    "}": [
        "╗",
        "╠",
        "╝",
    ],
    "#": [
        "  ",
        "╬╬",
        "╬╬",
    ],
    "~": [
        "   ",
        "╔═╝",
        "   ",
    ],
    ",": [
        " ",
        " ",
        "╗",
    ],
    ";": [
        "╗",
        " ",
        "╗",
    ],
    "°": [
        "┌┐",
        "└┘",
        "  ",
    ],
}
# fmt: on


with open("./data/memes.json", "r") as f:
    MEMES = json.load(f)


commands = {
    "meme": memes,
    "memes": memes,
    "mims": memes,
    "say": shitpost,
    "shitpost": shitpost,
}
