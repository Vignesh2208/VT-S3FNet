import plotly.graph_objects as go
import sys
import os
from os.path import expanduser
import numpy as np
import json
import math

home = expanduser("~")
nemus = [20, 40, 60, 80, 100]
mpi_jobs = ['sat', 'int', 'mm']
mpi_job_labels = {
    'sat': 'MPI Circuit SAT',
    'int': 'MPI Integration',
    'mm' : 'MPI Matrix Vector Multiply'
}
mpi_nemus_speedup = {}
mpi_compute_comm_ratio = {}




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


def get_avg_compute_comm_ratio(nemu, job, la_enabled):

    if la_enabled:
        dirPath = f"{home}/VT-S3FNet/experiment-data/MPI_Experiments/LA_Enabled/{job}/MPI_LA_Enabled_nemus_{nemu + 1}_mpi_{job}"
    else:
        dirPath = f"{home}/VT-S3FNet/experiment-data/MPI_Experiments/LA_Disabled/{job}/MPI_LA_Disabled_nemus_{nemu + 1}_mpi_{job}"

    r = os.popen(f"""grep -nr "Avg-Compute-Communication-Ratio" {dirPath}/worker1.log | tail -1 | xargs | cut -d " " -f 3""").read()
    import re
    r = re.sub("[^0-9.]", "", r)
    import ast
    r = ast.literal_eval(r)
    return float(r)

for nemu in nemus:
    for job in mpi_jobs:
        if job not in mpi_nemus_speedup:
            mpi_nemus_speedup[job] = {}
            mpi_nemus_speedup[job]['mu_ovr_en'] = []
            mpi_nemus_speedup[job]['std_ovr_en'] = []
            mpi_nemus_speedup[job]['mu_blen_en'] = []
            mpi_nemus_speedup[job]['std_blen_en'] = []
            mpi_nemus_speedup[job]['mu_ovr_dis'] = []
            mpi_nemus_speedup[job]['std_ovr_dis'] = []
            mpi_nemus_speedup[job]['mu_blen_dis'] = []
            mpi_nemus_speedup[job]['std_blen_dis'] = []
            mpi_nemus_speedup[job]['rel_ovr_mu'] = []
            mpi_nemus_speedup[job]['rel_ovr_std'] = []
            

        exp_la_en_log_dir = f"{home}/VT-S3FNet/experiment-data/MPI_Experiments/LA_Enabled/{job}/MPI_LA_Enabled_nemus_{nemu + 1}_mpi_{job}"
        exp_la_dis_log_dir = f"{home}/VT-S3FNet/experiment-data/MPI_Experiments/LA_Disabled/{job}/MPI_LA_Disabled_nemus_{nemu + 1}_mpi_{job}"

        ovrs_en, mu_blen_en, std_blen_en = get_stats(exp_la_en_log_dir)
        mpi_nemus_speedup[job]['mu_ovr_en'].append(np.mean(ovrs_en))
        mpi_nemus_speedup[job]['std_ovr_en'].append(np.std(ovrs_en))
        mpi_nemus_speedup[job]['mu_blen_en'].append(mu_blen_en)
        mpi_nemus_speedup[job]['std_blen_en'].append(std_blen_en)

        ovrs_dis, mu_blen, std_blen = get_stats(exp_la_dis_log_dir)
        mpi_nemus_speedup[job]['mu_ovr_dis'].append(np.mean(ovrs_dis))
        mpi_nemus_speedup[job]['std_ovr_dis'].append(np.std(ovrs_dis))
        mpi_nemus_speedup[job]['mu_blen_dis'].append(mu_blen)
        mpi_nemus_speedup[job]['std_blen_dis'].append(std_blen)

        mu_ovrs_dis = np.mean(ovrs_dis)
        rel_ovrs = []
        for x in ovrs_en:
            rel_ovrs.append(mu_ovrs_dis/float(x))
        mpi_nemus_speedup[job]['rel_ovr_mu'].append(np.mean(rel_ovrs))
        mpi_nemus_speedup[job]['rel_ovr_std'].append(1.96 * np.std(rel_ovrs)/math.sqrt(len(rel_ovrs)))

for job in ['int', 'sat', 'mm']:
    mpi_compute_comm_ratio[job] = []
    for nemu in [20, 40, 60, 80, 100]:
        mpi_compute_comm_ratio[job].append(get_avg_compute_comm_ratio(nemu, job, True))
    

def update_save_fig(fig, colorbar_title, plot_title, xlabel, ylabel, title_x,
    fname, disable_legend=False, width=900, height=600, legend_x=0, legend_y=1, enabled_border=True,
    legend_orientation="h", disable_color_axis=False, logy=False):

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

    if logy:
        fig.update_layout(yaxis_type="log")
        fig.update_yaxes(title_font=dict(size=axis_label_font_size, family='Courier'), tickfont=dict(family='Courier', size=tick_font_size), dtick=1)
    else:
        fig.update_yaxes(title_font=dict(size=axis_label_font_size, family='Courier'), tickfont=dict(family='Courier', size=tick_font_size), nticks=8)
    fig.update_xaxes(title_font=dict(size=axis_label_font_size, family='Courier'), tickfont=dict(family='Courier', size=tick_font_size))
    
    fig.update_xaxes(ticks="outside", tickwidth=tickwidth, ticklen=ticklength)
    fig.update_yaxes(ticks="outside", tickwidth=tickwidth, ticklen=ticklength)

    if legend_orientation == "h":
        fig.update_layout(legend_orientation="h")


    #fig.show()
    if not os.path.isdir(f"{home}/VT-S3FNet/experiment-data/figs"):
        os.mkdir(f"{home}/VT-S3FNet/experiment-data/figs")
    fig.write_image(f"{home}/VT-S3FNet/experiment-data/figs/{fname}",
        width=width, height=height)


mpi_job_lines = {
    'sat' :  dict(color="blue", width=4.0, dash="dash"),
    'int' : dict(color="red", width=4.0, dash="longdash"),
    'mm'  : dict(color="green", width=4.0, dash="solid")
}

mpi_job_markers = {
    'sat' : 'circle',
    'int' : 'square',
    'mm'  : 'triangle-up-dot'
}


fig = go.Figure()
for job in mpi_jobs:
    fig.add_trace(go.Scatter(
        x=nemus,
        y=mpi_nemus_speedup[job]['rel_ovr_mu'],
        error_y=dict(type='data',
            array=mpi_nemus_speedup[job]['rel_ovr_std'],
            thickness=1.5, width=3),
        name=mpi_job_labels[job],
        marker=dict(
            size=marker_size, coloraxis="coloraxis", color=mpi_nemus_speedup[job]['mu_ovr_en'],
            symbol=mpi_job_markers[job]),
        line=mpi_job_lines[job].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title="Absolute Overhead Ratio",
    plot_title="Relative Speedup with Lookahead - MPI Jobs",
    xlabel="Number of workers [units]", 
    ylabel="Relative Speedup [units]",
    title_x=0.1,
    fname="mpi_nemus_speedup.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=1000,
    height=600,
    enabled_border=False)

fig = go.Figure()
for job in ['int', 'sat', 'mm']:
    fig.add_trace(go.Scatter(
        x=nemus,
        y=mpi_compute_comm_ratio[job],
        name=mpi_job_labels[job],
        marker=dict(
            size=marker_size, symbol=mpi_job_markers[job]),
        line=mpi_job_lines[job].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title=None,
    plot_title="Avg Compute-Communication Ratio - MPI Jobs",
    xlabel="Number of workers [units]", 
    ylabel="Avg Compute-Communication Ratio [units]",
    title_x=0.1,
    fname="mpi_compute_comm_ratio.jpg",
    legend_x=0.02,
    legend_y=1.2,
    width=900,
    height=600,
    disable_color_axis=True,
    enabled_border=False,
    logy=True)


fig = go.Figure()
for job in mpi_jobs:
    fig.add_trace(go.Scatter(
        x=nemus,
        y=mpi_nemus_speedup[job]['mu_blen_en'],
        error_y=dict(type='data',
            array=mpi_nemus_speedup[job]['std_blen_en'],
            thickness=1.5, width=3),
        name=mpi_job_labels[job],
        marker=dict(
            size=marker_size,
            symbol=mpi_job_markers[job]),
        line=mpi_job_lines[job].copy(),
        mode="markers+lines"))
    
update_save_fig(
    fig=fig,
    colorbar_title=None,
    plot_title="Timeline Avg Execution Burst Length",
    xlabel="Traffic Period [ms]", 
    ylabel="Execution Burst Length [usec]",
    title_x=0.1,
    fname="mpi_nemus_exec_burst_lengths.jpg",
    legend_x=0.02,
    legend_y=1.02,
    width=1100,
    height=900,
    enabled_border=False,
    disable_color_axis=True)
