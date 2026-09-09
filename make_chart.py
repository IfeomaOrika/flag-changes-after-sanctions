import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with open('flag_hops.csv') as f:
    rows = list(csv.DictReader(f))

days = [int(r['days_to_hop']) for r in rows]

buckets = [0] * 13
labels = ['0-30', '31-60', '61-90', '91-120', '121-150', '151-180',
          '181-210', '211-240', '241-270', '271-300', '301-330',
          '331-365', '365+']

for d in days:
    if d > 365:
        buckets[12] += 1
    else:
        idx = min((d - 1) // 30, 11)
        buckets[idx] += 1

fig, ax = plt.subplots(figsize=(10, 5))

colours = ['#8B2635' if i < 3 else '#B8B8B8' for i in range(13)]
bars = ax.bar(labels, buckets, color=colours, edgecolor='white', linewidth=0.7)

for bar, count in zip(bars, buckets):
    if count > 0:
        ax.text(bar.get_x() + bar.get_width() / 2, count + 2, str(count),
                ha='center', va='bottom', fontsize=9, color='#333333')

ax.set_xlabel('Days from designation to first observed flag change', fontsize=10)
ax.set_ylabel('Vessels', fontsize=10)
ax.set_title('Time to first flag change after UK sanctions designation\n'
             f'n = {len(days)} vessels. 273 of 404 changed within 90 days.',
             fontsize=12, loc='left', pad=15)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')
ax.tick_params(labelsize=9, colors='#333333')
plt.xticks(rotation=45, ha='right')
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE', linewidth=0.8)

plt.tight_layout()
plt.savefig('days_to_flag_change.png', dpi=150, bbox_inches='tight')

print(f"Saved days_to_flag_change.png")
print(f"Total vessels: {len(days)}")
for label, count in zip(labels, buckets):
    print(f"  {label:>8}: {count}")