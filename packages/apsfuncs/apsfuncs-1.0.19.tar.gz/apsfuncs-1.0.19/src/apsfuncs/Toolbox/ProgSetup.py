import os, datetime, logging

from apsfuncs.Toolbox.ConfigHandlers import get_logs_path

# Funcion to set up and return a logger (and clear excess logs)
def gen_logger(log_identifier):
    # Create the log file path and name
    dt = datetime.datetime.now()
    log_path = get_logs_path()
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    filename = log_identifier + "_" + str(dt.year) + "_" + str(dt.month) + "_" + str(dt.day) + "_" + str(dt.hour) + str(dt.minute) + str(dt.second) + ".log"
    log_name = log_path + "\\" + filename

    # Create the logger and start it using the new log name
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(message)s', filename=log_name, level=logging.INFO)
    logger.info('Started')

    # Check how many log files already exist, if there are more than 15 then delete the oldest ones until only 15 remain
    log_list = os.listdir(log_path)
    while len(log_list) > 15:
        log_paths = [log_path+"\\{0}".format(log) for log in log_list]
        oldest_file = min(log_paths, key=os.path.getctime)
        os.remove(oldest_file)
        log_list = os.listdir(log_path)

    return logger, filename