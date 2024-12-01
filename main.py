import database
from wrappers import extract_cv, extract_cle, extract_eus
from dotenv import load_dotenv

load_dotenv()
database.clean_database()
database.create_database()
extract_eus()
extract_cv()
extract_cle()