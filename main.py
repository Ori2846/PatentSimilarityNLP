import requests
from bs4 import BeautifulSoup
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, render_template_string
import logging
from sentence_transformers import SentenceTransformer
import sqlite3

logging.basicConfig(level=logging.INFO)

nlp = spacy.load('en_core_web_sm')
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

app = Flask(__name__)

DATABASE = 'patents.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
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


def save_patent_data(patent_data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO patents (number, title, abstract, claims)
        VALUES (?, ?, ?, ?)
    ''', (patent_data['number'], patent_data['title'], patent_data['abstract'], patent_data['claims']))
    conn.commit()
    conn.close()


def get_patent_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT number, title, abstract, claims FROM patents')
    rows = cursor.fetchall()
    conn.close()
    return [{'number': row[0], 'title': row[1], 'abstract': row[2], 'claims': row[3]} for row in rows]


def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    processed_text = ' '.join(tokens)
    logging.info(f"Processed text: {processed_text}")
    return processed_text


@app.route('/')
def home():
    return render_template_string('''
    <h1>Patent Similarity Detection</h1>
    <p>Use the /similarity endpoint with a POST request to check patent similarities.</p>
    ''')


@app.route('/similarity', methods=['POST'])
def similarity():
    data = request.json
    query_doc = preprocess_text(data['query'])
    query_vec = bert_model.encode([query_doc])
    patents = get_patent_data()
    patent_abstracts = [patent['abstract'] for patent in patents]
    patent_vecs = bert_model.encode(patent_abstracts)
    similarities = cosine_similarity(query_vec, patent_vecs)

    response = [{'patent_number': patents[i]['number'], 'similarity': float(sim)} for i, sim in
                enumerate(similarities[0])]
    response = sorted(response, key=lambda x: x['similarity'], reverse=True)
    logging.info(f"Similarities: {response}")
    return jsonify(response)


if __name__ == '__main__':
    init_db()

    initial_patent_numbers = ['US11888042B2', 'US8765432B2']
    for pn in initial_patent_numbers:
        data = fetch_patent_data(pn)
        if data:
            save_patent_data(data)

    app.run(debug=True)
