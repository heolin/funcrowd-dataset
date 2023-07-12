from typing import Callable, Dict
from typing import List, Text, Tuple

import pandas as pd

from .learning import LearningAnalyser
from .utils import format_number
from .dataset import DatasetGroup, DatasetAnalyser


def _generate_group_report(group: DatasetGroup, metrics: List[Text]):
    stats = group.stats
    # ci
    _df_ci = pd.DataFrame(stats.ci, columns=metrics)
    _df_ci['quantile'] = ["0.05", "0.5", "0.95"]
    _df_ci['group_name'] = group.name
    
    # percentage ci
    _df_percentage_ci = pd.DataFrame(stats.percentage_ci, columns=metrics)
    _df_percentage_ci['quantile'] = ["0.05", "0.5", "0.95"]
    _df_percentage_ci['group_name'] = group.name

    # p_value
    _df_p_value = pd.DataFrame([stats.p_value], columns=metrics)
    _df_p_value['group_name'] = group.name

    # cohen d
    _df_cohen_d = pd.DataFrame([stats.cohen_d], columns=metrics)
    _df_cohen_d['group_name'] = group.name
    return _df_ci, _df_percentage_ci, _df_p_value, _df_cohen_d


def generate_comparison_report(dataset: DatasetAnalyser) \
        -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df_ci = pd.DataFrame()
    df_percentage_ci = pd.DataFrame()
    df_p_value = pd.DataFrame()
    df_cohen_d = pd.DataFrame()

    for group_name, group in dataset.groups.items():
        _df_ci, _df_percentage_ci, _df_p_value, _df_cohen_d = _generate_group_report(group, dataset.metrics)
        df_ci = pd.concat([df_ci, _df_ci])
        df_percentage_ci = pd.concat([df_percentage_ci, _df_percentage_ci])
        df_p_value = pd.concat([df_p_value, _df_p_value])
        df_cohen_d = pd.concat([df_cohen_d, _df_cohen_d])

    df_ci = df_ci.set_index(['group_name', 'quantile'])
    df_percentage_ci = df_percentage_ci.set_index(['group_name', 'quantile'])
    return df_ci, df_percentage_ci, df_p_value, df_cohen_d


def generate_test_groups_comparison_report(dataset: DatasetAnalyser):
    df_ci = pd.DataFrame()
    df_p_value = pd.DataFrame()
    df_cohen_d = pd.DataFrame()

    groups = list(dataset.groups.values())
    for index1 in range(len(groups)):
        for index2 in range(index1):
            group1, group2 = groups[index1], groups[index2]
            if group1.order < group2.order:
                group1, group2 = group2, group1

            if group1.name == group2.name:
                continue

            group = DatasetGroup(
                f"{group1.short_name}_{group2.short_name}",
                group1.diffs_percentage, group2.diffs_percentage,
                bootstrap_diffs=False
            )

            _df_ci, _, _df_p_value, _df_cohen_d = _generate_group_report(group, dataset.metrics)
            df_ci = pd.concat([df_ci, _df_ci])
            df_p_value = pd.concat([df_p_value, _df_p_value])
            df_cohen_d = pd.concat([df_cohen_d, _df_cohen_d])

    df_ci = df_ci.set_index(['group_name', 'quantile'])
    return df_ci, df_p_value, df_cohen_d


def compute_user_error(df: pd.DataFrame,
                       metrics_func: Callable[[pd.Series, pd.Series], Dict]) -> pd.DataFrame:
    data = []
    for (test_group, user_feedback, user_id), group in df.groupby(['test_group', 'user__feedback', 'user__id']):
        y_true = group['reference__output']
        y_pred = group['annotation__output']

        data.append({
            **{
                'test_group': test_group,
                'user__feedback': user_feedback,
                'user__id': user_id,
                'count': len(group),
                'annotation_time': group['annotation__time'].mean()
            },
            **metrics_func(y_true, y_pred)
        })

    return pd.DataFrame(data)


def generate_learning_report(learning: LearningAnalyser) -> pd.DataFrame:
    _stats = learning.stats
    _learning_metrics = [
        [r"\alpha", round(_stats.alpha, 3)],
        [r"\beta", round(_stats.beta, 3)],
        [r"\alpha_r", format_number(_stats.alpha_percentage, False)],
        [r"\beta_r", format_number(_stats.beta_percentage, False)],
    ]
    _df = pd.DataFrame(_learning_metrics, columns=['Metryka', "Wartość"])
    _df['Metryka'] = _df['Metryka'].apply(lambda x: f"${x}$")
    return _df
