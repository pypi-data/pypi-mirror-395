#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from __future__ import print_function

import argparse
import matplotlib.pyplot as plt  # to start
import matplotlib

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 


def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--font-scale', help="default=0.6", default=0.6)
    parser.add_argument('--sep', help="sep for input file, default=' '", default=" ")
    parser.add_argument('--annot', help="annotate squares, default=False",
                        action="store_true", default=False)
    parser.add_argument('--plot', help="output plot, default=_plot_.png", default="_plot_.png")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")
    parser.add_argument("file", help="", default="") # nargs='+')

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()


    matplotlib.rcParams['lines.linewidth'] = 10

    df = pd.read_csv(args.file,
                     sep=args.sep, index_col=False)#, index=False)
    df = df.set_index(df.columns)
    print(df)
    #df = df.drop('Unnamed: 15', axis=1)

    # plt.figure(figsize=(10,10))
    sns.set(font_scale=float(args.font_scale))
    plt.style.use('dark_background')
    g = sns.clustermap(df, cmap="bwr", annot=args.annot, #col_cluster=False,
                       figsize=(10, 10))#, standard_scale=0.8)#, linecolor = 'black', 
                           #linewidths=.3)#, vmin=-6, vmax=+6) # , 
    for a in g.ax_row_dendrogram.collections:
        a.set_linewidth(1)
        a.set_color('orange')
    for a in g.ax_col_dendrogram.collections:
        a.set_linewidth(1)
        a.set_color('orange')

    print(g.dendrogram_col.linkage)  # https://stackoverflow.com/questions/52915963/extract-dendrogram-from-seaborn-clustermap

    plt.savefig(args.plot, dpi=300, transparent=True)
