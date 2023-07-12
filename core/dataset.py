from dataclasses import dataclass, field
from typing import Dict, Text, List, Optional, Tuple
from strapping import bootstrap, stats
import numpy as np
import pandas as pd

from .consts import GROUPS_ORDER


@dataclass
class DatasetStats:
    test: np.ndarray
    control: np.ndarray
    diffs: np.ndarray

    @property
    def percentage_ci(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        return stats.percentage_confidence_intervals(self.diffs, self.control.mean(axis=0))

    @property
    def ci(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        return stats.confidence_intervals(self.diffs)

    @property
    def p_value(self) -> np.ndarray:
        return (self.diffs > 0).mean(axis=0)

    @property
    def cohen_d(self) -> np.ndarray:
        return self.diffs.mean(axis=0) / stats.pooled_std(self.test, self.control) 


@dataclass
class DatasetGroup:
    name: Text
    test: np.ndarray
    control: np.ndarray
    _diffs: Optional[np.ndarray] = field(default=None, init=False)
    _stats: Optional[DatasetStats] = field(default=None, init=False)
    bootstrap_diffs: bool = field(default=True)

    @property
    def order(self):
        return GROUPS_ORDER.get(self.name)

    def __post_init__(self):
        self._update_stats()

    def update_diffs(self, agg_func=np.mean, iterations: int = 100):
        if self.bootstrap_diffs:
            self._diffs = bootstrap.sample_diffs(self.test, self.control, iterations, agg_func)
        else:
            self._diffs = self.test - self.control
        self._update_stats()

    def _update_stats(self):
        self._stats = DatasetStats(self.test, self.control, self.diffs)

    @property
    def short_name(self):
        return self.name.split()[0]

    @property
    def diffs(self):
        if self._diffs is None:
            self.update_diffs()
        return self._diffs
    
    @property
    def diffs_percentage(self):
        return self.diffs / self.control.mean(axis=0)

    @property
    def stats(self) -> DatasetStats:
        return self._stats


@dataclass
class DatasetAnalyser:
    dataset: pd.DataFrame
    metrics: List[Text]
    _groups: Dict[Text, DatasetGroup] = field(default_factory=dict)

    def __post_init__(self):
        for group_name, group in self.dataset.groupby('test_group'):
            test_group = group.query("user__feedback == True")[self.metrics]
            control_group = group.query("user__feedback == False")[self.metrics]
            self._groups[group_name] = DatasetGroup(
                group_name, test_group.to_numpy(), control_group.to_numpy())

    @property
    def groups(self):
        return self._groups
