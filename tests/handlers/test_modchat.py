from models.room import Room


def test_modchat(mock_connection) -> None:
    conn, queue = mock_connection()

    queue.add_messages(
        [
            ">room1",
            "|init|chat",
            "|title|Room 1",
            "|users|1,*cerbottana",
            "|:|1500000000",
        ]
    )

    room1 = Room.get(conn, "room1")

    # by default no_mods_online is None
    assert room1.no_mods_online is None

    # a mod enters the room, no_mods_online should still be None
    queue.add_messages(
        [
            ">room1",
            "|j|@mod",
        ],
        [
            "|queryresponse|userdetails|{"
            + "  "
            + '  "id": "mod",'
            + '  "userid": "mod",'
            + '  "name": "mod",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "@room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online is None

    # a regular user joins then leaves the room, no_mods_online should still be None
    queue.add_messages(
        [
            ">room1",
            "|j| reg",
        ],
        [
            "|queryresponse|userdetails|{"
            + '  "id": "reg",'
            + '  "userid": "reg",'
            + '  "name": "reg",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online is None
    queue.add_messages(
        [
            ">room1",
            "|l|reg",
        ]
    )
    assert room1.no_mods_online is None

    # another mod enters the room, no_mods_online should still be None
    queue.add_messages(
        [
            ">room1",
            "|j|@mod2",
        ],
        [
            "|queryresponse|userdetails|{"
            + '  "id": "mod2",'
            + '  "userid": "mod2",'
            + '  "name": "mod2",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "@room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online is None

    # mod2 leaves the room, no_mods_online should still be None
    queue.add_messages(
        [
            ">room1",
            "|l|mod2",
        ]
    )
    assert room1.no_mods_online is None

    # the first mod leaves the room as well, no_mods_online should no longer be None
    queue.add_messages(
        [
            ">room1",
            "|l|mod",
        ]
    )
    assert room1.no_mods_online is not None
    time = room1.no_mods_online

    # another regular user joins then leaves the room, no_mods_online shouldn't change
    queue.add_messages(
        [
            ">room1",
            "|j| reg2",
        ],
        [
            "|queryresponse|userdetails|{"
            + '  "id": "reg2",'
            + '  "userid": "reg2",'
            + '  "name": "reg2",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online == time
    queue.add_messages(
        [
            ">room1",
            "|l|reg2",
        ]
    )
    assert room1.no_mods_online == time

    # a mod comes back then leaves again, no_mods_online should be different
    queue.add_messages(
        [
            ">room1",
            "|j|@mod",
        ],
        [
            "|queryresponse|userdetails|{"
            + '  "id": "mod",'
            + '  "userid": "mod",'
            + '  "name": "mod",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "@room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online is None
    queue.add_messages(
        [
            ">room1",
            "|l|mod",
        ]
    )
    assert room1.no_mods_online is not None
    assert room1.no_mods_online != time

    # a mod under alt joins the room
    queue.add_messages(
        [
            ">room1",
            "|j|modalt",
        ],
        [
            "|queryresponse|userdetails|{"
            + '  "id": "modalt",'
            + '  "userid": "modalt",'
            + '  "name": "modalt",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online is not None

    # then changes name
    queue.add_messages(
        [
            ">room1",
            "|n|@mod|modalt",
        ],
        [
            "|queryresponse|userdetails|{"
            + '  "id": "mod",'
            + '  "userid": "mod",'
            + '  "name": "mod",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "@room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online is None

    # then changes name again
    queue.add_messages(
        [
            ">room1",
            "|n| modalt|mod",
        ],
        [
            "|queryresponse|userdetails|{"
            + '  "id": "modalt",'
            + '  "userid": "modalt",'
            + '  "name": "modalt",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online is not None

    # same as before, but while another mod is online
    queue.add_messages(
        [
            ">room1",
            "|j|@mod2",
        ],
        [
            "|queryresponse|userdetails|{"
            + '  "id": "mod2",'
            + '  "userid": "mod2",'
            + '  "name": "mod2",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "@room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online is None

    queue.add_messages(
        [
            ">room1",
            "|n|@mod|modalt",
        ],
        [
            "|queryresponse|userdetails|{"
            + '  "id": "mod",'
            + '  "userid": "mod",'
            + '  "name": "mod",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "@room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online is None

    queue.add_messages(
        [
            ">room1",
            "|n| modalt|mod",
        ],
        [
            "|queryresponse|userdetails|{"
            + '  "id": "modalt",'
            + '  "userid": "modalt",'
            + '  "name": "modalt",'
            + '  "avatar": "1",'
            + '  "group": " ",'
            + '  "autoconfirmed": true,'
            + '  "status": "",'
            + '  "rooms": {'
            + '    "room1": {}'
            + "  }"
            + "}"
        ],
    )
    assert room1.no_mods_online is None

    # finally they both leave
    queue.add_messages(
        [
            ">room1",
            "|l|modalt",
        ],
        [
            ">room1",
            "|l|mod2",
        ],
    )
    assert room1.no_mods_online is not None

    queue.close()
