import csv

import utils

async def location(self, room, user, arg):
  if room is None or not utils.is_voice(user):
    return

  pokemon = next((item for item in POKEMON if item['identifier'] == arg), None)
  if pokemon is None:
    return await self.send_reply(room, user, 'Nessun dato')

  raw_encounters = list(filter(lambda encounter: encounter['pokemon_id'] == pokemon['id'], ENCOUNTERS))

  encounters = {}

  for encounter in raw_encounters:

    if not encounter['version_id'] in encounters:
      version_name = next((item['name'] for item in VERSION_NAMES if item['version_id'] == encounter['version_id'] and item['local_language_id'] == '9'), None)
      encounters[encounter['version_id']] = {'version_name': version_name,
                                             'encounters': {}}

    if not encounter['location_area_id'] in encounters[encounter['version_id']]['encounters']:
      location_area_name = next((item['name'] for item in LOCATION_AREA_PROSE if item['location_area_id'] == encounter['location_area_id'] and item['local_language_id'] == '9'), '')
      location_id = next((item['location_id'] for item in LOCATION_AREAS if item['id'] == encounter['location_area_id']), None)
      location_name = next(({'name': item['name'], 'subtitle': item['subtitle']} for item in LOCATION_NAMES if item['location_id'] == location_id and item['local_language_id'] == '9'), {'name': '', 'subtitle': ''})
      location_name_complete = location_name['name']
      if len(location_name['subtitle']):
        location_name_complete += ' - ' + location_name['subtitle']
      if len(location_area_name):
        location_name_complete += ' (' + location_area_name + ')'
      encounters[encounter['version_id']]['encounters'][encounter['location_area_id']] = {'location_name': location_name_complete,
                                                                                          'methods': {}}

    encounter_slot = next(({'encounter_method_id': item['encounter_method_id'], 'rarity': item['rarity']} for item in ENCOUNTER_SLOTS if item['id'] == encounter['encounter_slot_id']), None)
    if not encounter_slot['encounter_method_id'] in encounters[encounter['version_id']]['encounters'][encounter['location_area_id']]['methods']:
      encounters[encounter['version_id']]['encounters'][encounter['location_area_id']]['methods'][encounter_slot['encounter_method_id']] = {'encounter_method_name': next((item['name'] for item in ENCOUNTER_METHOD_PROSE if item['encounter_method_id'] == encounter_slot['encounter_method_id'] and item['local_language_id'] == '9'), None),
                                                                                                                                            'encounter_method_order': next((item['order'] for item in ENCOUNTER_METHODS if item['id'] == encounter_slot['encounter_method_id']), None),
                                                                                                                                            'min_level': 100,
                                                                                                                                            'max_level': 1,
                                                                                                                                            'rarity': {'base': 0,
                                                                                                                                                       'conditions': []}}

    encounters[encounter['version_id']]['encounters'][encounter['location_area_id']]['methods'][encounter_slot['encounter_method_id']]['min_level'] = min(int(encounter['min_level']), encounters[encounter['version_id']]['encounters'][encounter['location_area_id']]['methods'][encounter_slot['encounter_method_id']]['min_level'])
    encounters[encounter['version_id']]['encounters'][encounter['location_area_id']]['methods'][encounter_slot['encounter_method_id']]['max_level'] = max(int(encounter['max_level']), encounters[encounter['version_id']]['encounters'][encounter['location_area_id']]['methods'][encounter_slot['encounter_method_id']]['max_level'])

    encounter_conditions = sorted(list(filter(lambda condition: condition['encounter_id'] == encounter['id'], ENCOUNTER_CONDITION_VALUE_MAP)), key=lambda k: k['encounter_condition_value_id'])

    if len(encounter_conditions):
      condition_names = []
      for condition in encounter_conditions:
        condition_names.append(next((item['name'] for item in ENCOUNTER_CONDITION_VALUE_PROSE if item['encounter_condition_value_id'] == condition['encounter_condition_value_id'] and item['local_language_id'] == '9'), None))
      encounters[encounter['version_id']]['encounters'][encounter['location_area_id']]['methods'][encounter_slot['encounter_method_id']]['rarity']['conditions'].append({'name': ', '.join(condition_names),
                                                                                                                                                                    'rarity': int(encounter_slot['rarity'])})
    else:
      encounters[encounter['version_id']]['encounters'][encounter['location_area_id']]['methods'][encounter_slot['encounter_method_id']]['rarity']['base'] += int(encounter_slot['rarity'])


  versions_sorted = sorted(encounters, key=int)

  row = '<tr><td>{location}</td><td>{method}</td><td>{levels}</td><td style="text-align:right">{rarity}</td><td>{conditions}</td></tr>'
  conditions_col = '+{rarity}% {name}<br>'
  #head = '<tr><th>Location</th>
  head = '<summary><b><big>{version}</big></b></summary>'
  html = ''
  for version in versions_sorted:
    html += '<details>' + head.format(version=encounters[version]['version_name'])
    html += '<table style="width:100%"><tbody>'
    encounters_sorted = sorted(encounters[version]['encounters'], key=int)
    for encounter in encounters_sorted:
      methods_sorted = sorted(encounters[version]['encounters'][encounter]['methods'], key=int)
      for method in methods_sorted:
        levels = 'L' + str(encounters[version]['encounters'][encounter]['methods'][method]['min_level'])
        if encounters[version]['encounters'][encounter]['methods'][method]['min_level'] < encounters[version]['encounters'][encounter]['methods'][method]['max_level']:
          levels += '-' + str(encounters[version]['encounters'][encounter]['methods'][method]['max_level'])
        conditions = ''
        for condition in encounters[version]['encounters'][encounter]['methods'][method]['rarity']['conditions']:
          conditions += conditions_col.format(rarity=condition['rarity'],
                                              name=condition['name'])
        html += row.format(location=encounters[version]['encounters'][encounter]['location_name'],
                           method=encounters[version]['encounters'][encounter]['methods'][method]['encounter_method_name'],
                           levels=levels,
                           rarity=str(encounters[version]['encounters'][encounter]['methods'][method]['rarity']['base']) + '%',
                           conditions=conditions)
    html += '</tbody></table>'
    html += '</details>'

  await self.send_htmlbox(room, html)


with open('./data/veekun/encounter_condition_value_map.csv', 'r') as f:
  ENCOUNTER_CONDITION_VALUE_MAP = list(csv.DictReader(f))

with open('./data/veekun/encounter_condition_value_prose.csv', 'r') as f:
  ENCOUNTER_CONDITION_VALUE_PROSE = list(csv.DictReader(f))

with open('./data/veekun/encounter_method_prose.csv', 'r') as f:
  ENCOUNTER_METHOD_PROSE = list(csv.DictReader(f))

with open('./data/veekun/encounter_methods.csv', 'r') as f:
  ENCOUNTER_METHODS = list(csv.DictReader(f))

with open('./data/veekun/encounter_slots.csv', 'r') as f:
  ENCOUNTER_SLOTS = list(csv.DictReader(f))

with open('./data/veekun/encounters.csv', 'r') as f:
  ENCOUNTERS = list(csv.DictReader(f))

with open('./data/veekun/location_names.csv', 'r') as f:
  LOCATION_NAMES = list(csv.DictReader(f))

with open('./data/veekun/location_area_prose.csv', 'r') as f:
  LOCATION_AREA_PROSE = list(csv.DictReader(f))

with open('./data/veekun/location_areas.csv', 'r') as f:
  LOCATION_AREAS = list(csv.DictReader(f))

with open('./data/veekun/pokemon.csv', 'r') as f:
  POKEMON = list(csv.DictReader(f))

with open('./data/veekun/version_names.csv', 'r') as f:
  VERSION_NAMES = list(csv.DictReader(f))
