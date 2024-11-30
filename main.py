import database
from wrappers import pass_data_to_service  

database.clean_database()
database.create_database()
pass_data_to_service()