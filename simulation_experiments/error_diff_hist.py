# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import numpy
import matplotlib.pyplot as pyplot
import numpy as np
import pandas

from plot_utils import colorbar, get_autocorrelation
from pathlib import Path

label_size = 13
tick_size = 12

seed = str(0)
num_runs = 10000
est_list = ['OLS'] #, 'Ridge', 'Lasso', 'ElasticNet']
order_list = [3, 5, 7]
num_samples_train = 100
omega = 1

img_prefix = '../img/uai/all_orders/'
data_suffix = '_' + str(num_runs) + '_' + str(num_samples_train) + '_' + str(omega) + '_' + str(seed) + '.csv'
Path(img_prefix).mkdir(parents=True, exist_ok=True)

img_suffix = '_' + str(num_runs) + '_' + str(num_samples_train) + '_' + str(omega) + '_' + str(seed) + '_all.png'
fig, ax = pyplot.subplots(len(est_list), len(order_list), figsize=(4*len(order_list) + 2, 3.2*len(est_list)),
                          sharey=True, sharex=True)
if len(est_list) < 2:
    ax = numpy.expand_dims(ax, axis=0)
if len(order_list) < 2:
    ax = numpy.expand_dims(ax, axis=1)

for i, est in enumerate(est_list):
    for j, order in enumerate(order_list):
        axi = ax[i, j]
        if order == 'misspec':
            data_prefix = '../data/uai/misspec/'
        else:
            data_prefix = '../data/uai/order{}/'.format(order)

        params = pandas.read_csv(data_prefix + 'params' + data_suffix)
        caus_err = pandas.read_csv(data_prefix + 'error_causal_lambda_stat' + data_suffix)
        stat_err = pandas.read_csv(data_prefix + 'error_stat_lambda_stat' + data_suffix)
        df = pandas.DataFrame()
        df['error'] = numpy.abs(stat_err[est] - caus_err[est])
        num_buckets = 20
        df['bucket'] = pandas.cut(df['error'], num_buckets)
        groups = df.groupby('bucket')

        #autocorr = get_autocorrelation(params, order, data_prefix, data_suffix)

        # Plot showing the scatter plot of statistical and causal error. The colour indicates the condition num kappa
        # ------------------
        # Prepare axis labels
        #axi.set_ylabel(est + r': Causal Error $\mathcal{G}$', size=label_size)
        axi.set_ylabel('Number of ' + est + ' Predictors', size=label_size)
        axi.set_xlabel(r'$|\mathcal{G} - \mathcal{S}|$', size=label_size)
        axi.set_yscale('log')
        axi.set_xscale('linear')
        print(groups.groups.keys())
        #axi.set_xticklabels([k.right for k in list(groups.groups.keys())])
        # Actual plot
        #m = numpy.max([numpy.max(stat_err_lambda_stat[est]), numpy.max(caus_err_lambda_stat[est])])
        #axi.plot([0, m], [0, m], c='black')

        #print(groups.groups.keys())
        axi.bar([k.right for k in list(groups.groups.keys())], groups.count()['error'],
                [k.right-k.left for k in list(groups.groups.keys())])
        #cmap = axi.scatter(stat_err_lambda_stat[est], caus_err_lambda_stat[est],1,
        #                   #c=autocorr,
        #                   alpha=.5)

#colorbar(cmap, label=r'Condition Number $\kappa$')
fig.tight_layout()

# Save and show
pyplot.savefig(img_prefix + 'error_hist' + img_suffix, bbox_inches='tight')
pyplot.show()
pyplot.close()
