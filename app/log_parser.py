from __future__ import division

import os
import glob
import re
from config import GAME_LOG_PATH


class LogParser:
    def __init__(self):
        self.day = 0
        self.day_failed = None
        self.status = True
        self.games = {}
        self.agents = {}
        self.line = ''

    @staticmethod
    def numerical_sort(afilename):
        nondigits = re.compile("\D")
        return int(nondigits.sub("", afilename))

    def get_game_logs(self):
        return sorted(glob.glob(os.path.join(GAME_LOG_PATH, "*.txt")), key=self.numerical_sort)

    def add_agent_to_list(self):
        agent_name = self.line.split(":")[0]
        if agent_name not in self.agents:
            self.agents[agent_name] = {
                'status': True,
                'campaigns': [],
                'balances': [],
                'ucs_levels': [],
                'daily_cost_per_imp': [],
                'total_imps': [],
                'qualities': [],
            }

    def parse_logs(self):
        game_counter = 0
        sets_counter = 1
        for logfile in self.get_game_logs():
            game_counter += 1
            if game_counter in [5, 9, 13]:
                sets_counter += 1
            self.parse_log(logfile, sets_counter)
        return self.games

    def set_day(self):
        self.day = int(self.line.split(":")[1].strip().split(" ")[0])

    def set_bank_balance(self):
        for agent, stats in self.agents.iteritems():
            if agent in self.line:
                self.agents[agent]['balances'].append(round(float(self.line.split(":")[1].strip()), 2))

    def set_campaign(self):
        for agent, stats in self.agents.iteritems():
            if agent in self.line:
                campaign = int(
                        self.line.split(":")[1].split("Targeted Impressions")[0].strip().split(" ")[0].replace("#", ""))
                if campaign not in self.agents[agent]['campaigns']:
                    self.agents[agent]['campaigns'].append(campaign)

    def set_ucs_level(self):
        for agent, stats in self.agents.iteritems():
            if agent in self.line:
                self.agents[agent]['ucs_levels'].append(round(float(self.line.split(":")[1].strip()), 2))

    def set_daily_cost_per_imp(self):
        for agent, stats in self.agents.iteritems():
            if agent in self.line:
                imps_arr = self.line.split("Targeted Impressions: ")[1].split("	")[0].strip().split(".")
                daily_imps = float(imps_arr[0][0:5] + "." + imps_arr[1][0:5])
                if len(self.agents[agent]['total_imps']) == 0:
                    self.agents[agent]['total_imps'].append(daily_imps)
                else:
                    self.agents[agent]['total_imps'].append(self.agents[agent]['total_imps'][-1] + daily_imps)
                daily_cost = float(self.line.split("Cost: ")[1].strip()[0:6])

                if daily_imps != 0.0 and daily_cost != 0.0:
                    cost_per_imp = round(daily_cost / daily_imps, 4)
                    if cost_per_imp != 0.0:
                        self.agents[agent]['daily_cost_per_imp'].append(cost_per_imp)

    def set_quality(self):
        for agent, stats in self.agents.iteritems():
            if agent in self.line:
                quality_rating = round(float(self.line.split(":")[1].strip()), 2)
                self.agents[agent]['qualities'].append(quality_rating)
                if self.agents[agent]['status'] is True:
                    if quality_rating < 0.31:
                        self.agents[agent]['day_reached'] = self.day
                        self.agents[agent]['status'] = False
                    else:
                        self.agents[agent]['day_reached'] = self.day

    def parse_log(self, logfile, sets_counter):
        self.day = 0
        self.agents = {}
        self.line = ''

        with open(logfile, 'r') as game_log:
            # # game_name = logfile.split("_")[1].split(".")[0]
            for i, self.line in enumerate(game_log):
                if i in range(7, 15):
                    self.add_agent_to_list()
                if 'Next day' in self.line:
                    self.set_day()
                elif 'Bank balance:' in self.line:
                    self.set_bank_balance()
                elif 'Quality rating:' in self.line:
                    self.set_quality()
                elif 'UCS level:' in self.line:
                    self.set_ucs_level()
                elif 'Campaign report:' in self.line:
                    self.set_campaign()
                    self.set_daily_cost_per_imp()
            if sets_counter not in self.games:
                self.games[sets_counter] = [self.agents]
            else:
                self.games[sets_counter].append(self.agents)


if __name__ == '__main__':
    log_parser = LogParser()
    log_parser.parse_logs()
    counter = 0

    for game in log_parser.games:
        counter += 1
        for agent_name, agent_stats in game.iteritems():
            print(
                agent_name,
                agent_stats['balances'],
                # agent_stats['campaigns'],
                # agent_stats['balances'],
                # agent_stats['ucs_levels'],
                # agent_stats['daily_cost_per_imp'],
                # agent_stats['total_imps'],
                # agent_stats['qualities'],
            )
