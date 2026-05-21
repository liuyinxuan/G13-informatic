# Mini Search Engine

A small information retrieval project that implements a basic search engine for HTML/web document collections. The project includes document parsing, text preprocessing, inverted index construction, Boolean retrieval, ranking with term-based scoring, and a simple search interface.

This repository combines two development milestones:

- **Milestone 2:** Search and retrieval component
- **Milestone 3:** Complete search engine with improved ranking and evaluation

The project was developed as part of an Information Retrieval course project.

## Team members
* Phuong Luong @pluong3
    - NetID: pluong3 
    - Student ID:62887840
    
* Yinxuan Liu @yinxual1
    - NetID: yinxual1
    - Student ID:70861360 
 
* Robin Stoebe @cstoebe
    - NetID: cstoebe
    - Student ID:63085315
    
* Navid Sharmsar @nsharmsa
    - NetID: nsharmsa
    - Student ID:66353809


## Overview

The goal of this project is to build a functional search engine that can retrieve relevant documents from a collection of HTML pages. The system processes raw HTML content, extracts useful text, builds an inverted index, and allows users to search for documents using keyword queries.

The search engine supports Boolean-style retrieval, especially `AND` queries, and can be extended with ranking methods such as TF-IDF and cosine similarity. The final version also focuses on improving query performance, ranking quality, and runtime efficiency.

## Features

- HTML parsing using BeautifulSoup
- Text preprocessing with NLTK
- Tokenization and stopword removal
- Inverted index construction
- TF-IDF based document ranking
- Query evaluation using selected test queries
- Search interface for interactive retrieval
- Query improvement through general retrieval heuristics

## Technologies Used

- Python
- BeautifulSoup
- NLTK
- TF-IDF / cosine similarity concepts
- Inverted index data structure
- Basic information retrieval techniques
