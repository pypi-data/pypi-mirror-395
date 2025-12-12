#
#   Imandra Inc.
#
#   convert_api_to_mkd.py 
#


import json

with open('iml_api_reference_202510011126.json') as infile:
    contents = infile.read()


j = json.loads(contents)

data = {'base': []}

for record in j:
    if record['module'] == '':
        data['base'].append(record)
    else:
        if record['module'] not in data:
            data[record['module']] = []
        data[record['module']].append(record)


for idx, module_name in enumerate(data.keys()):

    name = module_name.capitalize()

    sStr = f"""----
title: {name} Module
description: {name} Module types and functions
order: {idx+1}
----

"""
    for record in data[module_name]:
        signature = record['signature']
        name = record['name']
        type_ = record['type']
        doc = record['doc']
        pattern = record['pattern']

        if doc is None: doc='N\\A'
        if pattern is None: pattern='N\\A'


        sStr += f"""
## `{signature.replace("\n",' ')}`
- name: {name}
- type: {type_}
- signature: `{signature}`
- doc: {doc}
- pattern: {pattern}

"""

    filepath = f'api/{module_name.lower()}.md'
    with open(filepath, 'w') as outfile:
        print(sStr, file=outfile)
