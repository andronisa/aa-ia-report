import os
import glob
from config import GAME_LOG_PATH, PLOT_PATH


class LogParser:
    def __init__(self):
        pass

    @staticmethod
    def read_log():
        for file_name in glob.glob(os.path.join(GAME_LOG_PATH, "*.txt")):
            print(file_name)
            # for file in


class GameLog:
    def __init__(self):
        pass


if __name__ == '__main__':
    log_parser = LogParser()
    log_parser.read_log()
