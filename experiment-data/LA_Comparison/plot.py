import json
import matplotlib.pyplot as plt

la_disabled = '/home/titan/VT-S3FNet/experiment-data/LXC_TCP_LA_Disabled_Rate_1/stats.json'
la_enabled = '/home/titan/VT-S3FNet/experiment-data/LXC_TCP_LA_Enabled_Rate_1/stats.json'

aggregation_wind_size = 5

la_disabled_json = {}
la_disabled_pkt_counts = []

la_enabled_json = {}
la_enabled_pkt_counts = []

with open(la_disabled, 'r') as f:
    la_disabled_json = json.load(f)

with open(la_enabled, 'r') as f:
    la_enabled_json = json.load(f)

for entry in la_disabled_json["pkt_send_counts"]:
    la_disabled_pkt_counts.append(entry["value"])

for entry in la_enabled_json["pkt_send_counts"]:
    la_enabled_pkt_counts.append(entry["value"])


plt.plot(la_disabled_pkt_counts)
plt.ylabel('Num-pkts')
plt.xlabel('slot')
plt.title('LA-Disabled')
plt.show()

plt.plot(la_enabled_pkt_counts)
plt.ylabel('Num-pkts')
plt.xlabel('slot')
plt.title('LA-Enabled')
plt.show()


