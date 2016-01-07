import os
import glob
from config import GAME_LOG_PATH, PLOT_PATH


class LogParser:
    def __init__(self):
        pass

    @staticmethod
    def get_game_logs():
        return glob.glob(os.path.join(GAME_LOG_PATH, "*.txt"))

    def parse_logs(self):
        for game_log in self.get_game_logs():
            print(game_log)


class GameLog:
    def __init__(self):
        pass


if __name__ == '__main__':
    log_parser = LogParser()
    log_parser.parse_logs()
