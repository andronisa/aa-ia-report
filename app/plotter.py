# !/usr/bin/env python
from __future__ import division
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))


class Plotter:
    def __init__(self):
        pass

    def plot_top_ten_categories(self):
        def percentage(part, whole):
            return int(100 * float(part) / float(whole))

        def calculate_rest_count(categories, whole):
            sum = 0
            for item in categories:
                sum += item['count']
                return sum

        pipeline = [
            {"$unwind": "$categories"},
            {"$group": {"_id": "$categories", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 9}
        ]

        col_name = 'review_category'

        fracs = []
        category_labels = []
        should_explode = True
        should_append_rest = True
        expl = []

        for category in categories:
            if should_explode:
                expl.append(0.1)
                should_explode = False
            else:
                expl.append(0)

            review_count = category['count']

            if review_count < rest_count and should_append_rest:
                fracs.append(percentage(rest_count, total_categories_no))
                category_labels.append("Others")
                expl.append(0)

                should_append_rest = False

            fracs.append(percentage(review_count, total_categories_no))
            category_labels.append(category['_id'])

        labels = tuple(category_labels)
        explode = tuple(expl)

        # make a square figure and axes
        figure(1, figsize=(6, 6))
        ax = axes([0.1, 0.1, 0.8, 0.8])

        pie(fracs, colors=colors, explode=explode, labels=labels,
            autopct='%1.1f%%', shadow=True, startangle=90)
        # The default startangle is 0, which would start
        # the Frogs slice on the x-axis.  With startangle=90,
        # everything is rotated counter-clockwise by 90 degrees,
        # so the plotting starts on the positive y-axis.
        mpl.rcParams['font.size'] = 15.0
        title('Top Business Categories', bbox={'facecolor': '0.8', 'pad': 5})

        show()

    def plot_top_ten_businesses_of_top_category(self):
        def percentage(part, whole):
            return int(100 * float(part) / float(whole))

        top_category = self.find_top_category()
        top_ten_business_id_docs = self.find_top_businesses_of_category(top_category, 3)

        businesses_for_plot = []
        total = 0
        for item in top_ten_business_id_docs:
            business_id = item['_id']
            bus_count = item['count']
            total += bus_count

            business_name = self.query.find_one('business', [('business_id', business_id)], ['name'])['name']
            businesses_for_plot.append((bus_count, business_name))

        category_labels = []
        should_explode = True
        counts = []
        expl = []

        leength = len(businesses_for_plot)
        colors = cm.Set1(np.arange(len(businesses_for_plot)) / leength)

        for count, name in businesses_for_plot:
            if should_explode:
                expl.append(0.1)
                should_explode = False
            else:
                expl.append(0)

            counts.append(count)

            category_labels.append(name)

        labels = tuple(category_labels)
        business_counts = tuple(counts)
        ind = np.arange(3)  # the x locations for the groups
        width = 0.35  # bar width

        fig, ax = plt.subplots()

        rects1 = ax.bar(ind, business_counts,  # data
                        width,  # bar width
                        color=colors,  # bar colour
                        error_kw={'ecolor': 'Tomato',  # error-bars colour
                                  'linewidth': 2})  # error-bar width

        axes = plt.gca()
        axes.set_ylim([0, 5000])  # y-axis bounds

        ax.set_ylabel('Reviews')
        ax.set_title('Most Popular Businesses')
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels(labels)

        rect_tuple = tuple(rects1)

        ax.legend(rect_tuple, labels)
        params = {'legend.fontsize': 25,
                  'legend.linewidth': 3}
        mpl.rcParams.update(params)

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                        '%d' % int(height),
                        ha='center',  # vertical alignment
                        va='bottom'  # horizontal alignment
                        )

        autolabel(rects1)

        plt.show()

    def plot_bus(self, result):
        category_labels = []
        counts = []
        colors = cm.Set1(np.arange(len(result)) / len(result))

        for name, count in result:
            counts.append(count)
            name_arr = name.split(" ")
            if len(name_arr) > 1:
                category_labels.append(name_arr[0])
            else:
                category_labels.append(name)

        labels = tuple(category_labels)
        business_counts = tuple(counts)
        ind = np.arange(len(result))  # the x locations for the groups
        width = 0.35  # bar width

        fig, ax = plt.subplots()

        rects1 = ax.bar(ind, business_counts,  # data
                        width,  # bar width
                        color=colors,  # bar colour
                        error_kw={'ecolor': 'Tomato',  # error-bars colour
                                  'linewidth': 2})  # error-bar width

        axes = plt.gca()
        axes.set_ylim([0, 3])  # y-axis bounds

        ax.set_ylabel('Occurences')
        ax.set_title('Complained keywords')
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels(labels)

        rect_tuple = tuple(rects1)

        ax.legend(rect_tuple, labels)

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                        '%d' % int(height),
                        ha='center',  # vertical alignment
                        va='bottom'  # horizontal alignment
                        )

        autolabel(rects1)

        plt.show()

    def bar_plot(result, title):
        OX = [
            'MinMax',
            'Alpha Beta',
            'Tie'
        ]

        mm = result['mm_wins']
        ab = result['ab_wins']
        ties = result['ties']

        OY = [mm, ab, ties]

        fig = plt.figure()

        width = .20
        ind = np.arange(len(OY))
        barlist = plt.bar(ind, OY, align='center')
        plt.xticks(ind + width / 2, OX)

        barlist[0].set_color('r')
        barlist[1].set_color('b')
        barlist[2].set_color('g')
        plt.legend((barlist[0], barlist[1], barlist[2]),
                   ('MinMax Wins: ' + str(mm), 'AlphaBeta Wins: ' + str(ab), 'Ties: ' + str(ties)))

        plt.xlabel('Result')
        plt.ylabel('Wins Count')
        plt.title(title)
        plt.show()

    def plot_times(result, limit=None, title=None):
        bfs = result['bfs']
        id_dfs = result['id_dfs']
        a_star = result['a_star']

        bfs_average = sum(bfs) / len(bfs)
        id_dfs_average = sum(id_dfs) / len(id_dfs)
        a_star_average = sum(a_star) / len(a_star)

        lines = plt.plot(bfs, 'xr-', id_dfs, 'xb-', a_star, 'xg-', linewidth=3)

        plt.legend((lines[0], lines[1], lines[2]),
                   ('BFS: ' + str(bfs_average) + " seconds",
                    'IDDFS: ' + str(id_dfs_average) + " seconds",
                    'A*: ' + str(a_star_average) + " seconds"),
                   loc=1)

        plt.xlabel('Time(seconds)')
        plt.ylabel('Times tried')
        if title:
            plt.title(title)

        if limit:
            x1, x2, y1, y2 = plt.axis()

            plt.axis((x1, x2, 0, limit))

        plt.show()


if __name__ == '__main__':
    plotter = Plotter()
    # plotter.plot_buses()

    # plotter.plot_top_ten_categories()
    plotter.plot_top_ten_businesses_of_top_category()
