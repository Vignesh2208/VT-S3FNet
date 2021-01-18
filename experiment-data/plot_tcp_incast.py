import plotly.graph_objects as go
import sys
import os
from os.path import expanduser
import numpy as np
import json
import math

home = expanduser("~")
tx_sizes = [8, 256, 2000]
mus = [200000, 1000000]
nincasts = [2, 4, 6, 8, 10]

incast_speedup = {}




title_font_size = 30
axis_label_font_size = 25
tick_font_size = 25
legend_font_size = 25
tickwidth = 5
ticklength = 10
colorbar_tickfont = 20
colorbar_titlefont = 20
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


for nemu in nincasts:
    for period in mus:
        if period not in incast_speedup:
            incast_speedup[period] = {}
        for tx_size in tx_sizes:
            if tx_size not in incast_speedup[period]:
                incast_speedup[period][tx_size] = {}
                incast_speedup[period][tx_size]['mu_ovr_en'] = []
                incast_speedup[period][tx_size]['std_ovr_en'] = []
                incast_speedup[period][tx_size]['mu_blen_en'] = []
                incast_speedup[period][tx_size]['std_blen_en'] = []

                incast_speedup[period][tx_size]['rel_ovr_mu'] = []
                incast_speedup[period][tx_size]['rel_ovr_std'] = []

                incast_speedup[period][tx_size]['mu_ovr_dis'] = []
                incast_speedup[period][tx_size]['std_ovr_dis'] = []
                incast_speedup[period][tx_size]['mu_blen_dis'] = []
                incast_speedup[period][tx_size]['std_blen_dis'] = []



            exp_la_en_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Enabled/incast/TCP_LA_Enabled_incast_tgen_nemus_{nemu + 1}_txSize_{tx_size}_mu_{period}"
            exp_la_dis_log_dir = f"{home}/VT-S3FNet/experiment-data/TCP_Experiments/LA_Disabled/incast/TCP_LA_Disabled_incast_tgen_nemus_{nemu + 1}_txSize_{tx_size}_mu_{period}"

            ovrs_en, mu_blen_en, std_blen_en = get_stats(exp_la_en_log_dir)
            incast_speedup[period][tx_size]['mu_ovr_en'].append(np.mean(ovrs_en))
            incast_speedup[period][tx_size]['std_ovr_en'].append(np.std(ovrs_en))
            incast_speedup[period][tx_size]['mu_blen_en'].append(mu_blen_en)
            incast_speedup[period][tx_size]['std_blen_en'].append(std_blen_en)

            ovrs_dis, mu_blen, std_blen = get_stats(exp_la_dis_log_dir)
            incast_speedup[period][tx_size]['mu_ovr_dis'].append(np.mean(ovrs_dis))
            incast_speedup[period][tx_size]['std_ovr_dis'].append(np.std(ovrs_dis))
            incast_speedup[period][tx_size]['mu_blen_dis'].append(mu_blen)
            incast_speedup[period][tx_size]['std_blen_dis'].append(std_blen)

            #print ("Tx-size: ", tx_size, " ovrs_en = ", ovrs_en, " ovrs_dis = ", ovrs_dis)
            mu_ovrs_dis = np.mean(ovrs_dis)
            rel_ovrs = []
            for x in ovrs_en:
                rel_ovrs.append(mu_ovrs_dis/float(x))
            incast_speedup[period][tx_size]['rel_ovr_mu'].append(np.mean(rel_ovrs))
            incast_speedup[period][tx_size]['rel_ovr_std'].append(1.96 * np.std(rel_ovrs)/math.sqrt(len(rel_ovrs)))


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
        title=go.layout.Title(
            text=plot_title,
        font=dict(
                    family="Courier",
                    size=title_font_size
                ),
        xanchor = "auto",
        yanchor = "middle",
        x=title_x),
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


period = mus[0]
fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=[2, 4, 6, 8, 10],
        y=incast_speedup[period][tx_size]['rel_ovr_mu'],
        error_y=dict(type='data',
            array=incast_speedup[period][tx_size]['rel_ovr_std'],
            thickness=1.5, width=3),
        name=f"Transfer size: {tx_size} Kb" if tx_size != 2000 else f"Transfer size: 2 Mb",
        marker=dict(
            size=marker_size, coloraxis="coloraxis", color=incast_speedup[period][tx_size]['mu_ovr_en'],
            symbol=tx_size_markers[tx_size]),
        line=tx_size_lines[tx_size].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Relative Speedup with Lookahead - Incast Traffic",
    xlabel="Number of incast flows [ms]", 
    ylabel="Relative Speedup [units]",
    title_x=0.1,
    fname="incast_speedup.jpg",
    legend_x=0.02,
    legend_y=1.02,
    width=1100,
    height=900,
    enabled_border=False)

fig = go.Figure()
for tx_size in tx_sizes:
    fig.add_trace(go.Scatter(
        x=[2, 4, 6, 8, 10],
        y=incast_speedup[period][tx_size]['mu_blen_en'],
        error_y=dict(type='data',
            array=incast_speedup[period][tx_size]['std_blen_en'],
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
    xlabel="Number of incast flows", 
    ylabel="Avg Execution Burst Length [usec]",
    title_x=0.1,
    fname="incast_exec_burst_lengths.jpg",
    legend_x=0.02,
    legend_y=1.02,
    width=1100,
    height=900,
    enabled_border=False,
    disable_color_axis=True)
