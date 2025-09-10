import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("MONKEYTYPE_API_KEY")

headers = {
    'Authorization': f'ApeKey {API_KEY}'
}

# GET request for MonkeyType STATS
stats_response = requests.get(f'https://api.monkeytype.com/users/stats', headers=headers)

# Check request response
if stats_response.status_code != 200:
    print(f"Stats API error (Status {stats_response.status_code}): {stats_response.text}")
    exit(1)

stats_data = stats_response.json()
completed_tests = stats_data['data']['completedTests']


def get_personal_best(mode, mode2, duration):
    params = {
        'mode': mode,
        'mode2': mode2
    }

    response = requests.get('https://api.monkeytype.com/users/personalBests', headers=headers, params=params)

    if response.status_code != 200:
        print(f"Personal Best ({duration}) API error (Status {response.status_code}): {response.text}")
        return None
    
    data = response.json()

    # Check that data is not empty
    if 'data' not in data or not data['data']:
        # print(f"No personal best data available for {duration}")
        return None

    # Data is returned in list form, so get first entry
    entry = data['data'][0]

    return {
        'accuracy': entry['acc'],
        'difficulty': entry['difficulty'],
        'wpm': entry['wpm']
    }

# get personal bests for each category
pb15 = get_personal_best('time', '15', '15s')
pb30 = get_personal_best('time', '30', '30s')
pb60 = get_personal_best('time', '60', '60s')


# Create new stats table based on updated stats
new_content = f"""
<div align="center">
### Tests completed: {completed_tests}

### Personal Bests:

| | 15 seconds   |      30 seconds      |  60 seconds |
|:------          |:----------:|:-------------:|------:|
|**WPM**            |{pb15['wpm']}|{pb30['wpm']}|{pb60['wpm']}|
|**Accuracy**       |{pb15['accuracy']}%|{pb30['accuracy']}%|{pb60['accuracy']}%|
|**Difficulty**     |0|0|0|

</div>
"""

# Update README with new MT stats

with open('README.md', 'r', encoding='utf-8') as file:
    content = file.read()

start = f"<!--- START --->"
end = f"<!--- END --->"

start_index = content.find(start)
end_index = content.find(end)

if start_index == -1  or end_index == -1:
    raise ValueError(f"Section not found in file")

# Calculate positions after start marker and before end marker
start = start_index + len(start)

# Replace the section content
updated = (content[:start] + f"\n{new_content}\n" + content[end_index:])

with open("README.md", 'w', encoding='utf-8') as file:
    file.write(updated)