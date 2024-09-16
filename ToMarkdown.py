from magic_item import Source
import json
import re
import os
from markdownify import markdownify

config = 'spells'
match config:
    case 'magic_item':
        magic_item_file_path =  './exported_magic_items.json'

        with open(magic_item_file_path, 'r') as inputFile:
            magic_items = json.load(inputFile)

        for item in magic_items:
            output_file = f'./ItemsClean/{item["rarity"]}/{item["name"]}.md'
            if not os.path.exists(f'./ItemsClean/{item["rarity"]}'):
                os.makedirs(f'./ItemsClean/{item["rarity"]}')
            item_text = f'''---
Rarity: {item["rarity"]}
Type: {item["type"]}
Source: {Source[item["source"]].toJSON()}
---

# {item["name"]}

{item["text"]}
        '''
            item_text = re.sub(r'\n{3,}', '\n\n', item_text)
            with open(output_file, 'w') as magic_item_file:
                magic_item_file.write(item_text)
    
    case 'spells':
        spell_file_path =  './exported_spells.json'

        with open(spell_file_path, 'r') as inputFile:
            spells = json.load(inputFile)

        for spell in spells:
            output_file = f'./SpellsClean/{spell["level"]}/{spell["name"].replace('/', '_').strip()}.md'
            if not os.path.exists(f'./SpellsClean/{spell["level"]}'):
                os.makedirs(f'./SpellsClean/{spell["level"]}')
            spell["cast_time"] = f' {spell["cast_time"]} minutos' if spell["cast_time"] != 0 else ''
            spell["spell_range"] = spell["spell_range"] if spell["spell_range"]!= '0' else spell["range_type"]
            higher_levels = ''
            if spell['has_upcast']:
                higher_levels = f'## At Higher Levels\n\n{spell['upcast']}'

            spell_text = f'''---
Level: {spell["level"]}
School: {spell["school"]}
Duration: {spell["duration"]}
Concentracion: {spell["is_concentration"]}
Tiempo: {spell["cast_type"]}{spell["cast_time"]}
Ritual: {spell["is_ritual"]}
Rango: {spell["spell_range"]}
Componentes: {', '.join(s[0] for s in spell['components'])}
ComponenteMaterial : {spell['component_material']}
Classes: {', '.join(spell['classes'])}
---

# {spell["name"]}

{markdownify(spell["description"])}
{higher_levels}
'''
            spell_text = re.sub(r'\n{3,}', '\n\n', spell_text)
            spell_text = re.sub(r'\n\s([^\s])', '\n\\1', spell_text)
            spell_text = re.sub(r'[\n\s]+$', '', spell_text)

            with open(output_file, 'w') as spell_file:
                spell_file.write(spell_text)
