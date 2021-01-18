import plotly.graph_objects as go
import sys
import os
from os.path import expanduser
import numpy as np
import json
import math


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
gem5_cache_stats['matrix_multiply'].append(1.0 - 0.184522)


#8-way
gem5_cache_stats['bzip2'].append(1.0 - 0.066689)
gem5_cache_stats['sjeng'].append(1.0 - 0.025269)
gem5_cache_stats['h264ref'].append(1.0 - 0.005657)
gem5_cache_stats['sysbench'].append(1.0 - 0.000243)
gem5_cache_stats['matrix_multiply'].append(1.0 - 0.475120)


# Manual filling (from cache_stats/ directory) - titan
#2-way
titan_cache_stats['bzip2'].append(0.933145)
titan_cache_stats['sjeng'].append(0.988958)
titan_cache_stats['h264ref'].append(0.988474)
titan_cache_stats['sysbench'].append(0.999879)
titan_cache_stats['matrix_multiply'].append(0.812950)

#8-way
titan_cache_stats['bzip2'].append(0.933740)
titan_cache_stats['sjeng'].append(0.995727)
titan_cache_stats['h264ref'].append(0.990084)
titan_cache_stats['sysbench'].append(0.999879)
titan_cache_stats['matrix_multiply'].append(0.522898)


x = ["Sysbench", "Matrix-Mul", "Bzip2", "Sjeng", "H264ref"]

data = []
data.append(
    go.Bar(name=f"Gem-5: 32KB-2way", x=x, y=[
        gem5_cache_stats['sysbench'][0],
        gem5_cache_stats['matrix_multiply'][0],
        gem5_cache_stats['bzip2'][0],
        gem5_cache_stats['sjeng'][0],
        gem5_cache_stats['h264ref'][0]
    ], textfont=dict(family='Courier', size=20))
)


data.append(
    go.Bar(name=f"Compiler-Assisted: 32KB-2way", x=x, y=[
        titan_cache_stats['sysbench'][0],
        titan_cache_stats['matrix_multiply'][0],
        titan_cache_stats['bzip2'][0],
        titan_cache_stats['sjeng'][0],
        titan_cache_stats['h264ref'][0]
    ], textfont=dict(family='Courier', size=20))
)

data.append(
    go.Bar(name=f"Gem-5: 32KB-8way", x=x, y=[
        gem5_cache_stats['sysbench'][1],
        gem5_cache_stats['matrix_multiply'][1],
        gem5_cache_stats['bzip2'][1],
        gem5_cache_stats['sjeng'][1],
        gem5_cache_stats['h264ref'][1]
    ], textfont=dict(family='Courier', size=20))
)


data.append(
    go.Bar(name=f"Compiler-Assisted: 32KB-8way", x=x, y=[
        titan_cache_stats['sysbench'][1],
        titan_cache_stats['matrix_multiply'][1],
        titan_cache_stats['bzip2'][1],
        titan_cache_stats['sjeng'][1],
        titan_cache_stats['h264ref'][1]
    ], textfont=dict(family='Courier', size=20))
)

        
fig = go.Figure(data=data)
# Change the bar mode
fig.update_layout(barmode='group')
fig.update_layout(
    title=go.layout.Title(
        text="Cache hit rate prediction accuracy",
        font=dict(
                    family="Courier",
                    size=30
                ),
        xanchor = "auto",
        yanchor = "middle",
        #x=0.25
        y=0.95
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Benchmark",
            font=dict(
                family="Courier",
                size=25
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Cache Hit Rate [units]",
            font=dict(
                family="Courier",
                size=25
            )
        )
    ),
    legend=go.layout.Legend(
        x=0.1,
        y=1.12,
        font=dict(
            family="sans-serif",
            size=20,
            color="black"
        ),
    )
)
#fig.update_traces(texttemplate='%{text:.2s}sec', textposition='inside')
fig.update_layout(legend_orientation="h")
fig.update_yaxes(tickfont=dict(family='Courier', size=25))
fig.update_xaxes(tickfont=dict(family='Courier', size=25))
fig.write_image(f"cache_hits_comparison.jpg", width=1100, height=600)

