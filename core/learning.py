from dataclasses import dataclass, field

import pandas as pd
from sklearn.linear_model import LinearRegression


@dataclass
class DataCurve:
    data: pd.Series
    curve: LinearRegression

    @property
    def start(self):
        return self.data[0]

    @property
    def end(self):
        return self.data[-1]


@dataclass
class LearningStats:
    alpha: float
    beta: float
    alpha_percentage: float
    beta_percentage: float


def _get_learning_curve(data: pd.DataFrame) -> DataCurve:
    data = data.reset_index()
    x, y = data[['index']], data['value']
    lr = LinearRegression()
    lr.fit(x, y)
    return DataCurve(
        data=lr.predict(x),
        curve=lr,
    )


def _get_annotations_data(test_group: pd.DataFrame, n: int = 50):
    data = []
    for user, group in test_group.groupby('user__id'):

        if len(group) < n:
            continue

        values = group.sort_values('data__item_id')['annotation_eval'].to_numpy()[:n]
        data.extend([
            {
                "index": i,
                "value": value
            }
            for i, value in enumerate(values)
        ])

    _df = pd.DataFrame(data)
    return _df.groupby('index')['value'] \
        .mean() \
        .to_frame("value")


@dataclass
class LearningAnalyser:
    df: pd.DataFrame
    n: int = 50
    window_size: int = 5
    _test_data: pd.DataFrame = field(init=False)
    _control_data: pd.DataFrame = field(init=False)
    _change_data: pd.DataFrame = field(init=False)
    _test_curve: DataCurve = field(init=False, default=None)
    _control_curve: DataCurve = field(init=False, default=None)
    _change_curve: DataCurve = field(init=False, default=None)

    def __post_init__(self):
        test_group = self.df.query('user__feedback')
        control_group = self.df.query('not user__feedback')

        self._test_data = self._preprocess_data(test_group)
        self._control_data = self._preprocess_data(control_group)
        self._change_data = self._get_change_data()

    def _preprocess_data(self, data):
        annotation_data = _get_annotations_data(data, self.n)
        return annotation_data.rolling(self.window_size).mean().fillna(0)[self.window_size-1:]

    def _get_change_data(self):
        _df = (self._test_data - self._control_data).sort_index()
        _df_change = _df['value'].dropna()
        return _df_change.to_frame('value').reset_index(drop=True)

    @property
    def change_data(self):
        return self._change_data

    @property
    def test_curve(self) -> DataCurve:
        if not self._test_curve:
            self._test_curve = _get_learning_curve(self._test_data)
        return self._test_curve

    @property
    def control_curve(self) -> DataCurve:
        if not self._control_curve:
            self._control_curve = _get_learning_curve(self._control_data)
        return self._control_curve

    @property
    def change_curve(self) -> DataCurve:
        if not self._change_curve:
            self._change_curve = _get_learning_curve(self._change_data)
        return self._change_curve

    @property
    def stats(self) -> LearningStats:
        change_start, change_end = self.change_curve.start, self.change_curve.end
        control_start = self.control_curve.start

        return LearningStats(
            alpha=self.change_curve.curve.coef_[0],
            beta=self.change_curve.curve.intercept_,
            alpha_percentage=(change_end - change_start) / control_start,
            beta_percentage=change_start / control_start
        )
