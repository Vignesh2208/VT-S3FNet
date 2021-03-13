import plotly.graph_objects as go
import sys
import os
from os.path import expanduser
import numpy as np
import json
import math

home = expanduser("~")
periods = [200000, 400000, 600000, 800000, 1000000]
tx_sizes = [8, 256, 2000]
mus = [200000, 400000, 600000, 800000, 1000000]
nemus = [20, 40, 60, 80, 100]
rates = [1, 10, 100, 1000]
n = nemus[0]


periodic_params_speedup = {}
poisson_params_speedup = {}
periodic_nemus_speedup = {}
poisson_nemus_speedup = {}
rand_nemus_speedup = {}
rate_nemus_speedup = {}
mixed_nemus_speedup = {}


fig_width=900
fig_height=600
title_font_size = 30
axis_label_font_size = 25
tick_font_size = 25
legend_font_size = 25
tickwidth = 5
ticklength = 10
colorbar_tickfont = 25
colorbar_titlefont = 25
marker_size=20

def get_stats(log_dir):

    with open(f"{log_dir}/stats.json", "r") as f:
        d = json.load(f)
    
    overheads = []
    burst_lengths = []
    for ovr_entry in d["overheads"]:
        overheads.append(float(ovr_entry["elapsedSec"]))
    
    for blength_entry in d["burst_lengths"]:

        if float(blength_entry["mu_progress_duration"]) > 0:
            burst_lengths.append(float(blength_entry["mu_progress_duration"]))
    return overheads, np.mean(burst_lengths), 1.96 * np.std(burst_lengths) / math.sqrt(len(burst_lengths))



for mu in mus:
    for tx_size in tx_sizes:
        if tx_size not in poisson_params_speedup:
            poisson_params_speedup[tx_size] = {}
            poisson_params_speedup[tx_size]['mu_ovr_en'] = []
            poisson_params_speedup[tx_size]['std_ovr_en'] = []
            poisson_params_speedup[tx_size]['mu_blen_en'] = []
            poisson_params_speedup[tx_size]['std_blen_en'] = []

            poisson_params_speedup[tx_size]['rel_ovr_mu'] = []
            poisson_params_speedup[tx_size]['rel_ovr_std'] = []

            poisson_params_speedup[tx_size]['mu_ovr_dis'] = []
            poisson_params_speedup[tx_size]['std_ovr_dis'] = []
            poisson_params_speedup[tx_size]['mu_blen_dis'] = []
            poisson_params_speedup[tx_size]['std_blen_dis'] = []

        exp_la_en_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Enabled/poisson/TCP_LA_Enabled_nemus_{n}_poisson_mu_{mu}_txsize_{tx_size}"
        exp_la_dis_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Disabled/poisson/TCP_LA_Disabled_nemus_{n}_poisson_mu_{mu}_txsize_{tx_size}"

        ovrs_en, mu_blen_en, std_blen_en = get_stats(exp_la_en_log_dir)
        poisson_params_speedup[tx_size]['mu_ovr_en'].append(np.mean(ovrs_en))
        poisson_params_speedup[tx_size]['std_ovr_en'].append(np.std(ovrs_en))
        poisson_params_speedup[tx_size]['mu_blen_en'].append(mu_blen_en)
        poisson_params_speedup[tx_size]['std_blen_en'].append(std_blen_en)


        ovrs_dis, mu_blen, std_blen = get_stats(exp_la_dis_log_dir)
        poisson_params_speedup[tx_size]['mu_ovr_dis'].append(np.mean(ovrs_dis))
        poisson_params_speedup[tx_size]['std_ovr_dis'].append(np.std(ovrs_dis))
        poisson_params_speedup[tx_size]['mu_blen_dis'].append(mu_blen)
        poisson_params_speedup[tx_size]['std_blen_dis'].append(std_blen)

        mu_ovrs_dis = np.mean(ovrs_dis)
        rel_ovrs = []
        for x in ovrs_en:
            rel_ovrs.append(mu_ovrs_dis/float(x))
        poisson_params_speedup[tx_size]['rel_ovr_mu'].append(np.mean(rel_ovrs))
        poisson_params_speedup[tx_size]['rel_ovr_std'].append(1.96 * np.std(rel_ovrs)/math.sqrt(len(rel_ovrs)))
        


for period in periods:
    for tx_size in tx_sizes:
        if tx_size not in periodic_params_speedup:
            periodic_params_speedup[tx_size] = {}
            periodic_params_speedup[tx_size]['mu_ovr_en'] = []
            periodic_params_speedup[tx_size]['std_ovr_en'] = []
            periodic_params_speedup[tx_size]['mu_blen_en'] = []
            periodic_params_speedup[tx_size]['std_blen_en'] = []

            periodic_params_speedup[tx_size]['rel_ovr_mu'] = []
            periodic_params_speedup[tx_size]['rel_ovr_std'] = []


            periodic_params_speedup[tx_size]['mu_ovr_dis'] = []
            periodic_params_speedup[tx_size]['std_ovr_dis'] = []
            periodic_params_speedup[tx_size]['mu_blen_dis'] = []
            periodic_params_speedup[tx_size]['std_blen_dis'] = []

        exp_la_en_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Enabled/periodic/TCP_LA_Enabled_nemus_{n}_periodic_period_{period}_txsize_{tx_size}"
        exp_la_dis_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Disabled/periodic/TCP_LA_Disabled_nemus_{n}_periodic_period_{period}_txsize_{tx_size}"

        ovrs_en, mu_blen_en, std_blen_en = get_stats(exp_la_en_log_dir)
        periodic_params_speedup[tx_size]['mu_ovr_en'].append(np.mean(ovrs_en))
        periodic_params_speedup[tx_size]['std_ovr_en'].append(np.std(ovrs_en))
        periodic_params_speedup[tx_size]['mu_blen_en'].append(mu_blen_en)
        periodic_params_speedup[tx_size]['std_blen_en'].append(std_blen_en)


        ovrs_dis, mu_blen, std_blen = get_stats(exp_la_dis_log_dir)
        periodic_params_speedup[tx_size]['mu_ovr_dis'].append(np.mean(ovrs_dis))
        periodic_params_speedup[tx_size]['std_ovr_dis'].append(np.std(ovrs_dis))
        periodic_params_speedup[tx_size]['mu_blen_dis'].append(mu_blen)
        periodic_params_speedup[tx_size]['std_blen_dis'].append(std_blen)

        mu_ovrs_dis = np.mean(ovrs_dis)
        rel_ovrs = []
        for x in ovrs_en:
            rel_ovrs.append(mu_ovrs_dis/float(x))
        periodic_params_speedup[tx_size]['rel_ovr_mu'].append(np.mean(rel_ovrs))
        periodic_params_speedup[tx_size]['rel_ovr_std'].append(1.96 * np.std(rel_ovrs)/math.sqrt(len(rel_ovrs)))


for nemu in nemus:
    period = periods[0]
    for tx_size in tx_sizes:
        if tx_size not in periodic_nemus_speedup:
            periodic_nemus_speedup[tx_size] = {}
            periodic_nemus_speedup[tx_size]['mu_ovr_en'] = []
            periodic_nemus_speedup[tx_size]['std_ovr_en'] = []
            periodic_nemus_speedup[tx_size]['mu_blen_en'] = []
            periodic_nemus_speedup[tx_size]['std_blen_en'] = []

            periodic_nemus_speedup[tx_size]['rel_ovr_mu'] = []
            periodic_nemus_speedup[tx_size]['rel_ovr_std'] = []

            periodic_nemus_speedup[tx_size]['mu_ovr_dis'] = []
            periodic_nemus_speedup[tx_size]['std_ovr_dis'] = []
            periodic_nemus_speedup[tx_size]['mu_blen_dis'] = []
            periodic_nemus_speedup[tx_size]['std_blen_dis'] = []


            poisson_nemus_speedup[tx_size] = {}
            poisson_nemus_speedup[tx_size]['mu_ovr_en'] = []
            poisson_nemus_speedup[tx_size]['std_ovr_en'] = []
            poisson_nemus_speedup[tx_size]['mu_blen_en'] = []
            poisson_nemus_speedup[tx_size]['std_blen_en'] = []

            poisson_nemus_speedup[tx_size]['rel_ovr_mu'] = []
            poisson_nemus_speedup[tx_size]['rel_ovr_std'] = []

            poisson_nemus_speedup[tx_size]['mu_ovr_dis'] = []
            poisson_nemus_speedup[tx_size]['std_ovr_dis'] = []
            poisson_nemus_speedup[tx_size]['mu_blen_dis'] = []
            poisson_nemus_speedup[tx_size]['std_blen_dis'] = []

        exp_la_en_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Enabled/periodic/TCP_LA_Enabled_nemus_{nemu}_periodic_period_{period}_txsize_{tx_size}"
        exp_la_dis_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Disabled/periodic/TCP_LA_Disabled_nemus_{nemu}_periodic_period_{period}_txsize_{tx_size}"

        ovrs_en, mu_blen_en, std_blen_en = get_stats(exp_la_en_log_dir)
        periodic_nemus_speedup[tx_size]['mu_ovr_en'].append(np.mean(ovrs_en))
        periodic_nemus_speedup[tx_size]['std_ovr_en'].append(np.std(ovrs_en))
        periodic_nemus_speedup[tx_size]['mu_blen_en'].append(mu_blen_en)
        periodic_nemus_speedup[tx_size]['std_blen_en'].append(std_blen_en)

        ovrs_dis, mu_blen, std_blen = get_stats(exp_la_dis_log_dir)
        periodic_nemus_speedup[tx_size]['mu_ovr_dis'].append(np.mean(ovrs_dis))
        periodic_nemus_speedup[tx_size]['std_ovr_dis'].append(np.std(ovrs_dis))
        periodic_nemus_speedup[tx_size]['mu_blen_dis'].append(mu_blen)
        periodic_nemus_speedup[tx_size]['std_blen_dis'].append(std_blen)

        print ("Tx-size: ", tx_size, " ovrs_en = ", ovrs_en, " ovrs_dis = ", ovrs_dis)
        mu_ovrs_dis = np.mean(ovrs_dis)
        rel_ovrs = []
        for x in ovrs_en:
            rel_ovrs.append(mu_ovrs_dis/float(x))
        periodic_nemus_speedup[tx_size]['rel_ovr_mu'].append(np.mean(rel_ovrs))
        periodic_nemus_speedup[tx_size]['rel_ovr_std'].append(1.96 * np.std(rel_ovrs)/math.sqrt(len(rel_ovrs)))


        exp_la_en_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Enabled/poisson/TCP_LA_Enabled_nemus_{nemu}_poisson_mu_{period}_txsize_{tx_size}"
        exp_la_dis_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Disabled/poisson/TCP_LA_Disabled_nemus_{nemu}_poisson_mu_{period}_txsize_{tx_size}"

        ovrs_en, mu_blen_en, std_blen_en = get_stats(exp_la_en_log_dir)
        poisson_nemus_speedup[tx_size]['mu_ovr_en'].append(np.mean(ovrs_en))
        poisson_nemus_speedup[tx_size]['std_ovr_en'].append(np.std(ovrs_en))
        poisson_nemus_speedup[tx_size]['mu_blen_en'].append(mu_blen_en)
        poisson_nemus_speedup[tx_size]['std_blen_en'].append(std_blen_en)

        ovrs_dis, mu_blen, std_blen = get_stats(exp_la_dis_log_dir)
        poisson_nemus_speedup[tx_size]['mu_ovr_dis'].append(np.mean(ovrs_dis))
        poisson_nemus_speedup[tx_size]['std_ovr_dis'].append(np.std(ovrs_dis))
        poisson_nemus_speedup[tx_size]['mu_blen_dis'].append(mu_blen)
        poisson_nemus_speedup[tx_size]['std_blen_dis'].append(std_blen)

        mu_ovrs_dis = np.mean(ovrs_dis)
        rel_ovrs = []
        for x in ovrs_en:
            rel_ovrs.append(mu_ovrs_dis/float(x))
        poisson_nemus_speedup[tx_size]['rel_ovr_mu'].append(np.mean(rel_ovrs))
        poisson_nemus_speedup[tx_size]['rel_ovr_std'].append(1.96 * np.std(rel_ovrs)/math.sqrt(len(rel_ovrs)))



for nemu in nemus:
    period = 1000000
    for tx_size in tx_sizes:
        if tx_size not in rand_nemus_speedup:
            rand_nemus_speedup[tx_size] = {}
            rand_nemus_speedup[tx_size]['mu_ovr_en'] = []
            rand_nemus_speedup[tx_size]['std_ovr_en'] = []
            rand_nemus_speedup[tx_size]['mu_blen_en'] = []
            rand_nemus_speedup[tx_size]['std_blen_en'] = []

            rand_nemus_speedup[tx_size]['rel_ovr_mu'] = []
            rand_nemus_speedup[tx_size]['rel_ovr_std'] = []

            rand_nemus_speedup[tx_size]['mu_ovr_dis'] = []
            rand_nemus_speedup[tx_size]['std_ovr_dis'] = []
            rand_nemus_speedup[tx_size]['mu_blen_dis'] = []
            rand_nemus_speedup[tx_size]['std_blen_dis'] = []

        exp_la_en_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Enabled/rand/TCP_RAND_LA_Enabled_nemus_{nemu}_poisson_mu_{period}_txsize_{tx_size}"
        exp_la_dis_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Disabled/rand/TCP_RAND_LA_Disabled_nemus_{nemu}_poisson_mu_{period}_txsize_{tx_size}"

        ovrs_en, mu_blen_en, std_blen_en = get_stats(exp_la_en_log_dir)
        rand_nemus_speedup[tx_size]['mu_ovr_en'].append(np.mean(ovrs_en))
        rand_nemus_speedup[tx_size]['std_ovr_en'].append(np.std(ovrs_en))
        rand_nemus_speedup[tx_size]['mu_blen_en'].append(mu_blen_en)
        rand_nemus_speedup[tx_size]['std_blen_en'].append(std_blen_en)

        ovrs_dis, mu_blen, std_blen = get_stats(exp_la_dis_log_dir)
        rand_nemus_speedup[tx_size]['mu_ovr_dis'].append(np.mean(ovrs_dis))
        rand_nemus_speedup[tx_size]['std_ovr_dis'].append(np.std(ovrs_dis))
        rand_nemus_speedup[tx_size]['mu_blen_dis'].append(mu_blen)
        rand_nemus_speedup[tx_size]['std_blen_dis'].append(std_blen)

        mu_ovrs_dis = np.mean(ovrs_dis)
        rel_ovrs = []
        for x in ovrs_en:
            rel_ovrs.append(mu_ovrs_dis/float(x))
        rand_nemus_speedup[tx_size]['rel_ovr_mu'].append(np.mean(rel_ovrs))
        rand_nemus_speedup[tx_size]['rel_ovr_std'].append(1.96 * np.std(rel_ovrs)/math.sqrt(len(rel_ovrs)))


for nemu in nemus:
    for rate in rates:
        if rate not in rate_nemus_speedup:
            rate_nemus_speedup[rate] = {}
            rate_nemus_speedup[rate]['mu_ovr_en'] = []
            rate_nemus_speedup[rate]['std_ovr_en'] = []
            rate_nemus_speedup[rate]['mu_blen_en'] = []
            rate_nemus_speedup[rate]['std_blen_en'] = []
            rate_nemus_speedup[rate]['mu_ovr_dis'] = []
            rate_nemus_speedup[rate]['std_ovr_dis'] = []
            rate_nemus_speedup[rate]['mu_blen_dis'] = []
            rate_nemus_speedup[rate]['std_blen_dis'] = []
            rate_nemus_speedup[rate]['rel_ovr_mu'] = []
            rate_nemus_speedup[rate]['rel_ovr_std'] = []
            

        exp_la_en_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Enabled/rate/TCP_LA_Enabled_nemus_{nemu}_ratelim_rate_{rate}"
        exp_la_dis_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Disabled/rate/TCP_LA_Disabled_nemus_{nemu}_ratelim_rate_{rate}"

        ovrs_en, mu_blen_en, std_blen_en = get_stats(exp_la_en_log_dir)
        rate_nemus_speedup[rate]['mu_ovr_en'].append(np.mean(ovrs_en))
        rate_nemus_speedup[rate]['std_ovr_en'].append(np.std(ovrs_en))
        rate_nemus_speedup[rate]['mu_blen_en'].append(mu_blen_en)
        rate_nemus_speedup[rate]['std_blen_en'].append(std_blen_en)

        ovrs_dis, mu_blen, std_blen = get_stats(exp_la_dis_log_dir)
        rate_nemus_speedup[rate]['mu_ovr_dis'].append(np.mean(ovrs_dis))
        rate_nemus_speedup[rate]['std_ovr_dis'].append(np.std(ovrs_dis))
        rate_nemus_speedup[rate]['mu_blen_dis'].append(mu_blen)
        rate_nemus_speedup[rate]['std_blen_dis'].append(std_blen)

        mu_ovrs_dis = np.mean(ovrs_dis)
        rel_ovrs = []
        for x in ovrs_en:
            rel_ovrs.append(mu_ovrs_dis/float(x))
        rate_nemus_speedup[rate]['rel_ovr_mu'].append(np.mean(rel_ovrs))
        rate_nemus_speedup[rate]['rel_ovr_std'].append(1.96 * np.std(rel_ovrs)/math.sqrt(len(rel_ovrs)))


mixed_nemus_speedup['mu_ovr_en'] = []
mixed_nemus_speedup['std_ovr_en'] = []
mixed_nemus_speedup['mu_blen_en'] = []
mixed_nemus_speedup['std_blen_en'] = []
mixed_nemus_speedup['mu_ovr_dis'] = []
mixed_nemus_speedup['std_ovr_dis'] = []
mixed_nemus_speedup['mu_blen_dis'] = []
mixed_nemus_speedup['std_blen_dis'] = []
mixed_nemus_speedup['rel_ovr_mu'] = []
mixed_nemus_speedup['rel_ovr_std'] = []

for nemu in nemus:
    

    exp_la_en_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Enabled/mixed/TCP_LA_Enabled_nemus_{nemu}_mixed"
    exp_la_dis_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Disabled/mixed/TCP_LA_Disabled_nemus_{nemu}_mixed"

    ovrs_en, mu_blen_en, std_blen_en = get_stats(exp_la_en_log_dir)
    mixed_nemus_speedup['mu_ovr_en'].append(np.mean(ovrs_en))
    mixed_nemus_speedup['std_ovr_en'].append(np.std(ovrs_en))
    mixed_nemus_speedup['mu_blen_en'].append(mu_blen_en)
    mixed_nemus_speedup['std_blen_en'].append(std_blen_en)

    ovrs_dis, mu_blen, std_blen = get_stats(exp_la_dis_log_dir)
    mixed_nemus_speedup['mu_ovr_dis'].append(np.mean(ovrs_dis))
    mixed_nemus_speedup['std_ovr_dis'].append(np.std(ovrs_dis))
    mixed_nemus_speedup['mu_blen_dis'].append(mu_blen)
    mixed_nemus_speedup['std_blen_dis'].append(std_blen)

    mu_ovrs_dis = np.mean(ovrs_dis)
    rel_ovrs = []
    for x in ovrs_en:
        rel_ovrs.append(mu_ovrs_dis/float(x))
    mixed_nemus_speedup['rel_ovr_mu'].append(np.mean(rel_ovrs))
    mixed_nemus_speedup['rel_ovr_std'].append(1.96 * np.std(rel_ovrs)/math.sqrt(len(rel_ovrs)))




cmin = 0
cmax = 0

for tx_size in tx_sizes:
    if cmin == 0 or min(periodic_params_speedup[tx_size]['mu_ovr_en']) < cmin:
        cmin = min(periodic_params_speedup[tx_size]['mu_ovr_en'])
    if cmax == 0 or max(periodic_params_speedup[tx_size]['mu_ovr_en']) > cmax:
        cmax = max(periodic_params_speedup[tx_size]['mu_ovr_en'])

step = (cmax - cmin)/len(periods)
colors_range = np.linspace(int(cmin), int(cmax), int(step))

def update_save_fig(fig, colorbar_title, plot_title, xlabel, ylabel, title_x,
    fname, disable_legend=False, width=900, height=600, legend_x=0, legend_y=1, enabled_border=True,
    legend_orientation="h", disable_color_axis=False):

    if enabled_border:
        legend=go.layout.Legend(
            x=legend_x,
            y=legend_y,
            font=dict(
                family="sans-serif",
                size=legend_font_size,
                color="black"
            ),
            bgcolor="White",
            bordercolor="Black",
            borderwidth=2
        )
    else:
        legend=go.layout.Legend(
            x=legend_x,
            y=legend_y,
            font=dict(
                family="sans-serif",
                size=legend_font_size,
                color="black"
            )
        )

    if disable_legend:
        legend = None

    
    if not disable_color_axis:
        fig.update_layout(
            coloraxis = {
            'colorscale':'bluered', 
            'colorbar': dict(
                title=colorbar_title, 
                titlefont=dict(family="Courier", size=colorbar_titlefont),
                tickfont=dict(family="Courier", size=colorbar_tickfont),
                titleside="right"
                ),
                

            })

    fig.update_layout(
        #title=go.layout.Title(
        #    text=plot_title,
        #font=dict(
        #            family="Courier",
        #            size=title_font_size
        #        ),
        #xanchor = "auto",
        #yanchor = "middle",
        #x=title_x),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text=xlabel,
                font=dict(
                    family="Courier",
                    size=axis_label_font_size
                )
            ),
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text=ylabel,
                font=dict(
                    family="Courier",
                    size=axis_label_font_size
                )
            )
        ),
        legend=legend
        
    )

    fig.update_xaxes(title_font=dict(size=axis_label_font_size, family='Courier'), tickfont=dict(family='Courier', size=tick_font_size))
    fig.update_yaxes(title_font=dict(size=axis_label_font_size, family='Courier'), tickfont=dict(family='Courier', size=tick_font_size), nticks=8)
    fig.update_xaxes(ticks="outside", tickwidth=tickwidth, ticklen=ticklength)
    fig.update_yaxes(ticks="outside", tickwidth=tickwidth, ticklen=ticklength)

    if legend_orientation == "h":
        fig.update_layout(legend_orientation="h")


    #fig.show()
    if not os.path.isdir(f"{home}/VT-S3FNet/experiment-data/figs"):
        os.mkdir(f"{home}/VT-S3FNet/experiment-data/figs")
    fig.write_image(f"{home}/VT-S3FNet/experiment-data/figs/{fname}",
        width=width, height=height)


tx_size_lines = {
    8:  dict(color="blue", width=4.0, dash="dash"),
    256: dict(color="red", width=4.0, dash="longdash"),
    2000: dict(color="green", width=4.0, dash="solid")
}

tx_size_markers = {
    8: 'circle',
    256: 'square',
    2000: 'triangle-up-dot'
}

rate_lines = {
    1:  dict(color="blue", width=4.0, dash="dash"),
    10: dict(color="red", width=4.0, dash="longdash"),
    100: dict(color="green", width=4.0, dash="solid"),
    1000: dict(color="black", width=4.0, dash="dashdot"),
}

rate_markers = {
    1: 'circle',
    10: 'square',
    100: 'triangle-up-dot',
    1000: 'triangle-down-dot'
}

fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=[200, 400, 600, 800, 1000],
        y=periodic_params_speedup[tx_size]['rel_ovr_mu'],
        error_y=dict(type='data',
            array=periodic_params_speedup[tx_size]['rel_ovr_std'],
            thickness=1.5, width=3),
        name=f"Transfer size: {tx_size} Kb" if tx_size != 2000 else f"Transfer size: 2 Mb",
        marker=dict(
            size=marker_size, coloraxis="coloraxis", color=periodic_params_speedup[tx_size]['mu_ovr_en'],
            symbol=tx_size_markers[tx_size]),
        line=tx_size_lines[tx_size].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Relative Speedup with Lookahead - Periodic Traffic",
    xlabel="Traffic Period [ms]", 
    ylabel="Relative Speedup [units]",
    title_x=0.1,
    fname="periodic_params_speedup.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False)

fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=[200, 400, 600, 800, 1000],
        y=periodic_params_speedup[tx_size]['mu_blen_en'],
        error_y=dict(type='data',
            array=periodic_params_speedup[tx_size]['std_blen_en'],
            thickness=1.5, width=3),
        name=f"Transfer size: {tx_size} Kb" if tx_size != 2000 else f"Transfer size: 2 Mb",
        marker=dict(
            size=marker_size,
            symbol=tx_size_markers[tx_size]),
        line=tx_size_lines[tx_size].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title=None,
    plot_title="Timeline Avg Execution Burst Length",
    xlabel="Traffic Period [ms]", 
    ylabel="Execution Burst Length [usec]",
    title_x=0.1,
    fname="periodic_params_exec_burst_lengths.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False,
    disable_color_axis=True)


#
#   Periodic Traffic
#

nemu_flows = [10, 20, 30, 40, 50]

fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=nemu_flows,
        y=periodic_nemus_speedup[tx_size]['rel_ovr_mu'],
        error_y=dict(type='data',
            array=periodic_nemus_speedup[tx_size]['rel_ovr_std'],
            thickness=1.5, width=3),
        name=f"Transfer size: {tx_size} Kb" if tx_size != 2000 else f"Transfer size: 2 Mb",
        marker=dict(
            size=marker_size, coloraxis="coloraxis", color=periodic_nemus_speedup[tx_size]['mu_ovr_en'],
            symbol=tx_size_markers[tx_size]),
        line=tx_size_lines[tx_size].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Relative Speedup with Lookahead - Periodic Traffic",
    xlabel="Number of emulated flows [units]", 
    ylabel="Relative Speedup [units]",
    title_x=0.1,
    fname="periodic_nemus_speedup.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False)


fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=nemu_flows,
        y=periodic_nemus_speedup[tx_size]['mu_blen_en'],
        error_y=dict(type='data',
            array=periodic_nemus_speedup[tx_size]['std_blen_en'],
            thickness=1.5, width=3),
        name=f"Transfer size: {tx_size} Kb" if tx_size != 2000 else f"Transfer size: 2 Mb",
        marker=dict(
            size=marker_size,
            symbol=tx_size_markers[tx_size]),
        line=tx_size_lines[tx_size].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Timeline Avg Execution Burst Lengths",
    xlabel="Number of emulated flows [units]", 
    ylabel="Execution Burst Lengths [usec]",
    title_x=0.1,
    fname="periodic_nemus_exec_burst_lengths.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False,
    disable_color_axis=True)

#
#   Poisson Traffic
#

fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=[200, 400, 600, 800, 1000],
        y=poisson_params_speedup[tx_size]['rel_ovr_mu'],
        error_y=dict(type='data',
            array=poisson_params_speedup[tx_size]['rel_ovr_std'],
            thickness=1.5, width=3),
        name=f"Transfer size: {tx_size} Kb" if tx_size != 2000 else f"Transfer size: 2 Mb",
        marker=dict(
            size=marker_size, coloraxis="coloraxis", color=poisson_params_speedup[tx_size]['mu_ovr_en'],
            symbol=tx_size_markers[tx_size]),
        line=tx_size_lines[tx_size].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Relative Speedup with Lookahead - Poisson Traffic",
    xlabel="Traffic Mean Interarrival Time [ms]", 
    ylabel="Relative Speedup [units]",
    title_x=0.1,
    fname="poisson_params_speedup.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False)

fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=[200, 400, 600, 800, 1000],
        y=poisson_params_speedup[tx_size]['mu_blen_en'],
        error_y=dict(type='data',
            array=poisson_params_speedup[tx_size]['std_blen_en'],
            thickness=1.5, width=3),
        name=f"Transfer size: {tx_size} Kb" if tx_size != 2000 else f"Transfer size: 2 Mb",
        marker=dict(
            size=marker_size,
            symbol=tx_size_markers[tx_size]),
        line=tx_size_lines[tx_size].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title=None,
    plot_title="Timeline Avg Execution Burst Length",
    xlabel="Traffic Period [ms]", 
    ylabel="Execution Burst Length [usec]",
    title_x=0.1,
    fname="poisson_params_exec_burst_lengths.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False,
    disable_color_axis=True)

fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=nemu_flows,
        y=poisson_nemus_speedup[tx_size]['rel_ovr_mu'],
        error_y=dict(type='data',
            array=poisson_nemus_speedup[tx_size]['rel_ovr_std'],
            thickness=1.5, width=3),
        name=f"Transfer size: {tx_size} Kb" if tx_size != 2000 else f"Transfer size: 2 Mb",
        marker=dict(
            size=marker_size, coloraxis="coloraxis", color=poisson_nemus_speedup[tx_size]['mu_ovr_en'],
            symbol=tx_size_markers[tx_size]),
        line=tx_size_lines[tx_size].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Relative Speedup with Lookahead - Poisson Traffic",
    xlabel="Number of poisson bursty emulated TCP flows [units]", 
    ylabel="Relative Speedup [units]",
    title_x=0.1,
    fname="poisson_nemus_speedup.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False)


fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=nemu_flows,
        y=poisson_nemus_speedup[tx_size]['mu_blen_en'],
        error_y=dict(type='data',
            array=poisson_nemus_speedup[tx_size]['std_blen_en'],
            thickness=1.5, width=3),
        name=f"Transfer size: {tx_size} Kb" if tx_size != 2000 else f"Transfer size: 2 Mb",
        marker=dict(
            size=marker_size,
            symbol=tx_size_markers[tx_size]),
        line=tx_size_lines[tx_size].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Timeline Avg Execution Burst Lengths",
    xlabel="Number of emulated flows [units]", 
    ylabel="Execution Burst Lengths [usec]",
    title_x=0.1,
    fname="poisson_nemus_exec_burst_lengths.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False,
    disable_color_axis=True)

#
#   TCP RAND experiments
#

fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=nemu_flows,
        y=rand_nemus_speedup[tx_size]['rel_ovr_mu'],
        error_y=dict(type='data',
            array=rand_nemus_speedup[tx_size]['rel_ovr_std'],
            thickness=1.5, width=3),
        name=f"Transfer size: {tx_size} Kb" if tx_size != 2000 else f"Transfer size: 2 Mb",
        marker=dict(
            size=marker_size, coloraxis="coloraxis", color=rand_nemus_speedup[tx_size]['mu_ovr_en'],
            symbol=tx_size_markers[tx_size]),
        line=tx_size_lines[tx_size].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Relative Speedup with Lookahead - TCP RAND",
    xlabel="Number of poisson bursty emulated TCP flows [units]", 
    ylabel="Relative Speedup [units]",
    title_x=0.1,
    fname="rand_nemus_speedup.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False)

#
#   Rate limited Traffic
#


fig = go.Figure()
for rate in rates:
    fig.add_trace(go.Scatter(
        x=nemu_flows,
        y=rate_nemus_speedup[rate]['rel_ovr_mu'],
        error_y=dict(type='data',
            array=rate_nemus_speedup[rate]['rel_ovr_std'],
            thickness=1.5, width=3),
        name= f"Rate: {rate} Mbps" if rate != 1000  else f"Rate: 1 Gbps",
        marker=dict(
            size=marker_size, coloraxis="coloraxis", color=rate_nemus_speedup[rate]['mu_ovr_en'],
            symbol=rate_markers[rate]),
        line=rate_lines[rate].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Relative Speedup with Lookahead: Rate-limited Traffic",
    xlabel="Number of rate limited emulated TCP flows [units]", 
    ylabel="Relative Speedup [units]",
    title_x=0.1,
    fname="rate_nemus_speedup.jpg",
    legend_x=-0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False)



fig = go.Figure()
for rate in rates:
    fig.add_trace(go.Scatter(
        x=nemu_flows,
        y=rate_nemus_speedup[rate]['mu_blen_en'],
        error_y=dict(type='data',
            array=rate_nemus_speedup[rate]['std_blen_en'],
            thickness=1.5, width=3),
        name= f"Rate: {rate} Mbps" if rate != 1000  else f"Rate: 1 Gbps",
        marker=dict(
            size=marker_size,
            symbol=rate_markers[rate]),
        line=rate_lines[rate].copy(),
        mode="markers+lines"))


update_save_fig(
    fig=fig,
    colorbar_title=None,
    plot_title="Timeline Avg Execution Burst Lengths",
    xlabel="Number of emulated flows [units]", 
    ylabel="Execution Burst Lengths [usec]",
    title_x=0.1,
    fname="rate_nemus_exec_burst_lengths.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False,
    disable_color_axis=True)


#
#   Mixed Traffic
#



fig = go.Figure()
fig.add_trace(go.Scatter(
    x=nemu_flows,
    y=mixed_nemus_speedup['rel_ovr_mu'],
    error_y=dict(type='data',
        array=mixed_nemus_speedup['rel_ovr_std'],
        thickness=1.5, width=3),
    marker=dict(
        size=marker_size, coloraxis="coloraxis", color=mixed_nemus_speedup['mu_ovr_en'],
        symbol='circle'),
    line=dict(color="red", width=4.0, dash="longdash"),
    mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Relative Speedup with Lookahead: Mixed Traffic",
    xlabel="Number of emulated TCP flows [units]", 
    ylabel="Relative Speedup [units]",
    title_x=0.0,
    fname="mixed_nemus_speedup.jpg",
    legend_x=-0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False,
    disable_legend=True)


"""
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=nemu_flows,
    y=mixed_nemus_speedup['mu_blen_en'],
    error_y=dict(type='data',
        array=mixed_nemus_speedup['std_blen_en'],
        thickness=1.5, width=3),
    marker=dict(
        size=marker_size,
        symbol='circle'),
    line=dict(color="red", width=4.0, dash="longdash"),
    mode="markers+lines"))


update_save_fig(
    fig=fig,
    colorbar_title=None,
    plot_title="Timeline Avg Execution Burst Lengths",
    xlabel="Number of emulated flows [units]", 
    ylabel="Execution Burst Lengths [usec]",
    title_x=0.1,
    fname="mixed_nemus_exec_burst_lengths.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=fig_width,
    height=fig_height,
    enabled_border=False,
    disable_color_axis=True,
    disable_legend=True)
"""




