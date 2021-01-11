import os
import plotly.graph_objects as go


home = os.path.expanduser('~')
EXP_TYPES = ['MM', 'SAT', 'INT']
ARCHS = ['Skylake', 'Sandy_Bridge', 'Ivy_Bridge', 'Haswell']
CACHE_SIZES = ['128kb', '256kb']
CACHE_ASSOCS = [4, 8]


def get_avg_job_completion_time(arch, exp_type):
    dirPath = f"{home}/VT-S3FNet/experiment-data/Architecture_Timings/MPI_{exp_type}_{arch}"
    r = os.popen(f"""grep -nr "Avg-Job-Completion-Time" {dirPath}/* | tail -1 | cut -d " " -f 3""").read()
    return float(r)


def get_cache_hit_rate(exp_type, cache_size, cache_assoc):
    dirPath = f"{home}/VT-S3FNet/experiment-data/Cache_Hits/MPI_{exp_type}_CACHE_{cache_size}_{cache_assoc}way"
    r = os.popen(f"""grep -nr "Hit rate" {dirPath}/worker* | tail -1 | xargs | cut -d " " -f 4""").read()
    
    import re
    r = re.sub("[^0-9.]", "", r)
    import ast
    r = ast.literal_eval(r)
    return float(r)
    
timings = {}
cache_hits = {}

for size in CACHE_SIZES:
    for assoc in CACHE_ASSOCS:
        cache_hits[f"{size}_{assoc}"] = []
        for exp in EXP_TYPES:
            cache_hits[f"{size}_{assoc}"].append(get_cache_hit_rate(exp, size, assoc))

for exp in EXP_TYPES:
    timings[exp] = []
    for arch in ARCHS:
        timings[exp].append(get_avg_job_completion_time(arch, exp))
    

x = ARCHS
fig = go.Figure(data=[
    go.Bar(name='MPI Integration', x=x, y=timings['INT'], text=timings['INT'], textfont=dict(family='Courier', size=20)),
    go.Bar(name='MPI Circuit SAT', x=x, y=timings['SAT'], text=timings['SAT'], textfont=dict(family='Courier', size=20)),
    go.Bar(name='MPI Matrix Multiply', x=x, y=timings['MM'], text=timings['MM'], textfont=dict(family='Courier', size=20))
])
# Change the bar mode
fig.update_layout(barmode='group')
fig.update_layout(
    title=go.layout.Title(
        text="Job completion times across target architectures",
        font=dict(
                    family="Courier",
                    size=30
                ),
        xanchor = "auto",
        yanchor = "middle",
        #x=0.25
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Target processor architecture",
            font=dict(
                family="Courier",
                size=25
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Avg job completion times [sec]",
            font=dict(
                family="Courier",
                size=25
            )
        )
    ),
    legend=go.layout.Legend(
        x=0.02,
        y=1.05,
        font=dict(
            family="sans-serif",
            size=20,
            color="black"
        ),
    )
)
fig.update_traces(texttemplate='%{text:.2s}sec', textposition='inside')
fig.update_layout(legend_orientation="h")
fig.update_yaxes(tickfont=dict(family='Courier', size=25))
fig.update_xaxes(tickfont=dict(family='Courier', size=25))
fig.write_image(f"{home}/VT-S3FNet/experiment-data/figs/mpi_arch_timings.jpg", width=1100, height=600)


x = ["MPI Matrix Multiply", "MPI Circuit SAT", "MPI Integration"]
data = []
for size in CACHE_SIZES:
    for assoc in CACHE_ASSOCS:
        data.append(
            go.Bar(name=f"CACHE: {size}-{assoc}way", x=x, y=cache_hits[f"{size}_{assoc}"], textfont=dict(family='Courier', size=20))
        )
fig = go.Figure(data=data)
# Change the bar mode
fig.update_layout(barmode='group')
fig.update_layout(
    title=go.layout.Title(
        text="Cache hit rate across jobs",
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
            text="MPI Job Type",
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
fig.write_image(f"{home}/VT-S3FNet/experiment-data/figs/mpi_cache_hits.jpg", width=1100, height=600)

