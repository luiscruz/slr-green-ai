import csv
from collections import Counter
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.major.size'] = 4
plt.rcParams['xtick.major.width'] = 0.5
plt.rcParams['ytick.major.size'] = 4
plt.rcParams['ytick.major.width'] = 0.5

ARTIFACT_DICTIONARY = {
    "algorithm - deep neural network": "Algorithm",
    'algorithm - general': "Algorithm",
    'algorithm - convolutional neural network': "Algorithm",
    'algorithm': "Algorithm",
    'algorithm - decision Tree': "Algorithm",
    'algorithm - neural network': "Algorithm",
    'algorithm - federated learning': "Algorithm",
    'algorithm - deep learning': "Algorithm",
    'algorithm - deep learning model': "Algorithm",
    'algorithm - deep neural network': "Algorithm",
    'algorithm - spiking neural network': "Algorithm",
    'algorithm - decision tree': "Algorithm",
    'algorithm - logistic regression model': "Algorithm",
    'algorithm - genetic algorithm': "Algorithm",
    'algorithm - stochastic gradient descent': "Algorithm",
    'algorithm - transformer': "Algorithm",
    'deep learning': "Algorithm",
    'all': "general",
}

data = []
with open('data/Selection and Extraction sheet (SLR Green AI).xlsx - Data extraction CLEAN.csv') as csv_file:
    reader = csv.DictReader(csv_file, delimiter=',')
    for row in reader:
        row["topic_set"] = set(topic.strip() for topic in row["Topic"].split(","))
        row["domain_set"] = set(topic.strip() for topic in row["Domain"].split(","))
        row["artifact_set"] = set(ARTIFACT_DICTIONARY.get(topic.strip(),topic.strip()) for topic in row["Artifact considered"].split(","))
        data.append(row)


# get unique topics
topics = Counter()
for paper in data:
    topics.update(paper["topic_set"])
print(topics)

for topic, count in topics.most_common():
    print(f"{topic}, {count}")

## get all papers addressing the top 4 topics
top_topics = {
    "monitoring",
    "hyperparameter-tuning",
    "deployment",
    "model-comparison"
}
top_topic_papers = []
for row in data:
    if row["topic_set"].intersection(top_topics):
        top_topic_papers.append(row)

print(f"There are {len(top_topic_papers)} papers out of {len(data)} that work on the top 4 topics.")

# get type of paper
paper_types = Counter(paper["Study type"].split(",")[0].strip() for paper in data)
print(paper_types)

for paper_type, count in paper_types.most_common():
    print(f"{paper_type}, {count}")
    
#type of study vs paper topic
topics_sorted = [item[0] for item in topics.most_common()]
with open('results/bubbleplot.csv', 'w') as f:
    print("study-type,"+",".join(topics_sorted), file=f)
    for paper_type in paper_types.keys():
        papers = [paper for paper in data if paper["Study type"] == paper_type]
        # print (papers)
        subtopics = Counter()
        subtopics.update({x:0 for x in topics_sorted})
        for paper in papers:
            subtopics.update(paper["topic_set"])
        print(f"{paper_type}," + ",".join(str(subtopics[topic]) for topic in topics_sorted), file=f)


## Bubble Plot

bubble_data = []
with open('bubbleplot.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
            bubble_data.append(row)
print(bubble_data)

def _flatten(l):
    return list(item for sublist in l for item in sublist)

bubble_data_xlabels = [label.title() for label in bubble_data[0][1:]]
bubble_data_ylabels = [row[0].title() for row in bubble_data[1:]]
bubble_data_x = list(range(len(bubble_data_xlabels)))*len(bubble_data_ylabels)
bubble_data_y = [0]*len(bubble_data_xlabels)+[1]*len(bubble_data_xlabels)+[2]*len(bubble_data_xlabels)
bubble_data_s = list(int(item) for item in _flatten([row[1:] for row in bubble_data[1:]]))
bubble_data_s_scaled = list(item*90 for item in bubble_data_s)
print(bubble_data_x)
print(bubble_data_y)
print(bubble_data_s)
# import pdb; pdb.set_trace()
fig, ax = plt.subplots(figsize=(10, 2))
ax.scatter(
    x=bubble_data_x,
    y=bubble_data_y,
    s=bubble_data_s_scaled,
    facecolors='white',
    edgecolors='k',
    linewidth=0.5
)
ax.set_xticks(range(len(bubble_data_xlabels)))
ax.set_xticklabels(bubble_data_xlabels, rotation=10)
ax.set_yticks(range(len(bubble_data_ylabels)))
ax.set_yticklabels(bubble_data_ylabels)
ax.set_ylim((-1,3))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


for i, value in enumerate(bubble_data_s):
    if value > 0:
        ax.annotate(value, (bubble_data_x[i], bubble_data_y[i]),
                    ha="center", va="center",
                    fontsize=8)
fig.tight_layout()
fig.savefig("results/bubbleplot.pdf")

fig, ax = plt.subplots(figsize=(6, 8))
ax.scatter(
    y=bubble_data_x,
    x=bubble_data_y,
    s=bubble_data_s_scaled,
    facecolors='white',
    edgecolors='k',
    linewidth=0.5
)
ax.set_yticks(range(len(bubble_data_xlabels)))
ax.set_yticklabels(bubble_data_xlabels)
ax.set_xticks(range(len(bubble_data_ylabels)))
ax.set_xticklabels(bubble_data_ylabels)
ax.set_xlim((-1,3))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

for i, value in enumerate(bubble_data_s):
    if value > 0:
        ax.annotate(value, (bubble_data_y[i], bubble_data_x[i]),
                    ha="center", va="center",
                    fontsize=8)

fig.tight_layout()
fig.savefig("results/bubbleplot-horizontal.pdf")

##### BAR Plots - Study type
def _get_counts_by_row(data, column):
    counts = Counter(row[column] for row in data).most_common()
    labels, yy = zip(*counts)
    return labels, yy

labels, yy = _get_counts_by_row(data, "Study type")
labels = list(map(str.title, labels))
xx = range(len(labels))
fig, ax = plt.subplots(figsize=(6, 4))
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Study type",  loc='right')
ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")

ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='white', linestyle='--', linewidth=1, alpha=0.3)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.savefig("results/barplot_study_type.pdf")


##### BAR Plots  - Year
labels, yy = labels, yy = _get_counts_by_row(data, "Year")
labels, yy = zip(*sorted(zip(labels, yy)))
labels = list(map(str.title, labels))
xx = range(len(labels))
fig, ax = plt.subplots(figsize=(6, 4))
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Year",  loc='center')
ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='white', linestyle='--', linewidth=1, alpha=0.3)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# ax.spines['bottom'].set(linewidth=0.5)

fig.tight_layout()
fig.savefig("results/barplot_year.pdf")

##### BAR Plots  - Domain
def _get_counts_by_row_multiple(data, column, others=None):
    """Count frequency when one paper/row has multiple values."""
    column = _flatten(row[column] for row in data)
    if others:
        other_count = sum(1 for value in column if value in others)
        column = [value for value in column if value not in others]
    counts = Counter(column).most_common()
    labels, yy = zip(*counts)
    if others:
        labels = [*labels, "other"]
        yy = [*yy, other_count]
    return labels, yy

others = ['smart cities', 'human activity', 'wereables', 'embedded-systems', 'autonomous driving', 'NLP', 'health']
labels, yy = labels, yy = _get_counts_by_row_multiple(data, "domain_set", others=others)
labels = list(map(str.title, labels))
labels = list(map(lambda x: x.replace(' ','\n'), labels))
xx = range(len(labels))

fig, ax = plt.subplots(figsize=(6, 4))
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Domain",  loc='center')
ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='white', linestyle='--', linewidth=1, alpha=0.3)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.savefig("results/barplot_domain.pdf")

### HORIZONTAL ####
fig, ax = plt.subplots(figsize=(6, 3.5))

bar = ax.barh(y = list(reversed(xx)), width=yy, tick_label=labels,
       color="lightgray", height=0.35,
       edgecolor="black", linewidth=0.5)
ax.bar_label(bar,
             label_type='edge', padding=3)
ax.set_xlabel("No. papers",  loc='center')
ax.set_ylabel("Domain",  loc='top', rotation="horizontal")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="x", color='white', linestyle='--', linewidth=1, alpha=0.3)
       
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


fig.tight_layout()
fig.savefig("results/barplot_domain_horizontal.pdf")


##### BAR Plots  - Studied Artifact

others = ['architecture', 'hardware', 'deep Learning', 'CPU', 'framework', '-']
labels, yy = labels, yy = _get_counts_by_row_multiple(data, "artifact_set", others=others)
labels = list(map(str.title, labels))
xx = range(len(labels))
import pdb; pdb.set_trace()
fig, ax = plt.subplots(figsize=(6, 4))
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Artifact",  loc='center')
ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='white', linestyle='--', linewidth=1, alpha=0.3)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.savefig("results/barplot_artifact.pdf")

