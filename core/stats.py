import time
from dataclasses import dataclass

import pandas as pd


@dataclass
class Statistics:
    df: pd.DataFrame

    @property
    def general(self) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "metric": "total_annotations",
                "value": len(self.df)
            },
            {
                "metric": "unique_items",
                "value": len(set(self.df['data__item_id'].values))
            },
            {
                "metric": "unique_users",
                "value": len(set(self.df['user__id'].values))
            },
            {
                "metric": "total_annotation_time",
                "value": time.strftime('%Hh %Mm %Ss', time.gmtime(self.df['annotation__time'].sum()))
            },
        ]).set_index("metric")

    @property
    def annotations_per_item(self) -> pd.DataFrame:
        return pd.DataFrame(self.df['data__item_id'].value_counts().describe())

    @property
    def annotations_per_user(self) -> pd.DataFrame:
        return pd.DataFrame(self.df['user__id'].value_counts().describe())

    @property
    def average_time_per_annotation(self, N=100) -> pd.DataFrame:
        data = []
        for feedback, group in self.df.groupby('user__id'):
            values = group.sort_values('data__item_id')['annotation__time'].to_numpy()[:N]
            data.extend(
                {"index": idx, "value": value}
                for idx, value in enumerate(values)
                if idx % 50 != 0
            )
        df_times = pd.DataFrame(data)
        df_times = df_times.groupby('index')['value'].mean().to_frame('value')
        return df_times
