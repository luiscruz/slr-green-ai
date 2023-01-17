import csv
from collections import Counter
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = ["Linux Libertine O", "serif"]
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.major.size'] = 4
plt.rcParams['xtick.major.width'] = 0.5
plt.rcParams['ytick.major.size'] = 4
plt.rcParams['ytick.major.width'] = 0.5
plt.rcParams['figure.constrained_layout.use'] = True

FIG_SIZE = (5,2.5)
LABEL_PAD=8

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

TOPIC_DICTIONARY = {
    "precision-energy-tradeoff": "Precision-Energy Trade-off",
    "model-comparison": "Model Benchmarking",
    "network-architecture": "network architecture"
}

TOPIC_IGNORE = [
    "tool",
    "model-simplification",
]

TYPE_OF_DATA_DICTIONARY = {
    "-": "Not specified",
    "number": "numeric",
    "NLP": "textual",
    "text": "textual",
}

VALIDATION_TYPE_DICTIONARY = {
    "field experiment": "Field\nExperiment",
    "simulation": "computer simulation",
    "laboratory": "Laboratory\nExperiment",
    "judgement": "Judgement\nStudy"
}

def _flatten(l):
    return list(item for sublist in l for item in sublist)


data = []
with open('data/Selection and Extraction sheet (SLR Green AI).xlsx - Data extraction CLEAN.csv') as csv_file:
    reader = csv.DictReader(csv_file, delimiter=',')
    for row in reader:
        row["topic_set"] = set(TOPIC_DICTIONARY.get(topic, topic)
                                              for value in row["Topic"].split(",")
                                              if (topic:=value.strip()) not in TOPIC_IGNORE)
        row["domain_set"] = set(topic.strip() for topic in row["Domain"].split(","))
        row["artifact_set"] = set(ARTIFACT_DICTIONARY.get(value.strip(),value.strip()) for value in row["Artifact considered"].split(","))
        row["type_of_data_set"] = set(TYPE_OF_DATA_DICTIONARY.get(value.strip(), value.strip())
                                      for value in row["Type of data"].split(","))
        row["validation_type_set"] = set(VALIDATION_TYPE_DICTIONARY.get(value.strip(),value.strip()) for value in row["Validation type"].split(","))
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
    


##### BAR Plots - Study type
def _get_counts_by_row(data, column):
    counts = Counter(row[column] for row in data).most_common()
    labels, yy = zip(*counts)
    return labels, yy

labels, yy = _get_counts_by_row(data, "Study type")
labels = list(map(str.title, labels))
xx = range(len(labels))
fig, ax = plt.subplots(figsize=(4,2))
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5, zorder=2)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Study type",  loc='center', labelpad=LABEL_PAD, fontsize=12)
# ax.tick_params(axis='both', which='major', labelsize=6)
# ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")
ax.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.5)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.savefig("results/barplot_study_type.eps")


##### BAR Plots  - Year
labels, yy = labels, yy = _get_counts_by_row(data, "Year")
labels, yy = zip(*sorted(zip(labels, yy)))
labels = list(map(str.title, labels))
xx = range(len(labels))
fig, ax = plt.subplots(figsize=FIG_SIZE)
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5, zorder=2)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Year",  loc='center', labelpad=LABEL_PAD, fontsize=12)
# ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.5)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# ax.spines['bottom'].set(linewidth=0.5)

fig.tight_layout()
fig.savefig("results/barplot_year.eps")

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

fig, ax = plt.subplots(figsize=FIG_SIZE)
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5, zorder=2)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Domain",  loc='center', labelpad=LABEL_PAD, fontsize=12)
# ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.5)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.savefig("results/barplot_domain.eps")

### HORIZONTAL ####
fig, ax = plt.subplots(figsize=(6, 3.5))

bar = ax.barh(y = list(reversed(xx)), width=yy, tick_label=labels,
       color="lightgray", height=0.35,
       edgecolor="black", linewidth=0.5)
ax.bar_label(bar,
             label_type='edge', padding=3)
ax.set_xlabel("No. papers",  loc='center', labelpad=LABEL_PAD, fontsize=12)
ax.set_ylabel("Domain",  loc='top', rotation="horizontal")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.5)
       
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


fig.tight_layout()
fig.savefig("results/barplot_domain_horizontal.eps")


##### BAR Plots  - Studied Artifact

others = ['architecture', 'hardware', 'deep Learning', 'CPU', 'framework', '-']
labels, yy = labels, yy = _get_counts_by_row_multiple(data, "artifact_set", others=others)
labels = list(map(str.title, labels))
xx = range(len(labels))

fig, ax = plt.subplots(figsize=FIG_SIZE)
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5, zorder=2)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Artifact",  loc='center', labelpad=LABEL_PAD, fontsize=12)
# ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.5)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.savefig("results/barplot_artifact.eps")

#type of study vs paper topic
others = ['user values', 'scheduling', 'rebound effects', 'security', 'energy capping']
topics_sorted = [item[0] for item in topics.most_common() if item[0] not in others]
topics_sorted.append("Other")
with open('results/bubbleplot.csv', 'w') as f:
    print("study-type,"+",".join(topics_sorted), file=f)
    for paper_type in paper_types.keys():
        papers = [paper for paper in data if paper["Study type"] == paper_type]
        # print (papers)
        subtopics = Counter()
        subtopics.update({x:0 for x in topics_sorted}) #set initial data
        for paper in papers:
            if paper["topic_set"].intersection(set(others)):
                print("-------")
                print(paper)
                subtopics.update({"Other"})
            subtopics.update(paper["topic_set"])
        print(f"{paper_type}," + ",".join(str(subtopics[topic]) for topic in topics_sorted), file=f)


## Bubble Plot

bubble_data = []
with open('results/bubbleplot.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
            bubble_data.append(row)
print(bubble_data)

bubble_data_xlabels = [label.title() for label in bubble_data[0][1:]]
bubble_data_ylabels = [row[0].title() for row in bubble_data[1:]]
bubble_data_x = list(range(len(bubble_data_xlabels)))*len(bubble_data_ylabels)
bubble_data_y = [0]*len(bubble_data_xlabels)+[1]*len(bubble_data_xlabels)+[2]*len(bubble_data_xlabels)
bubble_data_s = list(int(item) for item in _flatten([row[1:] for row in bubble_data[1:]]))
bubble_data_s_scaled = list(item*85 for item in bubble_data_s)
print(bubble_data_x)
print(bubble_data_y)
print(bubble_data_s)

# fig, ax = plt.subplots(figsize=(10, 2))
# ax.scatter(
#     x=bubble_data_x,
#     y=bubble_data_y,
#     s=bubble_data_s_scaled,
#     facecolors='white',
#     edgecolors='k',
#     linewidth=0.5
# )
# ax.set_xticks(range(len(bubble_data_xlabels)))
# ax.set_xticklabels(bubble_data_xlabels, rotation=10)
# ax.set_yticks(range(len(bubble_data_ylabels)))
# ax.set_yticklabels(bubble_data_ylabels)
# ax.set_ylim((-1,3))
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
#
#
# for i, value in enumerate(bubble_data_s):
#     if value > 0:
#         ax.annotate(value, (bubble_data_x[i], bubble_data_y[i]),
#                     ha="center", va="center",
#                     fontsize=8)
# fig.tight_layout()
# fig.savefig("results/bubbleplot.eps")

fig, ax = plt.subplots(figsize=(5, 7))
ax.scatter(
    y=bubble_data_x,
    x=bubble_data_y,
    s=bubble_data_s_scaled,
    facecolors='None',
    edgecolors='k',
    linewidth=0.5
)
ax.set_yticks(range(len(bubble_data_xlabels)))
ax.set_yticklabels(bubble_data_xlabels)
ax.set_xticks(range(len(bubble_data_ylabels)))
ax.set_xticklabels(bubble_data_ylabels)
ax.set_xlim((-1,3))
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)

for i, value in enumerate(bubble_data_s):
    if value > 0:
        ax.annotate(value, (bubble_data_y[i], bubble_data_x[i]),
                    ha="center", va="center",
                    fontsize=8)

fig.tight_layout()
fig.savefig("results/bubbleplot-horizontal.eps")

### BAR plot – Topic

others = ['user values', 'scheduling', 'rebound effects', 'security', 'energy capping']
labels, yy = labels, yy = _get_counts_by_row_multiple(data, "topic_set", others=others)
labels = list(map(str.title, labels))
# labels = list(map(lambda x: x.replace(' ','\n'), labels))
xx = range(len(labels))

fig, ax = plt.subplots(figsize=(7.5, 3))
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5, zorder=2)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Topic",  loc='center', fontsize=12)
# ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")
ax.tick_params(axis='x', labelrotation = 40, labelsize=9, pad=0)
for tick in ax.xaxis.get_majorticklabels():
    tick.set_horizontalalignment("right")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.5)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.savefig("results/barplot_topic.eps")

### BAR plot – Considered phase

labels, yy = labels, yy = _get_counts_by_row(data, "Considered phase")
labels = list(map(str.title, labels))
# labels = list(map(lambda x: x.replace(' ','\n'), labels))
xx = range(len(labels))

fig, ax = plt.subplots(figsize=(4,2))
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5, zorder=2)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Considered stage",  loc='center', labelpad=LABEL_PAD, fontsize=12)
# ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")

ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.5)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.savefig("results/barplot_phase.eps")


### BAR plot – type of data

others = ["Not specified"]
labels, yy = labels, yy = _get_counts_by_row_multiple(data, "type_of_data_set", others=others)
labels[-1] = "Not\nSpecified"
labels = list(map(str.title, labels))
# labels = list(map(lambda x: x.replace(' ','\n'), labels))
xx = range(len(labels))

fig, ax = plt.subplots(figsize=FIG_SIZE)
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5, zorder=2)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Data Type",  loc='center', labelpad=LABEL_PAD, fontsize=12)
# ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")
ax.tick_params(axis='x', labelrotation = 0, labelsize=9)
# for tick in ax.xaxis.get_majorticklabels():
    # tick.set_horizontalalignment("right")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.5)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.savefig("results/barplot_type_of_data.eps")

### BAR plot – research strategy
others = ["none"]
labels, yy = labels, yy = _get_counts_by_row_multiple(data, "validation_type_set", others=others)
labels[-1] = "None"
labels = [VALIDATION_TYPE_DICTIONARY.get(label, label).title() for label in labels]

xx = range(len(labels))

fig, ax = plt.subplots(figsize=FIG_SIZE)
bar = ax.bar(xx, yy, tick_label=labels,
       color="lightgray", width=0.35,
       edgecolor="black", linewidth=0.5, zorder=2)
ax.bar_label(bar, label_type='edge')
ax.set_xlabel("Research Strategy",  loc='center', labelpad=LABEL_PAD, fontsize=12)
# ax.set_ylabel("No. papers",  loc='top', rotation="horizontal")
ax.tick_params(axis='x', labelrotation = 0, labelsize=9)
# for tick in ax.xaxis.get_majorticklabels():
    # tick.set_horizontalalignment("right")

# ax.set_xlim((-0.4, 2.7))
ax.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.5)
       
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.savefig("results/barplot_research_strategy.eps")



