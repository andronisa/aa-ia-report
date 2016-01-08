# !/usr/bin/env python
from __future__ import division
import os
import time
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from log_parser import LogParser
from pylab import *

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))


class Plotter:
    def __init__(self):
        pass

    def bar_plot_qualities(self, game_set, title='Quality'):
        total_agent_qualities = {}
        agent_labels = []
        agent_qualities = []

        for game in game_set:
            for agent, stats in game.iteritems():
                if agent not in total_agent_qualities:
                    total_agent_qualities[agent] = stats['qualities']
                else:
                    total_agent_qualities[agent].extend(stats['qualities'])

        for agentname, qualities in total_agent_qualities.iteritems():
            agent_labels.append(agentname)
            agent_qualities.append(sum(qualities) / len(qualities))

        colors = plt.get_cmap('jet')(np.linspace(0.1, 1.2, 8))

        labels = tuple(agent_labels)
        qualities = tuple(agent_qualities)
        ind = np.arange(len(total_agent_qualities))  # the x locations for the groups
        width = 0.35  # bar width

        fig, ax = plt.subplots()

        rects1 = ax.bar(ind, qualities,  # data
                        width,  # bar width
                        color=colors,  # bar colour
                        error_kw={'ecolor': 'Tomato',  # error-bars colour
                                  'linewidth': 1})  # error-bar width

        axes = plt.gca()
        axes.set_ylim([0, 1.7])  # y-axis bounds

        ax.set_ylabel('Quality rating')
        ax.set_title(title)
        ax.set_xticks(ind + width)
        ax.set_xticklabels(labels)

        rect_tuple = tuple(rects1)

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                        '%g' % height,
                        ha='center',  # vertical alignment
                        va='bottom'  # horizontal alignment
                        )

        autolabel(rects1)

        ax.legend(rect_tuple, labels)

        plt.show()

    def bar_plot_days_stayed(self, game_set, title='Average days until dropped off'):
        total_agent_qualities = {}
        agent_labels = []
        agent_qualities = []

        for game in game_set:
            for agent, stats in game.iteritems():
                if agent not in total_agent_qualities:
                    total_agent_qualities[agent] = [stats['day_reached']]
                else:
                    total_agent_qualities[agent].append(stats['day_reached'])

        for agentname, qualities in total_agent_qualities.iteritems():
            agent_labels.append(agentname)
            agent_qualities.append(sum(qualities) / len(qualities))

        colors = plt.get_cmap('jet')(np.linspace(0.1, 1.2, 8))

        labels = tuple(agent_labels)
        qualities = tuple(agent_qualities)
        ind = np.arange(len(total_agent_qualities))  # the x locations for the groups
        width = 0.35  # bar width

        fig, ax = plt.subplots()

        rects1 = ax.bar(ind, qualities,  # data
                        width,  # bar width
                        color=colors,  # bar colour
                        error_kw={'ecolor': 'Tomato',  # error-bars colour
                                  'linewidth': 1})  # error-bar width

        axes = plt.gca()
        axes.set_ylim([0, 65])  # y-axis bounds

        ax.set_ylabel('Days')
        ax.set_title(title)
        ax.set_xticks(ind + width)
        ax.set_xticklabels(labels)

        rect_tuple = tuple(rects1)

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                        '%g' % height,
                        ha='center',  # vertical alignment
                        va='bottom'  # horizontal alignment
                        )

        autolabel(rects1)

        ax.legend(rect_tuple, labels)

        plt.show()

    def bar_plot_ucs_levels(self, game_set):
        total_agent_ucs_lvls = {}
        agent_labels = []
        agent_ucs_lvls = []

        for game in game_set:
            for agent, stats in game.iteritems():
                if agent not in total_agent_ucs_lvls:
                    total_agent_ucs_lvls[agent] = [stats['ucs_levels']]
                else:
                    total_agent_ucs_lvls[agent].append(stats['ucs_levels'])

        for agentname, qualities in total_agent_ucs_lvls.iteritems():
            agent_labels.append(agentname)
            agent_ucs_lvls.append(sum(qualities) / len(qualities))

        colors = plt.get_cmap('jet')(np.linspace(0.1, 1.2, 8))

        labels = tuple(agent_labels)
        qualities = tuple(agent_ucs_lvls)
        ind = np.arange(len(total_agent_ucs_lvls))  # the x locations for the groups
        width = 0.35  # bar width

        fig, ax = plt.subplots()

        rects1 = ax.bar(ind, qualities,  # data
                        width,  # bar width
                        color=colors,  # bar colour
                        error_kw={'ecolor': 'Tomato',  # error-bars colour
                                  'linewidth': 1})  # error-bar width

        axes = plt.gca()
        axes.set_ylim([0, 65])  # y-axis bounds

        ax.set_ylabel('Days')
        ax.set_title('Average days in the game')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(labels)

        rect_tuple = tuple(rects1)

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                        '%g' % height,
                        ha='center',  # vertical alignment
                        va='bottom'  # horizontal alignment
                        )

        autolabel(rects1)

        ax.legend(rect_tuple, labels)

        plt.show()

    def bar_plot_total_won_per_set(self, game_set, title='Campaigns Won'):
        total_agent_campaigns = {}
        agent_labels = []
        agent_campaigns = []

        for game in game_set:
            for agent, stats in game.iteritems():
                if agent not in total_agent_campaigns:
                    total_agent_campaigns[agent] = [len(stats['campaigns'])]
                else:
                    total_agent_campaigns[agent].append(len(stats['campaigns']))

        for agentname, campaigns in total_agent_campaigns.iteritems():
            agent_labels.append(agentname)
            agent_campaigns.append(sum(campaigns))

        colors = plt.get_cmap('jet')(np.linspace(0.1, 1.2, 8))

        labels = tuple(agent_labels)
        campaigns = tuple(agent_campaigns)
        ind = np.arange(len(total_agent_campaigns))  # the x locations for the groups
        width = 0.35  # bar width

        fig, ax = plt.subplots()

        rects1 = ax.bar(ind, campaigns,  # data
                        width,  # bar width
                        color=colors,  # bar colour
                        error_kw={'ecolor': 'Tomato',  # error-bars colour
                                  'linewidth': 1})  # error-bar width

        # axes = plt.gca()
        # axes.set_ylim([0, 65])  # y-axis bounds

        ax.set_ylabel('Campaigns Won')
        ax.set_title(title)
        ax.set_xticks(ind + width)
        ax.set_xticklabels(labels)

        rect_tuple = tuple(rects1)

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                        '%g' % height,
                        ha='center',  # vertical alignment
                        va='bottom'  # horizontal alignment
                        )

        autolabel(rects1)

        ax.legend(rect_tuple, labels)

        plt.show()

    def bar_plot_days_stayed_vs_total(self, game_set):
        total_agent_qualities = {'MrSmith': [], 'Rest of the agents': []}
        agent_labels = []
        agent_qualities = []

        for game in game_set:
            for agent, stats in game.iteritems():
                if agent != "MrSmith":
                    total_agent_qualities['Rest of the agents'].append(stats['day_reached'])
                else:
                    total_agent_qualities['MrSmith'].append(stats['day_reached'])

        for agentname, qualities in total_agent_qualities.iteritems():
            agent_labels.append(agentname)
            agent_qualities.append(sum(qualities) / len(qualities))

        colors = plt.get_cmap('jet')(np.linspace(0.1, 1.2, 8))

        labels = tuple(agent_labels)
        qualities = tuple(agent_qualities)
        ind = np.arange(len(total_agent_qualities))  # the x locations for the groups
        width = 0.35  # bar width

        fig, ax = plt.subplots()

        rects1 = ax.bar(ind, qualities,  # data
                        width,  # bar width
                        color=colors,  # bar colour
                        error_kw={'ecolor': 'Tomato',  # error-bars colour
                                  'linewidth': 1})  # error-bar width

        axes = plt.gca()
        axes.set_ylim([0, 65])  # y-axis bounds

        ax.set_ylabel('Days')
        ax.set_title('Average days until dropped off vs average of all the others')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(labels)

        rect_tuple = tuple(rects1)

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                        '%g' % height,
                        ha='center',  # vertical alignment
                        va='bottom'  # horizontal alignment
                        )

        autolabel(rects1)

        ax.legend(rect_tuple, labels)

        plt.show()

    def plot_quality_lines(self, game_set):
        colors = plt.get_cmap('jet')(np.linspace(0.1, 1.2, 8))
        for game in game_set:
            agent_labels = []
            total_plots = []

            counter = 0
            for agent, stats in game.iteritems():
                color = colors[counter]
                qualities = stats['qualities']
                agent_labels.append(agent)
                plot, = plt.plot(qualities, linewidth=1, color=color)
                total_plots.append(plot)

                counter += 1

            plt.legend(total_plots, agent_labels, loc=1)

            plt.xlabel('Days')
            plt.ylabel('Quality')
            plt.title("Quality Game 10")
            x1, x2, y1, y2 = plt.axis()

            plt.axis((x1, x2, 0, 2))
            plt.show()
            return

    def plot_balance_lines(self, game_set):
        colors = plt.get_cmap('jet')(np.linspace(0.1, 1.2, 8))
        for game in game_set:
            agent_labels = []
            total_plots = []

            counter = 0
            for agent, stats in game.iteritems():
                color = colors[counter]
                balances = stats['balances']
                agent_labels.append(agent)
                plot, = plt.plot(balances, linewidth=1, color=color)
                total_plots.append(plot)

                counter += 1

            plt.legend(total_plots, agent_labels, loc=3)

            plt.xlabel('Days')
            plt.ylabel('Balance')
            plt.title("Bank Game 10")
            plt.show()

    def plot_ucs_levels(self, game_set):
        for game in game_set:
            agent_labels = []
            total_plots = []

        colors = plt.get_cmap('jet')(np.linspace(0.1, 1.2, 8))
        counter = 0
        for agent, stats in game.iteritems():
            color = colors[counter]
            ucs_levels = stats['ucs_levels']

            agent_labels.append(agent)
            plot, = plt.plot(ucs_levels, linewidth=1, color=color)
            total_plots.append(plot)

            counter += 1

        plt.legend(total_plots, agent_labels, loc=2)

        plt.xlabel('Games')
        plt.ylabel('Number of Iterations')
        plt.title('foobar')
        plt.show()


if __name__ == '__main__':
    parser = LogParser()
    results = parser.parse_logs()
    plotter = Plotter()
    for game_set, games in results.iteritems():
        plotter.plot_quality_lines(games)
        plotter.plot_balance_lines(games)
        plotter.bar_plot_days_stayed(games)
        plotter.bar_plot_days_stayed_vs_total(games)
        plotter.bar_plot_ucs_levels(games)
        plotter.bar_plot_qualities(games)

        if game_set == 3:
            game = games[1]
            plotter.plot_quality_lines([game])
            plotter.plot_balance_lines([game])
            plotter.bar_plot_total_won_per_set([game])
            plotter.bar_plot_days_stayed([game])
