import database
import utils.remove_logs
from wrappers import extract_cv, extract_cle, extract_eus
from dotenv import load_dotenv
from utils import logger

logger = logger.MyLogger()

load_dotenv()
database.clean_database()
database.create_database()
extract_eus()
extract_cv()
extract_cle()

logger.get_counts()