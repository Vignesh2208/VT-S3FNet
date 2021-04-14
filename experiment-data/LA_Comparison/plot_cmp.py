import json
import os
import sys
import plotly.graph_objects as go
import numpy as np


home = os.path.expanduser('~')

aggregation_wind_size = 2

ts_start = 0.0
ts_end = 5.0
ts_step = float(aggregation_wind_size)*10.0 / 1000.0
num_sampes = int((ts_end - ts_start)/ts_step)

ts = np.linspace(ts_start, ts_end, num_sampes)

title_font_size = 30
axis_label_font_size = 25
tick_font_size = 25
legend_font_size = 25
tickwidth = 5
ticklength = 10
colorbar_tickfont = 20
colorbar_titlefont = 20
marker_size=20

la_disabled_periodic = f"{home}/VT-S3FNet/experiment-data/LA_Comparison/LXC_TCP_LA_Disabled_Periodic/stats.json"
la_enabled_periodic = f"{home}/VT-S3FNet/experiment-data/LA_Comparison/LXC_TCP_LA_Enabled_Periodic/stats.json"

la_disabled_poisson = f"{home}/VT-S3FNet/experiment-data/LA_Comparison/LXC_TCP_LA_Disabled_Poisson/stats.json"
la_enabled_poisson = f"{home}/VT-S3FNet/experiment-data/LA_Comparison/LXC_TCP_LA_Enabled_Poisson/stats.json"

la_disabled_ratelim = f"{home}/VT-S3FNet/experiment-data/LA_Comparison/LXC_TCP_LA_Disabled_Rate/stats.json"
la_enabled_ratelim = f"{home}/VT-S3FNet/experiment-data/LA_Comparison/LXC_TCP_LA_Enabled_Rate/stats.json"



la_disabled_json = {}
la_enabled_json = {}

la_disabled_periodic_pkt_counts = []
la_enabled_periodic_pkt_counts = []

la_disabled_poisson_pkt_counts = []
la_enabled_poisson_pkt_counts = []

la_disabled_ratelim_pkt_counts = []
la_enabled_ratelim_pkt_counts = []


la_disabled_periodic_pkt_ts = []
la_enabled_periodic_pkt_ts = []

la_disabled_poisson_pkt_ts = []
la_enabled_poisson_pkt_ts = []

la_disabled_ratelim_pkt_ts = []
la_enabled_ratetim_pkt_ts = []

with open(la_disabled_periodic, 'r') as f:
    la_disabled_json = json.load(f)

with open(la_enabled_periodic, 'r') as f:
    la_enabled_json = json.load(f)

for entry in la_disabled_json["pkt_send_counts"]:
    la_disabled_periodic_pkt_counts.append(entry["value"])

for entry in la_enabled_json["pkt_send_counts"]:
    la_enabled_periodic_pkt_counts.append(entry["value"])


with open(la_disabled_poisson, 'r') as f:
    la_disabled_json = json.load(f)

with open(la_enabled_poisson, 'r') as f:
    la_enabled_json = json.load(f)

for entry in la_disabled_json["pkt_send_counts"]:
    la_disabled_poisson_pkt_counts.append(entry["value"])

for entry in la_enabled_json["pkt_send_counts"]:
    la_enabled_poisson_pkt_counts.append(entry["value"])

with open(la_disabled_ratelim, 'r') as f:
    la_disabled_json = json.load(f)

with open(la_enabled_ratelim, 'r') as f:
    la_enabled_json = json.load(f)

for entry in la_disabled_json["pkt_send_counts"]:
    la_disabled_ratelim_pkt_counts.append(entry["value"])

for entry in la_enabled_json["pkt_send_counts"]:
    la_enabled_ratelim_pkt_counts.append(entry["value"])

def aggregate(ls, agg_window):
    agg = []
    res = []
    for value in ls:
        if len(agg) < agg_window:
            agg.append(value)
        else:
            res.append(sum(agg))
            agg = []
            agg.append(value)
    if agg:
        res.append(sum(agg))
    return res

la_disabled_periodic_pkt_ts = aggregate(la_disabled_periodic_pkt_counts, aggregation_wind_size)
la_enabled_periodic_pkt_ts = aggregate(la_enabled_periodic_pkt_counts, aggregation_wind_size)

la_disabled_poisson_pkt_ts = aggregate(la_disabled_poisson_pkt_counts, aggregation_wind_size)
la_enabled_poisson_pkt_ts = aggregate(la_enabled_poisson_pkt_counts, aggregation_wind_size)

la_disabled_ratelim_pkt_ts = aggregate(la_disabled_ratelim_pkt_counts, aggregation_wind_size)
la_enabled_ratetim_pkt_ts = aggregate(la_enabled_ratelim_pkt_counts, aggregation_wind_size)
            

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


lines = {
    'LA_Disabled' :  dict(color="blue", width=4.0, dash="dash"),
    'LA_Enabled'  : dict(color="green", width=2.0, dash="solid")
}

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=ts,
    y=la_disabled_periodic_pkt_ts,
    name="Periodic - LA Disabled",
    line=lines['LA_Disabled'].copy(),
    mode="lines"))

fig.add_trace(go.Scatter(
    x=ts,
    y=la_enabled_periodic_pkt_ts,
    name="Periodic - LA Enabled",
    line=lines['LA_Enabled'].copy(),
    mode="lines"))

update_save_fig(
    fig=fig,
    colorbar_title=None,
    plot_title="Comparison of Periodic Traffic Flow",
    xlabel="Time [sec]", 
    ylabel="Number of sent packets",
    title_x=0.1,
    fname="periodic_flow_cmp.jpg",
    legend_x=0.02,
    legend_y=1.02,
    width=1100,
    height=900,
    enabled_border=False,
    disable_color_axis=True)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=ts,
    y=la_disabled_poisson_pkt_ts,
    name="Poisson - LA Disabled",
    line=lines['LA_Disabled'].copy(),
    mode="lines"))

fig.add_trace(go.Scatter(
    x=ts,
    y=la_enabled_poisson_pkt_ts,
    name="Poisson - LA Enabled",
    line=lines['LA_Enabled'].copy(),
    mode="lines"))

update_save_fig(
    fig=fig,
    colorbar_title=None,
    plot_title="Comparison of Poisson Traffic Flow",
    xlabel="Time [sec]", 
    ylabel="Number of sent packets",
    title_x=0.1,
    fname="poisson_flow_cmp.jpg",
    legend_x=0.02,
    legend_y=1.02,
    width=1100,
    height=900,
    enabled_border=False,
    disable_color_axis=True)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=ts,
    y=la_disabled_ratelim_pkt_ts,
    name="10Mbps - LA Disabled",
    line=lines['LA_Disabled'].copy(),
    mode="lines"))

fig.add_trace(go.Scatter(
    x=ts,
    y=la_enabled_ratetim_pkt_ts,
    name="10Mbps - LA Enabled",
    line=lines['LA_Enabled'].copy(),
    mode="lines"))

update_save_fig(
    fig=fig,
    colorbar_title=None,
    plot_title="Comparison of Rate-limited Traffic Flow",
    xlabel="Time [sec]", 
    ylabel="Number of sent packets",
    title_x=0.1,
    fname="ratelim_flow_cmp.jpg",
    legend_x=0.02,
    legend_y=1.02,
    width=1100,
    height=900,
    enabled_border=False,
    disable_color_axis=True)


from plotly.subplots import make_subplots

fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.1,
                    x_title='Time [sec]',
                    y_title='Number of pkts sent')

fig.add_trace(go.Scatter(
    x=ts,
    y=la_disabled_periodic_pkt_ts,
    name="Periodic - LA Disabled",
    line=dict(color="royalblue", width=2.0, dash="solid"),
    mode="lines"), row=1, col=1)

fig.add_trace(go.Scatter(
    x=ts,
    y=la_enabled_periodic_pkt_ts,
    name="Periodic - LA Enabled",
    line=dict(color="magenta", width=4.0, dash="dot"),
    mode="lines"), row=1, col=1)

fig.add_trace(go.Scatter(
    x=ts,
    y=la_disabled_poisson_pkt_ts,
    name="Poisson - LA Disabled",
    line=dict(color="red", width=2.0, dash="solid"),
    mode="lines"), row=2, col=1)

fig.add_trace(go.Scatter(
    x=ts,
    y=la_enabled_poisson_pkt_ts,
    name="Poisson - LA Enabled",
    line=dict(color="green", width=4.0, dash="dot"),
    mode="lines"), row=2, col=1)

fig.add_trace(go.Scatter(
    x=ts,
    y=la_disabled_ratelim_pkt_ts,
    name="10Mbps - LA Disabled",
    line=dict(color="goldenrod", width=2.0, dash="solid"),
    mode="lines"), row=3, col=1)

fig.add_trace(go.Scatter(
    x=ts,
    y=la_enabled_ratetim_pkt_ts,
    name="10Mbps - LA Enabled",
    line=dict(color="orange", width=4.0, dash="dot"),
    mode="lines"), row=3, col=1)

"""
update_save_fig(
    fig=fig,
    colorbar_title=None,
    plot_title="Comparison of Rate-limited Traffic Flow",
    xlabel="Time [sec]", 
    ylabel="Number of sent packets",
    title_x=0.1,
    fname="flow_cmp.jpg",
    legend_x=0.02,
    legend_y=1.02,
    width=1100,
    height=900,
    enabled_border=False,
    disable_color_axis=True)
"""


fig.update_layout(legend = dict(font = dict(family = "Courier", size = 20, color = "black"), orientation="h", x = 0.0, y=1.35))
#fig.update_layout(legend = dict(font = dict(family = "Courier", size = 25, color = "black")))

#fig.update_layout(title_text= "Flow comparison (Lookahead Enabled vs Disabled)")
#fig.update_layout(
#        title=go.layout.Title(
#            text="Flow comparison (Lookahead Enabled vs Disabled)",
#            font=dict(
#                    family="Courier",
#                    size=title_font_size
#                ),
#        xanchor = "auto",
#        yanchor = "middle"))
        
for i in fig['layout']['annotations']:
    i['font'] = dict(size=25)

fig.update_xaxes(title_font=dict(size=25, family='Courier'), tickfont=dict(family='Courier', size=23), nticks=5)
fig.update_yaxes(title_font=dict(size=25, family='Courier'), tickfont=dict(family='Courier', size=23))
fig.update_xaxes(ticks="outside", tickwidth=5, ticklen=0)
fig.update_yaxes(ticks="outside", tickwidth=5, ticklen=0)

fig.write_image(f"{home}/VT-S3FNet/experiment-data/figs/flow_cmp.jpg", width=1000, height=500)
