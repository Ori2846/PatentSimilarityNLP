

---

<p align="center">
    <img src="https://github.com/Ori2846/PatentSimilarityNLP/assets/74078771/3173afcf-1d9d-4fa1-80bf-c6b7cd7e08e9"/>
</p>

<p align="center">
    <b>Patent Similarity Detection Using Machine Learning</b>
</p>

<p align="center">
    <a href="https://github.com/Ori2846/PatentSimilarityNLP/releases">
        <img src="https://img.shields.io/github/release/Ori2846/PatentSimilarityNLP.svg?style=flat&color=success" alt="Version"/>
    </a>
    <a href="https://github.com/Ori2846/PatentSimilarityNLP/releases">
        <img src="https://img.shields.io/github/release-date/Ori2846/PatentSimilarityNLP.svg?style=flat&color=blue" alt="GitHub Release Date"/>
    </a>
    <a href="https://github.com/Ori2846/PatentSimilarityNLP/issues">
        <img src="https://img.shields.io/github/issues/Ori2846/PatentSimilarityNLP.svg?style=flat&color=success" alt="GitHub issues"/>
    </a>
    <a href="https://github.com/Ori2846/PatentSimilarityNLP">
        <img src="https://img.shields.io/github/last-commit/Ori2846/PatentSimilarityNLP.svg?style=flat&color=blue" alt="GitHub last commit"/>
    </a>
</p>

---

## Overview
This project is a web-based application designed to detect and compare the similarity of patent documents using natural language processing (NLP) and machine learning techniques. The application preprocesses patent text data, converts it into numerical representations using advanced embeddings from sentence transformers, and calculates similarity scores using cosine similarity.

## Features
- **Patent Data Collection**: Fetches and processes patent data from online sources.
- **Text Preprocessing**: Implements tokenization, stop word removal, and lemmatization to clean and standardize text data.
- **Advanced Embedding Generation**: Uses Sentence Transformers for more accurate numerical representations of text data.
- **Similarity Detection**: Calculates similarity scores between patent documents using cosine similarity.
- **Web Interface**: Provides a user-friendly interface built with Flask for inputting patent text and displaying similarity results.

<p align="center">
    <img src="https://github.com/Ori2846/PatentSimilarityNLP/assets/74078771/1a8e4426-c5af-4c45-bd39-a11184f9dcc3"/>
</p>

## Technologies Used
- **Python**: Core programming language.
- **Flask**: Web framework for building the application.
- **spaCy**: NLP library for text preprocessing.
- **Sentence Transformers**: For generating advanced text embeddings.
- **scikit-learn**: Machine learning library for cosine similarity calculations.
- **BeautifulSoup**: Web scraping library for collecting patent data.
- **requests**: Library for making HTTP requests.

## Usage
```sh
curl -X POST -H "Content-Type: application/json" -d '{"query": "Your patent abstract text here"}' http://127.0.0.1:5000/similarity
```
Or:
```sh
Invoke-WebRequest -Uri http://127.0.0.1:5000/similarity -Method POST -ContentType "application/json" -Body '{"query": "Three-dimensional semiconductor memory devices and methods of fabricating the same. The three-dimensional semiconductor devices include an electrode structure with sequentially-stacked electrodes disposed on a substrate, semiconductor patterns penetrating the electrode structure, and memory elements including a first pattern and a second pattern interposed between the semiconductor patterns and the electrode structure, the first pattern vertically extending to cross the electrodes and the second pattern horizontally extending to cross the semiconductor patterns."}'
```

### Example Payload
```json
{
  "query": "The present invention provides a fusion terminal which can be selectively used at least for a first network and a second network. The present invention comprises a first communication device used for the first network, a second communication device used for the second network, a basic common part used for realizing the input function and the output function of the fusion terminal, and an application processor used for the collaboration of the first communication device, the second communication device and the basic common part. According to requirements, at least one of the first communication device and the second communication device is connected with the basic common part; therefore, one of various load supporting modes of the fusion terminal is selected. According to the fusion terminal of the present invention, no special requirements are required for the existing mobile network and the existing PSTN network; different phone numbers are used for the mobile network and the PSTN network by users; the habits for utilization of mobile users are respected. According to the habits for utilization of mobile users, PSTN telephones are called; the share of the functions and modules of the mobile terminal and the PSTN terminal are furthest realized; the telephone fee of users can be lowered."
}
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Project Updates
- **Advanced Embeddings**: Replaced TF-IDF vectorization with Sentence Transformers for generating embeddings, enhancing accuracy in similarity detection.
- **Database Integration**: Implemented SQLite for efficient patent data storage and retrieval.
- **Error Handling and Logging**: Added robust error handling and logging for better debugging and monitoring.
- **JSON Serialization Fix**: Ensured all similarity scores are converted to standard `float` types to avoid serialization issues.
