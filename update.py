# -*- coding: utf-8 -*-
""" Update Readme.md and cumulative_gans.jpg """
from __future__ import print_function
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import csv


def load_data():
    """ Load GANs data from the gans.csv file """

    with open('gans.tsv') as fid:
        reader = csv.DictReader(fid, delimiter='\t')
        gans = [row for row in reader]
    return gans


def update_readme(gans):
    """ Update the Readme.md text file from a Jinja2 template """
    import jinja2 as j2

    gans.sort(key=lambda v: v['Abbr.'].upper())
    j2_env = j2.Environment(loader=j2.FileSystemLoader('.'),
                            trim_blocks=True, lstrip_blocks=True)

    with open('README.md', 'w') as fid:
        print(j2_env.get_template('README.j2.md').render(gans=gans), file=fid)


def update_figure(gans):
    """ Update the figure cumulative_gans.jpg """
    data = np.array([int(gan['Year']) + int(gan['Month']) / 12
                     for gan in gans])
    x_range = int(np.ceil(np.max(data) - np.min(data)) * 12) + 1
    y_range = int(np.ceil(data.size / 10)) * 10 + 1

    with plt.style.context("seaborn"):
        plt.hist(data, x_range, cumulative="True")
        plt.xticks(range(2014, 2019))
        plt.yticks(np.arange(0, y_range, 15))
        plt.title("Cumulative number of named GAN papers by month")
        plt.xlabel("Year")
        plt.ylabel("Total number of papers")
        plt.savefig('cumulative_gans.jpg')

def update_github_stats(gans):
    """ Update Github stats """
    num_rows = len(gans)
    print('Fetching Github stats...')
    for i, gan in enumerate(gans):
        url = gan['Official_Code']
        if url != "-" and url != "":
            print(str(i) + '/' + str(num_rows))
            result = requests.get(url)
            c = result.text
            soup = BeautifulSoup(c, "html.parser")
            samples = soup.select("a.social-count")
            gan['Watches'] = samples[0].get_text().strip().replace(",", "")
            gan['Stars'] = samples[1].get_text().strip().replace(",", "")
            gan['Forks'] = samples[2].get_text().strip().replace(",", "")

    print(str(i) + '/' + str(num_rows))
    print('Complete.')
    
    with open('gans.tsv', 'w') as outfile:
        fp = csv.DictWriter(outfile, gans[0].keys(), delimiter='\t')
        fp.writeheader()
        fp.writerows(gans)

if __name__ == '__main__':
    GANS = load_data()
    update_readme(GANS)
    update_figure(GANS)
    update_github_stats(GANS)
