import os
import glob
from config import GAME_LOG_PATH, PLOT_PATH


class LogParser:
    def __init__(self):
        self.day = 0
        self.day_failed = None
        self.status = True
        self.games = []
        self.agents = {}
        self.line = ''

    @staticmethod
    def get_game_logs():
        return glob.glob(os.path.join(GAME_LOG_PATH, "*.txt"))

    def add_agent_to_list(self):
        agent_name = self.line.split(":")[0]
        if agent_name not in self.agents:
            self.agents[agent_name] = {
                'status': True,
                'campaigns': []
            }

    def parse_logs(self):
        for logfile in self.get_game_logs():
            self.parse_log(logfile)

    def set_day(self):
        self.day = int(self.line.split(":")[1].strip().split(" ")[0])

    def set_bank_balance(self):
        for agent, stats in self.agents.iteritems():
            if agent in self.line and self.agents[agent]['status']:
                self.agents[agent]['bank_balance'] = round(float(self.line.split(":")[1].strip()), 2)

    def set_campaign_report(self):
        for agent, stats in self.agents.iteritems():
            if agent in self.line and self.agents[agent]['status']:
                campaign = int(
                        self.line.split(":")[1].split("Targeted Impressions")[0].strip().split(" ")[0].replace("#", ""))
                if campaign not in self.agents[agent]['campaigns']:
                    self.agents[agent]['campaigns'].append(campaign)

    def set_quality(self):
        for agent, stats in self.agents.iteritems():
            if agent in self.line:
                quality_rating = round(float(self.line.split(":")[1].strip()), 2)
                if quality_rating < 0.31 and self.agents[agent]['status'] is True:
                    self.agents[agent]['day_reached'] = self.day
                    self.agents[agent]['status'] = False
                elif quality_rating > 0.31 and self.agents[agent]['status'] is False:
                    self.agents[agent]['status'] = True
                    self.agents[agent]['day_reached'] = self.day
                elif quality_rating > 0.31 and self.agents[agent]['status'] is True:
                    self.agents[agent]['day_reached'] = self.day
                self.agents[agent]['quality_rating'] = quality_rating

    def parse_log(self, logfile):
        with open(logfile, 'r') as game_log:
            # game_name = logfile.split("_")[1].split(".")[0]
            for i, self.line in enumerate(game_log):
                if i in range(7, 15):
                    self.add_agent_to_list()
                if 'Next day' in self.line:
                    self.set_day()
                if 'Bank balance:' in self.line:
                    self.set_bank_balance()
                if 'Quality rating:' in self.line:
                    self.set_quality()
                if 'Campaign report:' in self.line:
                    self.set_campaign_report()
            self.games.append(self.agents)


class GameLog:
    def __init__(self):
        pass


if __name__ == '__main__':
    log_parser = LogParser()
    log_parser.parse_logs()
    for game in log_parser.games:
        for agent, stats in game.iteritems():
            print(agent, stats)
