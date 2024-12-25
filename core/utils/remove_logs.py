import os

def removeLogs():
    root_directory = os.getcwd()
    logger_directory = os.path.join(root_directory, "logs")
    if not os.path.exists(logger_directory):
        os.makedirs(logger_directory)
    for file in os.listdir(logger_directory):
        if file.endswith(".log"):
            os.remove(os.path.join(logger_directory, file))

removeLogs()