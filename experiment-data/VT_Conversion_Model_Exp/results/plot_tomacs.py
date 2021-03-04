import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

archs = ["Sandy_Bridge", "Skylake"]
cmds = ["sysbench", "bzip2", "sjeng", "h264ref"]
configs = ["c1", "c2", "c3"]

accuracy = {
		"Normal": {},
		"Ins Counting": {},
		"Processor Model": {}
	   }

overheads = {
		"Kronos": {},
		"Intel PIN Ins-Counting" : {},
	        "Intel PIN P-Model" : {},
		"Compiler Ins-Counting": {},
		"Compiler P-Model": {}
	   }

overheads_std = {
		"Intel PIN Ins-Counting" : {},
	        "Intel PIN P-Model" : {},
		"Compiler Ins-Counting": {},
		"Compiler P-Model": {}
	   }



for arch in archs:
	for cmd in cmds:
		for cfg in configs:
			file_name = f"{script_dir}/accuracy/ins-counting/{arch}/vt_{cmd}_{cfg}_ts1000000/val.txt"
			time_taken = []
			with open(file_name, 'r') as f:
				lines = f.read().splitlines()
				time_taken = [float(x) for x in lines]
			if arch not in accuracy["Ins Counting"]:
				accuracy["Ins Counting"][arch] = {}
			if cmd not in accuracy["Ins Counting"][arch]:
				accuracy["Ins Counting"][arch][cmd] = {}
			accuracy["Ins Counting"][arch][cmd][cfg] = np.mean(time_taken)

			file_name = f"{script_dir}/accuracy/normal/{arch}/normal_{cmd}_{cfg}/val.txt"
			time_taken = []
			with open(file_name, 'r') as f:
				lines = f.read().splitlines()
				time_taken = [float(x) for x in lines]
			if arch not in accuracy["Normal"]:
				accuracy["Normal"][arch] = {}
			if cmd not in accuracy["Normal"][arch]:
				accuracy["Normal"][arch][cmd] = {}
			accuracy["Normal"][arch][cmd][cfg] = np.mean(time_taken)

			file_name = f"{script_dir}/accuracy/PModel/{arch}/vt_{cmd}_{cfg}_ts1000000/val.txt"
			time_taken = []
			with open(file_name, 'r') as f:
				lines = f.read().splitlines()
				time_taken = [float(x) for x in lines]
			if arch not in accuracy["Processor Model"]:
				accuracy["Processor Model"][arch] = {}
			if cmd not in accuracy["Processor Model"][arch]:
				accuracy["Processor Model"][arch][cmd] = {}
			accuracy["Processor Model"][arch][cmd][cfg] = np.mean(time_taken)
				

tslices = [1000, 10000, 100000, 1000000, 10000000]
num_iters = 5
for cmd in cmds:
	for tslice_idx, tslice in enumerate(tslices):
		iter_list = []
		for iter_no in range(1, num_iters + 1):	
			file_name = f"{script_dir}/overheads/ins-vt/vt_{cmd}_c1_ts{tslice}/overhead_{iter_no}.json"
			with open(file_name) as f:
				d = json.load(f)
				if cmd not in overheads["Kronos"]:
					overheads["Kronos"][cmd] = []
				iter_list.append(float(d["overhead_ratio"] * 1e9))
		overheads["Kronos"][cmd].append(np.mean(iter_list))

		iter_list = []
		for iter_no in range(1, num_iters + 1):	
			file_name = f"{script_dir}/overheads/app-vt-ins-counting/vt_{cmd}_c1_ts{tslice}/overhead_{iter_no}.json"
			with open(file_name) as f:
				d = json.load(f)
				if cmd not in overheads["Intel PIN Ins-Counting"]:
					overheads["Intel PIN Ins-Counting"][cmd] = []
					overheads_std["Intel PIN Ins-Counting"][cmd] = []
				
				iter_list.append(overheads["Kronos"][cmd][tslice_idx]/float(d["overhead_ratio"] * 1e9))
		overheads["Intel PIN Ins-Counting"][cmd].append(np.mean(iter_list))
		overheads_std["Intel PIN Ins-Counting"][cmd].append(np.std(iter_list))


		iter_list = []
		for iter_no in range(1, num_iters + 1):	
			file_name = f"{script_dir}/overheads/app-vt-pmodel/vt_{cmd}_c1_ts{tslice}/overhead_{iter_no}.json"
			with open(file_name) as f:
				d = json.load(f)
				if cmd not in overheads["Intel PIN P-Model"]:
					overheads["Intel PIN P-Model"][cmd] = []
					overheads_std["Intel PIN P-Model"][cmd] = []
				
				iter_list.append(overheads["Kronos"][cmd][tslice_idx]/float(d["overhead_ratio"] * 1e9))
		overheads["Intel PIN P-Model"][cmd].append(np.mean(iter_list))
		overheads_std["Intel PIN P-Model"][cmd].append(np.std(iter_list))


		iter_list = []
		for iter_no in range(1, num_iters + 1):	
			file_name = f"{script_dir}/overheads/compiler-ins-counting/vt_{cmd}_c1_ts{tslice}/overhead_{iter_no}.json"
			with open(file_name) as f:
				d = json.load(f)
				if cmd not in overheads["Compiler Ins-Counting"]:
					overheads["Compiler Ins-Counting"][cmd] = []
					overheads_std["Compiler Ins-Counting"][cmd] = []
				
				iter_list.append(overheads["Kronos"][cmd][tslice_idx]/float(d["overhead_ratio"] * 1e9))
		overheads["Compiler Ins-Counting"][cmd].append(np.mean(iter_list))
		overheads_std["Compiler Ins-Counting"][cmd].append(np.std(iter_list))


		iter_list = []
		for iter_no in range(1, num_iters + 1):	
			file_name = f"{script_dir}/overheads/compiler-pmodel/vt_{cmd}_c1_ts{tslice}/overhead_{iter_no}.json"
			with open(file_name) as f:
				d = json.load(f)
				if cmd not in overheads["Compiler P-Model"]:
					overheads["Compiler P-Model"][cmd] = []
					overheads_std["Compiler P-Model"][cmd] = []
				
				iter_list.append(overheads["Kronos"][cmd][tslice_idx]/float(d["overhead_ratio"] * 1e9))
		overheads["Compiler P-Model"][cmd].append(np.mean(iter_list))
		overheads_std["Compiler P-Model"][cmd].append(np.std(iter_list))
		

print ("Accuracy = ", accuracy)

cmd_labels = ["sysbench(cfg-1)", "sysbench(cfg-2)", "sysbench(cfg-3)", "bzip2(cfg-1)", "bzip2(cfg-2)", "bzip2(cfg-3)", "sjeng(cfg-1)", "sjeng(cfg-2)", "sjeng(cfg-3)", "h264ref(cfg-1)", "h264ref(cfg-2)", "h264ref(cfg-3)"]
normal_skylake_acc = []
ins_counting_skylake_acc = []
ins_counting_skylake_pct = []
pmodel_skylake_acc = []
pmodel_skylake_pct = []

normal_sb_acc = []
ins_counting_sb_acc = []
ins_counting_sb_pct = []
pmodel_sb_acc = []
pmodel_sb_pct = []

for cmd in cmds:
	for cfg in configs:
		normal_skylake_acc.append(accuracy["Normal"]["Skylake"][cmd][cfg])
		ins_counting_skylake_acc.append(accuracy["Ins Counting"]["Skylake"][cmd][cfg])
		pmodel_skylake_acc.append(accuracy["Processor Model"]["Skylake"][cmd][cfg])
		ins_counting_skylake_pct.append(100 * float(accuracy["Ins Counting"]["Skylake"][cmd][cfg]) / float(accuracy["Normal"]["Skylake"][cmd][cfg]))
		pmodel_skylake_pct.append(100 * float(accuracy["Processor Model"]["Skylake"][cmd][cfg]) / float(accuracy["Normal"]["Skylake"][cmd][cfg]))

		normal_sb_acc.append(accuracy["Normal"]["Sandy_Bridge"][cmd][cfg])
		ins_counting_sb_acc.append(accuracy["Ins Counting"]["Sandy_Bridge"][cmd][cfg])
		pmodel_sb_acc.append(accuracy["Processor Model"]["Sandy_Bridge"][cmd][cfg])
		ins_counting_sb_pct.append(100 * float(accuracy["Ins Counting"]["Sandy_Bridge"][cmd][cfg]) / float(accuracy["Normal"]["Sandy_Bridge"][cmd][cfg]))
		pmodel_sb_pct.append(100 * float(accuracy["Processor Model"]["Sandy_Bridge"][cmd][cfg]) / float(accuracy["Normal"]["Sandy_Bridge"][cmd][cfg]))

fig = go.Figure(data=[
    go.Bar(name='Native', x=cmd_labels, y=normal_skylake_acc),
    go.Bar(name='Processor Model', x=cmd_labels, y=pmodel_skylake_acc),
    go.Bar(name='Ins-Counting', x=cmd_labels, y=ins_counting_skylake_acc),
])
# Change the bar mode
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.update_layout(
    title=go.layout.Title(
        text="Virtual Time Conversion Accuracy (Intel Skylake Processor)",
	font=dict(
                family="Courier",
                size=25
            ),
	xanchor = "auto",
	yanchor = "middle",
	#x=0.25
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Command + (input configuration)",
            font=dict(
                family="Courier",
                size=25
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Completion time (secs) [Real/Virtual Time]",
            font=dict(
                family="Courier",
                size=30
            )
        ),
	type="log"
    ),
    legend=go.layout.Legend(
	x=0,
	y=1,
        font=dict(
            family="sans-serif",
            size=25,
            color="black"
        ),
        bgcolor="White",
        bordercolor="Black",
        borderwidth=5
    )
)
fig.update_yaxes(tickfont=dict(family='Courier', size=15), dtick=1)
fig.update_xaxes(tickfont=dict(family='Courier', size=15))
fig.write_image("skylake_accuracy.jpg", width=1100, height=900)


fig = go.Figure(data=[
    go.Bar(name='Native', x=cmd_labels, y=normal_sb_acc),
    go.Bar(name='Processor Model', x=cmd_labels, y=pmodel_sb_acc),
    go.Bar(name='Ins-Counting', x=cmd_labels, y=ins_counting_sb_acc),
])
# Change the bar mode
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.update_layout(
    title=go.layout.Title(
        text="Virtual Time Conversion Accuracy (Intel Sandy-Bridge Processor)",
	font=dict(
                family="Courier",
                size=25
            ),
	xanchor = "auto",
	yanchor = "middle",
	#x=0.25
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Command + (input configuration)",
            font=dict(
                family="Courier",
                size=25
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Completion time (secs) [Real/Virtual Time]",
            font=dict(
                family="Courier",
                size=30
            )
        ),
	type="log"
    ),
    legend=go.layout.Legend(
	x=0,
	y=1,
        font=dict(
            family="sans-serif",
            size=25,
            color="black"
        ),
        bgcolor="White",
        bordercolor="Black",
        borderwidth=5
    )
)
fig.update_yaxes(tickfont=dict(family='Courier', size=15), dtick=1)
fig.update_xaxes(tickfont=dict(family='Courier', size=15))
fig.write_image("sandy_bridge_accuracy.jpg", width=1100, height=900)


fig = go.Figure(data=[
    go.Bar(name='Sandy Bridge', x=cmd_labels, y=normal_sb_acc),
    go.Bar(name='Skylake', x=cmd_labels, y=normal_skylake_acc),
])
# Change the bar mode
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.update_layout(
    title=go.layout.Title(
        text="Native Execution Time of Test Benchmarks",
	font=dict(
                family="Courier",
                size=30
            ),
	xanchor = "auto",
	yanchor = "middle",
	x=0.15
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Command + (input configuration)",
            font=dict(
                family="Courier",
                size=25
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Completion time (secs) [Real Time]",
            font=dict(
                family="Courier",
                size=30
            )
        ),
	type="log"
    ),
    legend=go.layout.Legend(
	x=0,
	y=1,
        font=dict(
            family="sans-serif",
            size=25,
            color="black"
        ),
        bgcolor="White",
        bordercolor="Black",
        borderwidth=5
    )
)
fig.update_yaxes(tickfont=dict(family='Courier', size=15), dtick=1)
fig.update_xaxes(tickfont=dict(family='Courier', size=15))
fig.write_image("native_exec_time.jpg", width=1100, height=900)


fig = go.Figure(data=[
    go.Bar(name='Processor Model', x=cmd_labels, y=pmodel_skylake_pct, text=pmodel_skylake_pct,  textangle=-90, textfont=dict(family='Courier', size=20)),
    go.Bar(name='Ins-Counting', x=cmd_labels, y=ins_counting_skylake_pct, text=ins_counting_skylake_pct,  textangle=-90, textfont=dict(family='Courier', size=20)),
])
# Change the bar mode
fig.update_layout(barmode='group', xaxis_tickangle=45)
fig.update_layout(
    title=go.layout.Title(
        text="Virtual Time Conversion Accuracy (Intel Skylake Processor)",
	font=dict(
                family="Courier",
                size=25
            ),
	xanchor = "auto",
	yanchor = "middle",
	#x=0.25
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Command + (input configuration)",
            font=dict(
                family="Courier",
                size=25
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Normalized Completion Time [%]",
            font=dict(
                family="Courier",
                size=25
            )
        )
    ),
    legend=go.layout.Legend(
	x=0,
	y=1,
        font=dict(
            family="sans-serif",
            size=25,
            color="black"
        ),
        #bgcolor="White",
        #bordercolor="Black",
        #borderwidth=5
    )
)
#fig.update_layout(uniformtext_minsize=20)
fig.update_traces(texttemplate='%{text:.2s}%', textposition='inside')
fig.update_yaxes(tickfont=dict(family='Courier', size=25))
fig.update_xaxes(tickfont=dict(family='Courier', size=25))
fig.write_image("skylake_accuracy_pct.jpg", width=1100, height=600)


fig = go.Figure(data=[
    go.Bar(name='Processor Model', x=cmd_labels, y=pmodel_sb_pct, text=pmodel_sb_pct, textangle=-90, textfont=dict(family='Courier', size=20)),
    go.Bar(name='Ins-Counting', x=cmd_labels, y=ins_counting_sb_pct, text=ins_counting_sb_pct, textangle=-90, textfont=dict(family='Courier', size=20)),
])
# Change the bar mode
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.update_layout(
    title=go.layout.Title(
        text="Virtual Time Conversion Accuracy (Intel Sandy-Bridge Processor)",
	font=dict(
                family="Courier",
                size=25
            ),
	xanchor = "auto",
	yanchor = "middle",
	#x=0.25
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Command + (input configuration)",
            font=dict(
                family="Courier",
                size=25
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Normalized Completion Time [%]",
            font=dict(
                family="Courier",
                size=25
            )
        )
    ),
    legend=go.layout.Legend(
	x=0,
	y=1,
        font=dict(
            family="sans-serif",
            size=25,
            color="black"
        ),
        #bgcolor="White",
        #bordercolor="Black",
        #borderwidth=5
    )
)
fig.update_traces(texttemplate='%{text:.2s}%', textposition='inside')
fig.update_yaxes(tickfont=dict(family='Courier', size=25))
fig.update_xaxes(tickfont=dict(family='Courier', size=25))
fig.write_image("sandy_bridge_accuracy_pct.jpg", width=1100, height=600)

print ("Overheads = ", overheads)
print ("Overheads_std = ", overheads_std)
tslices = [1, 10, 100, 1000, 10000]
marker_size=25
#fig = go.Figure()
fig = make_subplots(rows=1, cols=2, x_title='Timeslice (us)',
                    y_title='Relative Speedup (w.r.t INS-SCHED[H])',
		    horizontal_spacing = 0.08, vertical_spacing = 0.13,
                    subplot_titles=('(a) Compiler Assisted (Ins-Counting)','(b) Intel PIN tool (Ins-Counting)'))
fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler Ins-Counting"]["sysbench"],
    error_y=dict(type='data', array=overheads_std["Compiler Ins-Counting"]["sysbench"]),
    name='sysbench',
    marker=dict(color='blue', size=marker_size, symbol='circle'),
    line=dict(
                color="blue",
                width=4.0,
                dash="dashdot",
            )
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler Ins-Counting"]["bzip2"],
    error_y=dict(type='data', array=overheads_std["Compiler Ins-Counting"]["bzip2"]),
    name='bzip2',
    marker=dict(color='goldenrod', size=marker_size, symbol='square'),
    line=dict(
                color="goldenrod",
                width=4.0,
                dash="dash",
            )
), row=1, col=1)


fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler Ins-Counting"]["sjeng"],
    error_y=dict(type='data', array=overheads_std["Compiler Ins-Counting"]["sjeng"]),
    name='sjeng',
    marker=dict(color='red', size=marker_size, symbol='diamond'),
    line=dict(
                color="red",
                width=4.0,
                dash="longdash",
            ),
    
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler Ins-Counting"]["h264ref"],
    error_y=dict(type='data', array=overheads_std["Compiler Ins-Counting"]["h264ref"]),
    name='h264ref',
    marker=dict(color='green', size=marker_size, symbol='triangle-up-dot'),
            line=dict(
                color="green",
                width=4.0,
                dash="solid",
            ),
    
), row=1, col=1)


fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Intel PIN Ins-Counting"]["sysbench"],
    error_y=dict(type='data', array=overheads_std["Intel PIN Ins-Counting"]["sysbench"]),
    name='sysbench',
    showlegend=False,
    marker=dict(color='blue', size=marker_size, symbol='circle'),
    line=dict(
                color="blue",
                width=4.0,
                dash="dashdot",
            )
),     row=1, col=2)
fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Intel PIN Ins-Counting"]["bzip2"],
    error_y=dict(type='data', array=overheads_std["Intel PIN Ins-Counting"]["bzip2"]),
    name='bzip2',
    showlegend=False,
    marker=dict(color='goldenrod', size=marker_size, symbol='square'),
    line=dict(
                color="goldenrod",
                width=4.0,
                dash="dash",
            )
), row=1, col=2)


fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Intel PIN Ins-Counting"]["sjeng"],
    error_y=dict(type='data', array=overheads_std["Intel PIN Ins-Counting"]["sjeng"]),
    name='sjeng',
    showlegend=False,
    marker=dict(color='red', size=marker_size, symbol='diamond'),
    line=dict(
                color="red",
                width=4.0,
                dash="longdash",
            )
    
), row=1, col=2)

fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Intel PIN Ins-Counting"]["h264ref"],
    error_y=dict(type='data', array=overheads_std["Intel PIN Ins-Counting"]["h264ref"]),
    name='h264ref',
    showlegend=False,
    marker=dict(color='green', size=marker_size, symbol='triangle-up-dot'),
            line=dict(
                color="green",
                width=4.0,
                dash="solid",
            )
    
), row=1, col=2)

fig.update_layout(
    title=go.layout.Title(
        text="Overhead Comparison (INS-SCHED[H] vs INS-SCHED[BI])",
	font=dict(
                family="Courier",
                size=30
            ),
	xanchor = "auto",
	yanchor = "middle",
	x=0.25
    ), 
    legend=go.layout.Legend(
	font=dict(
            family="sans-serif",
            size=30,
            color="black"
        )
    ),
    yaxis=dict(
            range=[0, 4]
    )
)

for i in fig['layout']['annotations']:
    i['font'] = dict(size=25)

#fig.update_xaxes(type="log", dtick=1)
fig.update_xaxes(title_font=dict(size=30, family='Courier'), tickfont=dict(family='Courier', size=25), type="log", dtick=1)
fig.update_yaxes(title_font=dict(size=30, family='Courier'), tickfont=dict(family='Courier', size=25))
fig.write_image("ins_counting_overhead_comparison_kronos.png", width=1600, height=900)




tslices = [1, 10, 100, 1000, 10000]
marker_size=25
#fig = go.Figure()
fig = make_subplots(rows=1, cols=2, x_title='Timeslice (us)',
                    y_title='Relative Speedup (w.r.t INS-SCHED[H])',
		    horizontal_spacing = 0.08, vertical_spacing = 0.13,
                    subplot_titles=('(a) Compiler Assisted (P-Model)','(b) Intel PIN tool (P-Model)'))
fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler P-Model"]["sysbench"],
    error_y=dict(type='data', array=overheads_std["Compiler P-Model"]["sysbench"]),
    name='sysbench',
    marker=dict(color='blue', size=marker_size, symbol='circle'),
    line=dict(
                color="blue",
                width=4.0,
                dash="dashdot",
            )
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler P-Model"]["bzip2"],
    error_y=dict(type='data', array=overheads_std["Compiler P-Model"]["bzip2"]),
    name='bzip2',
    marker=dict(color='goldenrod', size=marker_size, symbol='square'),
    line=dict(
                color="goldenrod",
                width=4.0,
                dash="dash",
            )
), row=1, col=1)


fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler P-Model"]["sjeng"],
    error_y=dict(type='data', array=overheads_std["Compiler P-Model"]["sjeng"]),
    name='sjeng',
    marker=dict(color='red', size=marker_size, symbol='diamond'),
    line=dict(
                color="red",
                width=4.0,
                dash="longdash",
            ),
    
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler P-Model"]["h264ref"],
    error_y=dict(type='data', array=overheads_std["Compiler P-Model"]["h264ref"]),
    name='h264ref',
    marker=dict(color='green', size=marker_size, symbol='triangle-up-dot'),
            line=dict(
                color="green",
                width=4.0,
                dash="solid",
            ),
    
), row=1, col=1)


fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Intel PIN P-Model"]["sysbench"],
    error_y=dict(type='data', array=overheads_std["Intel PIN P-Model"]["sysbench"]),
    name='sysbench',
    showlegend=False,
    marker=dict(color='blue', size=marker_size, symbol='circle'),
    line=dict(
                color="blue",
                width=4.0,
                dash="dashdot",
            )
),     row=1, col=2)
fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Intel PIN P-Model"]["bzip2"],
    error_y=dict(type='data', array=overheads_std["Intel PIN P-Model"]["bzip2"]),
    name='bzip2',
    showlegend=False,
    marker=dict(color='goldenrod', size=marker_size, symbol='square'),
    line=dict(
                color="goldenrod",
                width=4.0,
                dash="dash",
            )
), row=1, col=2)


fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Intel PIN P-Model"]["sjeng"],
    error_y=dict(type='data', array=overheads_std["Intel PIN P-Model"]["sjeng"]),
    name='sjeng',
    showlegend=False,
    marker=dict(color='red', size=marker_size, symbol='diamond'),
    line=dict(
                color="red",
                width=4.0,
                dash="longdash",
            )
    
), row=1, col=2)

fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Intel PIN P-Model"]["h264ref"],
    error_y=dict(type='data', array=overheads_std["Intel PIN P-Model"]["h264ref"]),
    name='h264ref',
    showlegend=False,
    marker=dict(color='green', size=marker_size, symbol='triangle-up-dot'),
            line=dict(
                color="green",
                width=4.0,
                dash="solid",
            )
    
), row=1, col=2)

fig.update_layout(
    title=go.layout.Title(
        text="Overhead Comparison [INS-SCHED[H] vs INS-SCHED[BI] Processor Model]",
	font=dict(
                family="Courier",
                size=30
            ),
	xanchor = "auto",
	yanchor = "middle",
	x=0.1
    ), 
    legend=go.layout.Legend(
	font=dict(
            family="sans-serif",
            size=30,
            color="black"
        )
    ),
    yaxis=dict(
            range=[0, 4]
    )
)

for i in fig['layout']['annotations']:
    i['font'] = dict(size=25)

#fig.update_xaxes(type="log", dtick=1)
fig.update_xaxes(title_font=dict(size=30, family='Courier'), tickfont=dict(family='Courier', size=20), type="log", dtick=1)
fig.update_yaxes(title_font=dict(size=30, family='Courier'), tickfont=dict(family='Courier', size=20))
fig.write_image("pmodel_overhead_comparison_kronos.png", width=1600, height=900)

"""
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler P-Model"]["sysbench"],
    name='sysbench',
    marker=dict(color='blue', size=marker_size, symbol='circle'),
    line=dict(
                color="blue",
                width=4.0,
                dash="dashdot",
            )
))
fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler P-Model"]["bzip2"],
    name='bzip2',
    marker=dict(color='goldenrod', size=marker_size, symbol='square'),
    line=dict(
                color="goldenrod",
                width=4.0,
                dash="dash",
            )
))


fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler P-Model"]["sjeng"],
    name='sjeng',
    marker=dict(color='red', size=marker_size, symbol='diamond'),
    line=dict(
                color="red",
                width=4.0,
                dash="longdash",
            ),
    
))

fig.add_trace(go.Scatter(
    x=tslices, y=overheads["Compiler P-Model"]["h264ref"],
    name='h264ref',
    marker=dict(color='green', size=marker_size, symbol='triangle-up-dot'),
            line=dict(
                color="green",
                width=4.0,
                dash="solid",
            ),
    
))


fig.update_layout(
    title=go.layout.Title(
        text="Overhead Comparison [Kronos vs Compiler Assisted Processor Model]",
	font=dict(
                family="Courier",
                size=30
            ),
	xanchor = "auto",
	yanchor = "middle",
	x=0
    ), 
   xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Timeslice (us)",
            font=dict(
                family="Courier",
                size=25
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Relative Speedup [w.r.t Kronos (INS-SCHED) ]",
            font=dict(
                family="Courier",
                size=25
            )
        )
    ),
    legend=go.layout.Legend(
	font=dict(
            family="sans-serif",
            size=30,
            color="black"
        )
    )
)

#fig.update_xaxes(type="log", dtick=1)
fig.update_xaxes(title_font=dict(size=25, family='Courier'), tickfont=dict(family='Courier', size=20), type="log", dtick=1)
fig.update_yaxes(title_font=dict(size=25, family='Courier'), tickfont=dict(family='Courier', size=20))
fig.write_image("overhead_comparison_pmodel.png", width=1200, height=900)
"""




