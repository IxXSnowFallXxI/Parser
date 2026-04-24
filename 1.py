import requests
from bs4 import BeautifulSoup as BfS
import json
import psycopg2
import pprint

data = requests.get(link)
soup = BfS(data.text, "html.parser")
json_scripts = soup.find_all('script', type='application/ld+json')
game_req_list = []
for script in json_scripts:
    req_data = json.loads(script.string)
    if req_data.get('@type') != 'SoftwareApplication':
        continue

    full_name = req_data.get('name', '')
    if not full_name:
        continue

    if 'минимальные' in full_name.lower():
        req_type = 'min'
    elif 'рекомендуемые' in full_name.lower():
        req_type = 'rec'
    else:
        continue

    game_req = {
        "name": full_name,
        "type": req_type,
        "cpu": req_data.get('processorRequirements', 'N/A'),
        "gpu": req_data.get('graphicsRequirements', 'N/A'),
        "os": req_data.get('operatingSystem', 'N/A'),
        "ram": req_data.get('memoryRequirements', 'N/A'),
        "storage": req_data.get('storageRequirements', 'N/A')
    }
   
    game_req_list.append(game_req)
with open("pars.txt", "w", encoding='utf-8') as f:
    for line in game_req_list:
        f.write(pprint.pformat(line, sort_dicts=False))
