import requests
from bs4 import BeautifulSoup
import sqlite3
import logging
import json

logging.basicConfig(level=logging.INFO) 

def init_db(db_path='patents.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT UNIQUE,
            title TEXT,
            abstract TEXT,
            claims TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_patent_data(patent_number):
    url = f"https://patents.google.com/patent/{patent_number}/en"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('span', itemprop='title').text if soup.find('span', itemprop='title') else ''
        abstract = soup.find('div', class_='abstract').text if soup.find('div', class_='abstract') else ''
        claims = soup.find('div', class_='claims').text if soup.find('div', class_='claims') else ''
        logging.info(f"Fetched data for {patent_number}: Title: {title}, Abstract: {abstract}, Claims: {claims}")
        return {'number': patent_number, 'title': title, 'abstract': abstract, 'claims': claims}
    except requests.RequestException as e:
        logging.error(f"Error fetching data for {patent_number}: {e}")
        return None

def save_patent_data(patent_data, db_path='patents.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO patents (number, title, abstract, claims)
        VALUES (?, ?, ?, ?)
    ''', (patent_data['number'], patent_data['title'], patent_data['abstract'], patent_data['claims']))
    conn.commit()
    conn.close()

def collect_patents(patent_numbers, db_path='patents.db'):
    for pn in patent_numbers:
        data = fetch_patent_data(pn)
        if data:
            save_patent_data(data, db_path)

def load_patent_numbers_from_json(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
        return data.get('patent_numbers', [])

if __name__ == '__main__':
    init_db()
    patent_numbers = load_patent_numbers_from_json('patent_numbers.json')
    collect_patents(patent_numbers)
