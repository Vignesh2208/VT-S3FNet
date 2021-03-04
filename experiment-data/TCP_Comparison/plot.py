
import json
import os
import sys
import plotly.graph_objects as go
import numpy as np


home = os.path.expanduser('~')

aggregation_wind_size = 1

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

incorrect_tcp_periodic_1 = f"{home}/VT-S3FNet/experiment-data/TCP_Comparison/Incorrect_Run_1_TCP_LA_Enabled_nemus_20_periodic_period_200000_txsize_2000/stats.json"
incorrect_tcp_periodic_2 = f"{home}/VT-S3FNet/experiment-data/TCP_Comparison/Incorrect_Run_2_TCP_LA_Enabled_nemus_20_periodic_period_200000_txsize_2000/stats.json"

correct_tcp_periodic_1 = f"{home}/VT-S3FNet/experiment-data/TCP_Comparison/Correct_Run_1_TCP_LA_Enabled_nemus_20_periodic_period_200000_txsize_2000/stats.json"
correct_tcp_periodic_2 = f"{home}/VT-S3FNet/experiment-data/TCP_Comparison/Correct_Run_2_TCP_LA_Enabled_nemus_20_periodic_period_200000_txsize_2000/stats.json"




incorrect_tcp_periodic_json_1 = {}
incorrect_tcp_periodic_json_2 = {}
correct_tcp_periodic_json_1 = {}
correct_tcp_periodic_json_2 = {}

incorrect_tcp_periodic_pkt_counts_1 = []
incorrect_tcp_periodic_pkt_counts_2 = []
correct_tcp_periodic_pkt_counts_1 = []
correct_tcp_periodic_pkt_counts_2 = []

incorrect_tcp_periodic_pkt_ts_1 = []
incorrect_tcp_periodic_pkt_ts_2 = []
correct_tcp_periodic_pkt_ts_1 = []
correct_tcp_periodic_pkt_ts_2 = []



with open(incorrect_tcp_periodic_1, 'r') as f:
    incorrect_tcp_periodic_json_1 = json.load(f)

with open(incorrect_tcp_periodic_2, 'r') as f:
    incorrect_tcp_periodic_json_2 = json.load(f)

with open(correct_tcp_periodic_1, 'r') as f:
    correct_tcp_periodic_json_1 = json.load(f)

with open(correct_tcp_periodic_2, 'r') as f:
    correct_tcp_periodic_json_2 = json.load(f)

for entry in incorrect_tcp_periodic_json_1["pkt_send_counts"]:
    incorrect_tcp_periodic_pkt_counts_1.append(entry["value"])

for entry in incorrect_tcp_periodic_json_2["pkt_send_counts"]:
    incorrect_tcp_periodic_pkt_counts_2.append(entry["value"])

for entry in correct_tcp_periodic_json_1["pkt_send_counts"]:
    correct_tcp_periodic_pkt_counts_1.append(entry["value"])

for entry in correct_tcp_periodic_json_2["pkt_send_counts"]:
    correct_tcp_periodic_pkt_counts_2.append(entry["value"])


def aggregate_bursts(ls):
    res = []
    agg = 0
    for value in ls:
        if value == 0 and agg > 0:
            res.append(agg)
            agg = 0
        else:
            agg += value
    return res

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



incorrect_tcp_periodic_pkt_ts_1 = aggregate(incorrect_tcp_periodic_pkt_counts_1, aggregation_wind_size)
correct_tcp_periodic_pkt_ts_1 = aggregate(correct_tcp_periodic_pkt_counts_1, aggregation_wind_size)

incorrect_tcp_periodic_pkt_ts_2 = aggregate(incorrect_tcp_periodic_pkt_counts_2, aggregation_wind_size)
correct_tcp_periodic_pkt_ts_2 = aggregate(correct_tcp_periodic_pkt_counts_2, aggregation_wind_size)

#incorrect_tcp_periodic_pkt_ts = aggregate_bursts(incorrect_tcp_periodic_pkt_counts)[1:]
#correct_tcp_periodic_pkt_ts = aggregate_bursts(correct_tcp_periodic_pkt_counts)[1:]


# incorrect_tcp_num_retx_pkts = []
# correct_tcp_num_retx_pkts = []

# for value in incorrect_tcp_periodic_pkt_ts:
#     incorrect_tcp_num_retx_pkts.append(value - min(incorrect_tcp_periodic_pkt_ts))

# for value in correct_tcp_periodic_pkt_ts:
#     correct_tcp_num_retx_pkts.append(value - min(correct_tcp_periodic_pkt_ts))



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


# lines = {
#     'NATIVE_TCP' :  dict(color="blue", width=4.0, dash="dash"),
#     'VT_TCP'  : dict(color="green", width=2.0, dash="solid")
# }

# fig = go.Figure()
# fig.add_trace(go.Scatter(
#     x=ts,
#     y=incorrect_tcp_periodic_pkt_ts,
#     name="With native TCP sockets",
#     line=lines['NATIVE_TCP'].copy(),
#     mode="lines"))

# fig.add_trace(go.Scatter(
#     x=ts,
#     y=correct_tcp_periodic_pkt_ts,
#     name="With VT-TCP sockets",
#     line=lines['VT_TCP'].copy(),
#     mode="lines"))

# update_save_fig(
#     fig=fig,
#     colorbar_title=None,
#     plot_title="Comparison of Periodic Traffic Flow",
#     xlabel="Time [sec]", 
#     ylabel="Number of sent packets",
#     title_x=0.1,
#     fname="tcp_flow_cmp.jpg",
#     legend_x=0.02,
#     legend_y=1.02,
#     width=1100,
#     height=900,
#     enabled_border=False,
#     disable_color_axis=True)


from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.1,
                    x_title='Time [sec]',
                    y_title='Number of pkts sent')

fig.add_trace(go.Scatter(
    x=ts,
    y=incorrect_tcp_periodic_pkt_ts_1,
    name="Native TCP sock (Trial-1)",
    line=dict(color="red", width=4.0, dash="solid"),
    mode="lines"), row=1, col=1)

fig.add_trace(go.Scatter(
    x=ts,
    y=incorrect_tcp_periodic_pkt_ts_2,
    name="Native TCP sock (Trial-2)",
    line=dict(color="green", width=2.0, dash="dash"),
    mode="lines"), row=1, col=1)

fig.add_trace(go.Scatter(
    x=ts,
    y=correct_tcp_periodic_pkt_ts_1,
    name="Virtual TCP sock (Trial-1)",
    line=dict(color="royalblue", width=4.0, dash="dot"),
    mode="lines"), row=2, col=1)

fig.add_trace(go.Scatter(
    x=ts,
    y=correct_tcp_periodic_pkt_ts_2,
    name="Virtual TCP sock (Trial-2)",
    line=dict(color="magenta", width=2.0, dash="solid"),
    mode="lines"), row=2, col=1)





fig.update_layout(legend = dict(font = dict(family = "Courier", size = 24, color = "black"), orientation="h", x = 0.0, y=1.3))
#fig.update_layout(title_text= "Flow comparison (Lookahead Enabled vs Disabled)")
#fig.update_layout(
#        title=go.layout.Title(
#            text="Flow comparison (Native vs VT-integrated TCP layer)",
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

fig.write_image(f"{home}/VT-S3FNet/experiment-data/figs/tcp_cmp.jpg", width=1000, height=500)
