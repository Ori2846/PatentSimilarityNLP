# PatentSimilarityNLP
 

Patent Similarity Detection Using Machine Learning
Overview
This project is a web-based application designed to detect and compare the similarity of patent documents using natural language processing (NLP) and machine learning techniques. The application preprocesses patent text data, converts it into numerical representations using TF-IDF vectorization, and calculates similarity scores using cosine similarity.

Features
Patent Data Collection: Fetches and processes patent data from online sources.
Text Preprocessing: Implements tokenization, stop word removal, and lemmatization to clean and standardize text data.
TF-IDF Vectorization: Transforms text data into numerical features suitable for machine learning.
Similarity Detection: Calculates similarity scores between patent documents using cosine similarity.
Web Interface: Provides a user-friendly interface built with Flask for inputting patent text and displaying similarity results.

![image](https://github.com/Ori2846/PatentSimilarityNLP/assets/74078771/3c159d52-1b9c-4308-a3dd-94790936d80b)


Technologies Used
Python: Core programming language.
Flask: Web framework for building the application.
spaCy: NLP library for text preprocessing.
scikit-learn: Machine learning library for TF-IDF vectorization and cosine similarity.
BeautifulSoup: Web scraping library for collecting patent data.
requests: Library for making HTTP requests.

Usage: curl -X POST -H "Content-Type: application/json" -d '{"query": "Your patent abstract text here"}' http://127.0.0.1:5000/similarity

Example payload: {
  "query": "The present invention provides a fusion terminal which can be selectively used at least for a first network and a second network. The present invention comprises a first communication device used for the first network, a second communication device used for the second network, a basic common part used for realizing the input function and the output function of the fusion terminal, and an application processor used for the collaboration of the first communication device, the second communication device and the basic common part. According to requirements, at least one of the first communication device and the second communication device is connected with the basic common part; therefore, one of various load supporting modes of the fusion terminal is selected. According to the fusion terminal of the present invention, no special requirements are required for the existing mobile network and the existing PSTN network; different phone numbers are used for the mobile network and the PSTN network by users; the habits for utilization of mobile users are respected. According to the habits for utilization of mobile users, PSTN telephones are called; the share of the functions and modules of the mobile terminal and the PSTN terminal are furthest realized; the telephone fee of users can be lowered."
}

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for details.
