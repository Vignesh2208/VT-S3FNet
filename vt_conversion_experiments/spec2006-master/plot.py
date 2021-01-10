import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = ['bzip2', 'sjeng', 'h264ref']
normal = [2.397338, 33.743752, 46.514449]
pmodel = [5.532093, 26.598927, 46.521738]
ins_counting = [4.01, 17.55, 25.966672]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/3, normal, width/3, label='Native')
rects2 = ax.bar(x, pmodel, width/3, label='PModel')
rects3 = ax.bar(x + width/3, ins_counting, width/3, label='Ins-Counting')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Time taken [real or virtual time] (secs)')
ax.set_title('Accuracy of virtual time model')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


fig.tight_layout()
plt.show()
