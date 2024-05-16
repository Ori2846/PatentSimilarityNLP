import requests
from bs4 import BeautifulSoup
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, render_template_string


def fetch_patent_data(patent_number):
    url = f"https://patents.google.com/patent/{patent_number}/en"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('span', itemprop='title').text if soup.find('span', itemprop='title') else ''
    abstract = soup.find('div', class_='abstract').text if soup.find('div', class_='abstract') else ''
    claims = soup.find('div', class_='claims').text if soup.find('div', class_='claims') else ''
    print(f"Fetched data for {patent_number}: Title: {title}, Abstract: {abstract}, Claims: {claims}")
    return {'title': title, 'abstract': abstract, 'claims': claims}


patent_numbers = ['US7654321B1', 'US8765432B2']


patent_data = [fetch_patent_data(pn) for pn in patent_numbers]


additional_patent_numbers = ['US9876543B1', 'US8765432B2', 'US1234567A']
additional_patent_data = [fetch_patent_data(pn) for pn in additional_patent_numbers]
patent_data.extend(additional_patent_data)


nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    processed_text = ' '.join(tokens)
    print(f"Processed text: {processed_text}")
    return processed_text

documents = [preprocess_text(data['abstract']) for data in patent_data]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)
print("TF-IDF matrix:", X.toarray())

app = Flask(__name__)

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
    query_vec = vectorizer.transform([query_doc])
    similarities = cosine_similarity(query_vec, X)
    print(f"Query vector: {query_vec.toarray()}")
    print(f"Similarities: {similarities}")
    return jsonify(similarities[0].tolist())

if __name__ == '__main__':
    app.run(debug=True)
