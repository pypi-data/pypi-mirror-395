from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
SOURCES_DIR = PROJECT_ROOT / 'sources'
SCRAPING_DIR = PROJECT_ROOT / 'scraping'

load_dotenv(PROJECT_ROOT / '.env')

GET_SEGMENTS_FOR_LEMMA_EXPECTED_AVERAGE_SECONDS = 5
FREQUENT_CONTEXTS_EXPECTED_AVERAGE_SECONDS = 5


db_config = {
    "user": os.getenv("DATABASE_USERNAME"),
    "password": os.getenv("DATABASE_PASSWORD"),
    "host": os.getenv("DATABASE_IP"),
    "port": os.getenv("DATABASE_PORT"),
    "database": os.getenv("DATABASE_NAME")
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from .db_manager import DBManager
from .source_parser import Parser
from .n_gram_collector import NGramCollector
