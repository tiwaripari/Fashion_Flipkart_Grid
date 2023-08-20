import sqlite3
import os
import shutil
import csv
import requests
from bs4 import BeautifulSoup

history_db = os.path.expanduser('~') + "/Library/Application Support/Google/Chrome/Default/History"
shutil.copy2(history_db, "temp_history")
conn = sqlite3.connect("temp_history")
cursor = conn.cursor()
query = "SELECT url, title, last_visit_time FROM urls WHERE url LIKE '%https://www.flipkart.com/%' ORDER BY last_visit_time DESC"
cursor.execute(query)
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID', 'Occasion', 'Type', 'Color'])
    rows = cursor.fetchall()
    for i, row in enumerate(rows, start=1):
        url = row[0]
        title = row[1]
        timestamp = row[2] / 1000000
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        div_element = soup.find('div', class_="_2yIA0Y")
        occasion_found = False
        type_found = False
        color_found = False

        if div_element and "Occasion" in div_element.text:
            row_elements = div_element.find_all('div', class_="row")
            for row_element in row_elements:
                col_element = row_element.find('div', class_="col col-3-12 _2H87wv")
                if col_element and col_element.text.strip() == "Occasion":
                    occasion = col_element.find_next_sibling('div', class_="col col-9-12 _2vZqPX").text.strip()
                    occasion_found = True
                if col_element and col_element.text.strip() == "Type":
                    type = col_element.find_next_sibling('div', class_="col col-9-12 _2vZqPX").text.strip()
                    type_found = True
                if col_element and col_element.text.strip() == "Color":
                    color = col_element.find_next_sibling('div', class_="col col-9-12 _2vZqPX").text.strip()
                    color_found = True

        writer.writerow([i, occasion if occasion_found else "casual", type if type_found else "", color if color_found else "Multi-colour"])

conn.close()
os.remove("temp_history")
