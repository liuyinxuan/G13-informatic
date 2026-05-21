from collections import defaultdict
import json
import math
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import zipfile
import re
from urllib.parse import urlparse, urlunparse
import time
import nltk
from nltk.data import find


# uncomment this if those things are not downloaded
try:
    find('tokenizers/punkt')
except LookupError:
    # If not found, download
    nltk.download('punkt')

try:
    find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


# this should load the inverted_index created by indexer.py
def load_json(path='inverted_index.json'):
    with open(path, 'r') as file:
        return json.load(file)


# In case the inverted index contains .json file instead of urls
# this would turn filepath into urls (reads the file)
# no longer used
def get_url_from_file(filepath, zippath="developer.zip"):
    try:
        with zipfile.ZipFile(zippath) as z:
            with z.open(filepath) as f:
                content = f.read().decode('utf-8')
                content = json.loads(content)
                url = content.get('url', '')  # Extract the URL
    except Exception as e:
        print(f"Error processing file: {e}")
        return None  # Return None if there was an error
    return url or None  # Return None if URL is not found in JSON content


# this should preprocess what user entered, and change it into appropriate suffix (token)
def preprocess_input(inputs):
    stemmer = PorterStemmer()
    stopword = set(stopwords.words('english'))
    lowered_i = inputs.lower()
    valid_i = re.sub(r'[^a-zA-Z0-9\s]', '', lowered_i)  # check if non letter/int word is present
    # REMINDER: change this to our tokenizer at M3
    tokens = word_tokenize(valid_i)
    # isalnum recheck if the word is valid (no non-letter/int character)
    stem = [stemmer.stem(v) for v in tokens if v.isalnum() and v not in stopword]
    return stem


# this should be the main program for searching.
def AND_search(inputs, inverted_index):
    tokens = preprocess_input(inputs)
    # use first token(stem) to allocate document set
    if tokens and tokens[0] in inverted_index:
        documents = set(inverted_index[tokens[0]].keys())
    else:
        return []  # if not found then means no match for AND

    # perform AND
    for v in tokens[1:]:
        if v in inverted_index:
            documents &= set(inverted_index[v].keys())  # keep those files that intersect the first token only.
        else:
            return []  # same logic

    if len(documents) == 0:
        return []

    # Calculate TF-IDF scores for the query
    tfidf_query = {}
    for token in set(tokens):  # Use set to remove duplicates
        tf = tokens.count(token) / len(tokens)
        df = len(inverted_index[token])
        idf = math.log(len(documents) / (df + 1)) + 1  # Add 1 to avoid division by zero and adjust IDF
        tfidf_query[token] = tf * idf

    # Calculate TF-IDF scores for each document
    tfidf_scores = defaultdict(float)
    for doc_id in documents:
        tfidf_doc = {}
        for token in set(tokens):  # Use set to remove duplicates
            tf = inverted_index[token].get(doc_id, 0)
            df = len(inverted_index[token])
            idf = math.log(len(documents) / (df + 1)) + 1  # Add 1 to avoid division by zero and adjust IDF
            tfidf_doc[token] = tf * idf
        # Sum up the TF-IDF scores for all query terms in the document
        tfidf_scores[doc_id] = sum(tfidf_query[token] * tfidf_doc[token] for token in tfidf_query)

    # Sort documents by total TF-IDF score
    ranked = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    ranked_docs = [doc_id for doc_id, _ in ranked]

    return ranked_docs

def OR_search(inputs, inverted_index):
    tokens = preprocess_input(inputs)

    # Initialize a set to collect documents that contain any of the tokens
    documents = set()
    for token in tokens:
        if token in inverted_index:
            documents.update(inverted_index[token].keys())  # Use update to add documents for each token

    if not documents:
        return []

    # Calculate TF-IDF scores for the query
    tfidf_query = {}
    total_documents = len(documents)
    for token in set(tokens):  # Use set to remove duplicates
        tf = tokens.count(token) / len(tokens)
        df = len(inverted_index.get(token, {}))
        idf = math.log((total_documents / (df + 1))) + 1  # Adjust IDF calculation
        tfidf_query[token] = tf * idf

    # Calculate TF-IDF scores for each document
    tfidf_scores = defaultdict(float)
    for doc_id in documents:
        tfidf_doc = {}
        for token in set(tokens):  # Use set to remove duplicates
            if token in inverted_index:
                tf = inverted_index[token].get(doc_id, 0)
                df = len(inverted_index[token])
                idf = math.log(total_documents / (df + 1)) + 1  # Adjust IDF calculation
                tfidf_doc[token] = tf * idf
                # Sum up the TF-IDF scores for all query terms in the document
                tfidf_scores[doc_id] += tfidf_query[token] * tfidf_doc[token]

    # Sort documents by total TF-IDF score
    ranked = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    ranked_docs = [doc_id for doc_id, _ in ranked]

    return ranked_docs

# load previous inverted_index if exist
inverted_index = load_json()
doc_id = load_json("doc_id.json")


# Use to obtain query input from user through Web GUI,
# Same as the While loop
def web_search(user_input):
    result = AND_search(user_input, inverted_index)
    search_results = []
    count = 0
    visited_urls = set()
    for v in result:
        url = doc_id[v]
        parsed_url = urlparse(url)
        # Remove file extension from the path/ removing duplicates (need testing)
        path_without_extension = re.sub(r'\.\w+$', '', parsed_url.path)
        normalized_url = urlunparse(parsed_url._replace(path=path_without_extension, fragment='', query=''))
        # normalized_url = url.split('#')[0].rstrip('/')
        if not re.search(r'\.\w+$', normalized_url) and normalized_url not in visited_urls:
            # summary = summarize_url(normalized_url)
            search_results.append(normalized_url)
            # {'url':path_without_extension, 'summary': summary})
            visited_urls.add(normalized_url)
            count += 1
        if count >= 10:  # Limit to top 10 unique URLs
            break
    return search_results


# use to search index through cmd
def cmd_search():
    while True:

        user_input = input("Enter your inputs (Q to quit): ")

        if user_input.lower() != "q":
            start_time = time.time()
            result = AND_search(user_input, inverted_index)
            search_time = (time.time() - start_time) * 1000
            print(f"This search took {search_time:.2f} ms")
            if len(result) == 0:
                print("No results found!!! An lesser strict 'OR-search' is going to be performed.")
                print("The search result would be less relevant than normal")
                start_time = time.time()
                result = OR_search(user_input, inverted_index)
                search_time = (time.time() - start_time) * 1000
                print(f"Additional OR search took {search_time:.2f} ms")
                if len(result) == 0:
                    print("Still No results found!!!")
                    continue

            print(f"Top 10 search result for {user_input} (Attempting Sorting):")
            count = 0
            visited_urls = set()
            for v in result:
                url = doc_id[v]
                parsed_url = urlparse(url)
                # Remove file extension from the path/ removing duplicates (need testing)
                path_without_extension = re.sub(r'\.\w+$', '', parsed_url.path)
                # normalized_url = urlunparse(parsed_url._replace(fragment='', query='')) removing fragments/duplicates
                if path_without_extension not in visited_urls:
                    print(url)
                    visited_urls.add(path_without_extension)
                    count += 1
                if count >= 10:  # Limit to top 10 unique URLs
                    break
        else:
            break
            
if __name__ == "__main__":
    cmd_search()
