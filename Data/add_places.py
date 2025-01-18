from bs4 import BeautifulSoup as bs
from urllib import request
import pandas as pd

print("Fetching Data of Different Airports...")

# Adding top 100 airports in the world
page = request.urlopen("https://gettocenter.com/airports/top-100-airports-in-world")
soup = bs(page, features="html.parser")

column_names = ['city', 'airport', 'code', 'country']
rows = []

tr = soup.body.find_all('tr')

for r in tr:
    d = r.find_all('td')
    if len(d) >= 5:  # Ensuring all required columns are available
        airport = d[1].text.strip()
        code = d[2].text.strip().upper()
        city = d[3].text.strip()
        country = d[4].text.strip()

        row = [city, airport, code, country]
        rows.append(row)

# Create DataFrame from rows
df = pd.DataFrame(rows, columns=column_names)

# Adding top 30 airports in India
page = request.urlopen("https://www.worlddata.info/asia/india/airports.php")
soup = bs(page, features="html.parser")

tr = soup.body.find_all('table')[0].find_all('tr')

for r in tr[1:]:
    d = r.find_all('td')
    if len(d) >= 3:  # Ensuring all required columns are available
        airport = d[1].text.strip()
        code = d[0].text.strip().upper()
        city = d[2].text.strip()
        country = 'India'

        # Avoid duplicates by checking if code already exists in DataFrame
        if code not in df['code'].values:
            row = [city, airport, code, country]
            rows.append(row)

# Create DataFrame from rows again to include both world and India airports
df = pd.DataFrame(rows, columns=column_names)

print("Saving data in the file airports.csv")
df.to_csv("airports.csv", index=False)

print("DONE")
