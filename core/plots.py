import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties
from strapping import stats

from .consts import GROUPS_ORDER, GROUPS_NAME
from .dataset import DatasetAnalyser
from .learning import LearningAnalyser


def plot_histogram(dataset: DatasetAnalyser, metric_index: int):
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    all_data = np.vstack([
        group.diffs_percentage
        for group in dataset.groups.values()
    ])[:, metric_index]
    bins = np.histogram(all_data, bins=20)[1]

    for (group_name, group) in dataset.groups.items():
        index = len(GROUPS_ORDER) - group.order - 1

        diffs = pd.Series(group.diffs_percentage[:, metric_index])
        diffs.plot.hist(ax=axes[index],
                        title=f"$W_{group.order+1}$ - {GROUPS_NAME[group_name]}",
                        bins=bins,
                        density=True)
        axes[index].set_ylabel("")
        axes[index].set_xlabel("Różnica jakości w stosunku do grupy kontrolnej [%]")

        ci = stats.confidence_intervals(diffs.to_numpy())
        axes[index].axvline(x=ci[0], color='k', linestyle='--', alpha=0.8)
        axes[index].axvline(x=ci[1], color='k', linestyle='-', alpha=0.8)
        axes[index].axvline(x=ci[2], color='k', linestyle='--', alpha=0.8)

        vals = axes[index].get_xticks()
        axes[index].set_xticklabels(['{:,.2%}'.format(x) for x in vals])

    fig.text(0.08, 0.5, 'Częstość [%]', va='center', rotation='vertical')

    artist = plt.Line2D((0, 1), (0, 0), color='k', linestyle='--')
    any_artist = plt.Line2D((0,1),(0,0), color='k')

    plt.legend(
        [artist, any_artist],
        ['Percentyle (P05 i P95)', 'Średnia'],
        bbox_to_anchor=(0.27, 3.35)
    )


def plot_learning_curve(learning: LearningAnalyser, report: pd.DataFrame):
    _, axes = plt.subplots(1, 2, figsize=(15, 5), gridspec_kw={'width_ratios': [4, 1]})
    axes[0].set_xlabel("Indeks anotacji")
    axes[0].set_ylabel("Różnica jakości w czasie [%]")

    axes[0].plot(learning.change_data, 'bo', label="$R$ - różnicy jakości")
    axes[0].plot(learning.change_curve.data, label="$\hat{R}$ - aproksymacja liniowa $R$")
    axes[0].legend()

    axes[1].set_axis_off()
    table = axes[1].table(
        cellText=report.values,
        colLabels=report.columns,
        loc='center',
        cellLoc='center',
        colWidths=[0.4, 0.4]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(16)
    table.scale(1.5, 3)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))
