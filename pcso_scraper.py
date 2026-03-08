import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

url = "https://www.lottopcso.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

today = datetime.now().strftime("%B %d, %Y")

results = []

# valid time pattern
time_pattern = re.compile(r'^\d{1,2}:\d{2}\s?(AM|PM)$')

tables = soup.find_all("table")

for table in tables:

    rows = table.find_all("tr")

    for row in rows:

        cols = row.find_all("td")

        if len(cols) >= 2:

            draw_time = cols[0].text.strip()
            result = cols[1].text.strip()

            # Skip standby
            if "stand" in result.lower():
                continue

            # ONLY accept valid time rows
            if not time_pattern.match(draw_time):
                continue

            # Only numbers like 1-2-3
            if not re.match(r'^[0-9\-]+$', result):
                continue

            numbers = result.split("-")
            count = len(numbers)

            # Detect lotto game
            if count == 2:
                game = "2D Lotto"
            elif count == 3:
                game = "3D Lotto"
            elif count == 4:
                game = "4D Lotto"
            elif count == 6:
                game = "6 Digit Lotto"
            else:
                continue

            results.append({
                "game": game,
                "date": today,
                "time": draw_time,
                "result": result
            })


# remove duplicates
unique = []
seen = set()

for r in results:

    key = f"{r['game']}-{r['time']}-{r['result']}"

    if key not in seen:
        seen.add(key)
        unique.append(r)


for r in unique:

    print("====== PCSO RESULT ======")
    print("Game:", r["game"])
    print("Date:", r["date"])
    print("Time:", r["time"])
    print("Result:", r["result"])
    print("=========================")




data = {
    "game": "3D Lotto",
    "date": "March 05 2026",
    "time": "2:00 PM",
    "result": "0-6-4"
}

webhook_url = "https://rapao-n8n.hf.space/webhook/lotto-result"

requests.post(webhook_url, json=data)


