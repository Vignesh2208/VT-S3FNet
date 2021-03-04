import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

legend_x=0.0
legend_y=1.2

title_font_size = 25
xlabel_font_size = 25
ylabel_font_size = 25
legend_font_size = 25

archs = ["Sandy_Bridge", "Skylake"]
cmds = ["sysbench", "bzip2", "sjeng", "h264ref"]
configs = ["c2"]

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

cmd_labels = ["sysbench", "bzip2", "sjeng", "h264ref"]
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
    go.Bar(name='Processor model [Skylake]', x=cmd_labels, y=pmodel_skylake_pct, text=pmodel_skylake_pct,  textangle=-90, textfont=dict(family='Courier', size=20), marker_color='rgb(58, 78, 159)'),
    go.Bar(name='Processor model [Sandy bridge]', x=cmd_labels, y=pmodel_sb_pct, text=pmodel_sb_pct,  textangle=-90, textfont=dict(family='Courier', size=20), marker_color='indianred'),
    go.Bar(name='Plain ins-counting [Skylake]', x=cmd_labels, y=ins_counting_skylake_pct, text=ins_counting_skylake_pct,  textangle=-90, textfont=dict(family='Courier', size=20), marker_color='rgb(111, 64, 112)'),
    go.Bar(name='Plain ins-counting [Sandy bridge]', x=cmd_labels, y=ins_counting_sb_pct, text=ins_counting_sb_pct,  textangle=-90, textfont=dict(family='Courier', size=20), marker_color='lightsalmon'),
])
# Change the bar mode
fig.update_layout(barmode='group', xaxis_tickangle=45)
fig.update_layout(
    # title=go.layout.Title(
    #     text="Virtual Time Conversion Accuracy",
    #     font=dict(
    #                 family="Courier",
    #                 size=title_font_size
    #             ),
    #     xanchor = "auto",
    #     yanchor = "middle",
    #     x=0.5
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
            text="Normalized Completion Time [%]",
            font=dict(
                family="Courier",
                size=ylabel_font_size
            )
        ),
        range=[0, 600]
    ),
    legend=go.layout.Legend(
        x=legend_x,
        y=legend_y,
        font=dict(
                family="sans-serif",
                size=legend_font_size,
                color="black"
            )
    ),
)
#fig.update_layout(uniformtext_minsize=20)

fig.update_layout(title_x=0.5)
fig.update_layout(legend_orientation="h")
fig.update_traces(texttemplate='%{text:.2s}%', textposition='inside')
fig.update_yaxes(tickfont=dict(family='Courier', size=ylabel_font_size))
fig.update_xaxes(tickfont=dict(family='Courier', size=xlabel_font_size))
fig.write_image("vt_conversion_accuracy_pct.jpg", width=1000, height=500)



print ("Overheads = ", overheads)
print ("Overheads_std = ", overheads_std)
tslices = [1000, 10000, 100000, 1000000, 10000000]
marker_size=25
fig = go.Figure()

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
))
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
))


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
    
))

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
    
))



fig.update_layout(
    # title=go.layout.Title(
    #     text="Ins counting overhead comparison",
    #     font=dict(
    #                 family="Courier",
    #                 size=title_font_size
    #             ),
    #     xanchor = "auto",
    #     yanchor = "middle",
    # ), 
    legend=go.layout.Legend(
        x=legend_x,
        y=legend_y,
        font=dict(
                family="Courier",
                size=legend_font_size,
                color="black"
            )
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Burst length [insns]",
            font=dict(
                family="Courier",
                size=xlabel_font_size
            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Relative Speedup [w.r.t Kronos]",
            font=dict(
                family="Courier",
                size=ylabel_font_size
            )
        ),
        range=[0, 4]
    ),

)

for i in fig['layout']['annotations']:
    i['font'] = dict(size=25)

#fig.update_xaxes(type="log", dtick=1)
#fig.update_layout(title_text='Ins counting overhead comparison', title_x=0.5)
fig.update_layout(legend_orientation="h")
fig.update_xaxes(title_font=dict(size=xlabel_font_size, family='Courier'), tickfont=dict(family='Courier', size=xlabel_font_size), type="log", dtick=1)
fig.update_yaxes(title_font=dict(size=xlabel_font_size, family='Courier'), tickfont=dict(family='Courier', size=ylabel_font_size))
fig.write_image("ins_count_overhead_comparison.png", width=900, height=550)



