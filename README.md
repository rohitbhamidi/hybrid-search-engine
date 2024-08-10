# Hybrid Search Engine

## Overview
The Hybrid Search Engine is designed to combine full-text search capabilities with vector-based similarity search. The system leverages BM25 for full-text search and FAISS for vector similarity search, combining the results using Reciprocal Rank Fusion (RRF). It also integrates with S3 cloud object storage for long-term storage of data segments.

## Features
- **Core Database Functionality**
  - Data storage and retrieval
  - Auto-assigned IDs for data insertion
  - Versioned data handling

- **Full-Text Search with BM25**
  - Implements BM25Okapi from `rank_bm25`

- **Vector Search with FAISS**
  - Uses FAISS for vector-based search

- **Hybrid Search Combining Both Methods**
  - Combines results using Reciprocal Rank Fusion (RRF)

- **Basic Transaction Logging**
  - Logs database operations

## Extended Features (Post-MVP)
- Transaction management with commit and rollback
- Backup and restore functionality using AWS S3
- Vector embedding generation via OpenAI API
- Comprehensive unit and integration testing

## Project Structure
```
hybrid-search-engine/
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
├── scripts
│   ├── insert_data.py
│   └── perform_hybrid_search.py
├── src
│   ├── __init__.py
│   ├── database.py
│   ├── faiss_search.py
│   ├── fulltext_search.py
│   ├── hybrid_search.py
│   ├── transaction_log.py
│   └── versioned_data.py
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── test_database.py
    ├── test_faiss_search.py
    ├── test_fulltext_search.py
    ├── test_hybrid_search.py
    ├── test_transaction_log.py
    └── test_versioned_data.py
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hybrid-search-engine.git
   cd hybrid-search-engine
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Insert Data
To insert data into the database, run:
```bash
python scripts/insert_data.py
```

### Perform Hybrid Search
To perform a hybrid search, run:
```bash
python scripts/perform_hybrid_search.py
```

## Testing
Run the test suite using:
```bash
pytest
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.