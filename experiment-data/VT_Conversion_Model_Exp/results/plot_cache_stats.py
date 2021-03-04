import plotly.graph_objects as go
import sys
import os
from os.path import expanduser
import numpy as np
import json
import math


legend_x=0.0
legend_y=1.2

legend_font_size = 25
xlabel_font_size = 25
ylabel_font_size = 25

gem5_cache_stats = {}
gem5_cache_stats['bzip2'] = []
gem5_cache_stats['sjeng'] = []
gem5_cache_stats['h264ref'] = []
gem5_cache_stats['sysbench'] = []
gem5_cache_stats['matrix_multiply'] = []

titan_cache_stats = {}
titan_cache_stats['bzip2'] = []
titan_cache_stats['sjeng'] = []
titan_cache_stats['h264ref'] = []
titan_cache_stats['sysbench'] = []
titan_cache_stats['matrix_multiply'] = []

# Manual filling (from cache_stats/ directory) - Gem5
#2-way
gem5_cache_stats['bzip2'].append(1.0 - 0.067373)
gem5_cache_stats['sjeng'].append(1.0 - 0.028564)
gem5_cache_stats['h264ref'].append(1.0 - 0.00769)
gem5_cache_stats['sysbench'].append(1.0 - 0.000247)

# 32-kb 2-way
gem5_cache_stats['matrix_multiply'].append(1.0 - 0.184522)
# 128-kb 2-way
gem5_cache_stats['matrix_multiply'].append(1.0 - 0.549909)


#8-way
gem5_cache_stats['bzip2'].append(1.0 - 0.066689)
gem5_cache_stats['sjeng'].append(1.0 - 0.025269)
gem5_cache_stats['h264ref'].append(1.0 - 0.005657)
gem5_cache_stats['sysbench'].append(1.0 - 0.000243)

# 32-kb 8-way
gem5_cache_stats['matrix_multiply'].append(1.0 - 0.475120)
# 128-kb 8-way
gem5_cache_stats['matrix_multiply'].append(1.0 - 0.549908)


# Manual filling (from cache_stats/ directory) - titan
#2-way
titan_cache_stats['bzip2'].append(0.933145)
titan_cache_stats['sjeng'].append(0.988958)
titan_cache_stats['h264ref'].append(0.988474)
titan_cache_stats['sysbench'].append(0.999879)

# 32 kb 2-way
titan_cache_stats['matrix_multiply'].append(0.812950)

# 128 kb 2-way
titan_cache_stats['matrix_multiply'].append(1 - 0.562391)

#8-way
titan_cache_stats['bzip2'].append(0.933740)
titan_cache_stats['sjeng'].append(0.995727)
titan_cache_stats['h264ref'].append(0.990084)
titan_cache_stats['sysbench'].append(0.999879)

# 32 kb 8-way
titan_cache_stats['matrix_multiply'].append(0.522898)

# 128 kb 8-way
titan_cache_stats['matrix_multiply'].append(1 - 0.562391)


#x = ["sysbench", "matrix-multiply", "bzip2", "sjeng", "h264ref"]

x = ["sysbench", "bzip2", "sjeng", "h264ref"]



data = []
data.append(
    go.Bar(name=f"gem5: 32KB-2way", x=x, y=[
        gem5_cache_stats['sysbench'][0],
        gem5_cache_stats['bzip2'][0],
        gem5_cache_stats['sjeng'][0],
        gem5_cache_stats['h264ref'][0]
    ], textfont=dict(family='Courier', size=legend_font_size),
    marker_color='rgb(58, 78, 159)')
)


data.append(
    go.Bar(name=f"Titan: 32KB-2way", x=x, y=[
        titan_cache_stats['sysbench'][0],
        titan_cache_stats['bzip2'][0],
        titan_cache_stats['sjeng'][0],
        titan_cache_stats['h264ref'][0]
    ], textfont=dict(family='Courier', size=legend_font_size),
    marker_color='rgb(111, 64, 112)')
)

data.append(
    go.Bar(name=f"gem5: 32KB-8way", x=x, y=[
        gem5_cache_stats['sysbench'][1],
        gem5_cache_stats['bzip2'][1],
        gem5_cache_stats['sjeng'][1],
        gem5_cache_stats['h264ref'][1]
    ], textfont=dict(family='Courier', size=legend_font_size),
    marker_color='indianred')
)


data.append(
    go.Bar(name=f"Titan: 32KB-8way", x=x, y=[
        titan_cache_stats['sysbench'][1],
        titan_cache_stats['bzip2'][1],
        titan_cache_stats['sjeng'][1],
        titan_cache_stats['h264ref'][1]
    ], textfont=dict(family='Courier', size=legend_font_size),
    marker_color='lightsalmon')
)

        
fig = go.Figure(data=data)
# Change the bar mode
fig.update_layout(barmode='group')
fig.update_layout(
    # title=go.layout.Title(
    #     text="Cache hit rate predictions",
    #     font=dict(
    #                 family="Courier",
    #                 size=25
    #             ),
    #     xanchor = "auto",
    #     yanchor = "middle",
    # ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Benchmark",
            font=dict(
                family="Courier",
                size=xlabel_font_size
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Cache Hit Rate [units]",
            font=dict(
                family="Courier",
                size=ylabel_font_size
            )
        )
    ),
    legend=go.layout.Legend(
        x=legend_x,
        y=legend_y + 0.1,
        font=dict(
            family="sans-serif",
            size=legend_font_size,
            color="black"
        ),
    )
)
#fig.update_traces(texttemplate='%{text:.2s}sec', textposition='inside')

#fig.update_layout(title_x=0.5)
fig.update_layout(legend_orientation="h")
fig.update_yaxes(tickfont=dict(family='Courier', size=ylabel_font_size))
fig.update_xaxes(tickfont=dict(family='Courier', size=xlabel_font_size))
fig.write_image(f"cache_hits_comparison.jpg", width=900, height=500)

x=['32 KB 2-way', '128 KB 2-way', '32 KB 8-way', '128 KB 8-way']

fig = go.Figure(data=[
    go.Bar(name='gem5', x=x, y=gem5_cache_stats['matrix_multiply'], marker_color='indianred'),
    go.Bar(name='Titan', x=x, y=titan_cache_stats['matrix_multiply'], marker_color='lightsalmon')
])

fig.update_layout(barmode='group')
fig.update_layout(
    # title=go.layout.Title(
    #     text="Matrix multiplication: Cache hit rate predictions",
    #     font=dict(
    #                 family="Courier",
    #                 size=25
    #             ),
    #     xanchor = "auto",
    #     yanchor = "middle",
    # ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Cache configuration",
            font=dict(
                family="Courier",
                size=xlabel_font_size
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Cache Hit Rate [units]",
            font=dict(
                family="Courier",
                size=ylabel_font_size
            )
        )
    ),
    legend=go.layout.Legend(
        x=legend_x,
        y=legend_y,
        font=dict(
            family="Courier",
            size=legend_font_size,
            color="black"
        ),
    )
)

#fig.update_layout(title_x=0.5)
fig.update_layout(legend_orientation="h")
fig.update_yaxes(tickfont=dict(family='Courier', size=ylabel_font_size))
fig.update_xaxes(tickfont=dict(family='Courier', size=xlabel_font_size))
fig.write_image(f"matmul_cache_hits_comparison.jpg", width=800, height=600)

