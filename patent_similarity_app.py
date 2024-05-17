import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template_string
import logging
from sentence_transformers import SentenceTransformer
import sqlite3
import re
import math

logging.basicConfig(level=logging.INFO)

bert_model = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity_manual(vec1, vec2):
    dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    magnitude_vec1 = math.sqrt(sum(v ** 2 for v in vec1))
    magnitude_vec2 = math.sqrt(sum(v ** 2 for v in vec2))
    if not magnitude_vec1 or not magnitude_vec2:
        return 0.0
    return dot_product / (magnitude_vec1 * magnitude_vec2)

class PatentSimilarityApp:
    def __init__(self, db_path='patents.db'):
        self.app = Flask(__name__)
        self.db_path = db_path
        self.setup_routes()

    def get_patent_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT number, title, abstract, claims FROM patents')
        rows = cursor.fetchall()
        conn.close()
        return [{'number': row[0], 'title': row[1], 'abstract': row[2], 'claims': row[3]} for row in rows]

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        tokens = text.split()
        lemmas = [token.rstrip('s') for token in tokens]
        stop_words = set(
            ['a', 'an', 'the', 'and', 'or', 'but', 'if', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'of', 'for',
             'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
             'to', 'from', 'up', 'down', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
             'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
             'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
             'should', 'now'])
        filtered_lemmas = [lemma for lemma in lemmas if lemma not in stop_words]
        processed_text = ' '.join(filtered_lemmas)
        logging.info(f"Processed text: {processed_text}")
        return processed_text

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return render_template_string('''
            <h1>Patent Similarity Detection</h1>
            <p>Use the /similarity endpoint with a POST request to check patent similarities.</p>
            ''')

        @self.app.route('/similarity', methods=['POST'])
        def similarity():
            data = request.json
            query_doc = self.preprocess_text(data['query'])
            query_vec = bert_model.encode([query_doc])
            patents = self.get_patent_data()
            patent_abstracts = [patent['abstract'] for patent in patents]
            patent_vecs = bert_model.encode(patent_abstracts)

            similarities = [cosine_similarity_manual(query_vec[0], patent_vec) for patent_vec in patent_vecs]

            response = [{'patent_number': patents[i]['number'], 'similarity': float(sim)} for i, sim in
                        enumerate(similarities)]
            response = sorted(response, key=lambda x: x['similarity'], reverse=True)
            logging.info(f"Similarities: {response}")
            return jsonify(response)

    def run(self, debug=True):
        self.app.run(debug=debug)

if __name__ == '__main__':
    app = PatentSimilarityApp()
    app.run()
