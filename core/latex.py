from dataclasses import dataclass
from typing import Text, Tuple

import pandas as pd

from .utils import format_number


def get_metric_row(
        group_name: Text,  # noqa
        metric: Text,
        df_percentage_ci: pd.DataFrame,
        df_p_value: pd.DataFrame,
        df_cohen_d: pd.DataFrame
) -> Tuple[float, float, float, float, float]:
    ci = df_percentage_ci.reset_index().query('group_name == @group_name')
    return (
        ci.iloc[0][metric],
        ci.iloc[1][metric],
        ci.iloc[2][metric],
        df_p_value.query('group_name == @group_name')[metric][0],
        df_cohen_d.query('group_name == @group_name')[metric][0],
    )


def get_latex_row(label, group_name, metric, df_percentage_ci, df_p_value, df_cohen_d):
    p05, mu, p95, p, delta = get_metric_row(group_name, metric, df_percentage_ci, df_p_value, df_cohen_d)
    return r'\multicolumn{1}{c|}{' + label + r'} & ' + \
           r'\multicolumn{1}{c|}{' + format_number(p05) + r'} & ' + \
           r'\multicolumn{1}{c|}{' + format_number(mu) + r'} & ' + \
           r'\multicolumn{1}{c|}{' + format_number(p95) + r'} & ' + \
           r'\multicolumn{1}{c|}{' + str(round(p, 4)) + r'} & ' + \
           str(round(delta, 2)) + r' \\ \hline'


@dataclass
class ResultTables:
    ci: pd.DataFrame
    p_value: pd.DataFrame
    cohen_d: pd.DataFrame


@dataclass
class LatexTablesGenerator:
    h1: ResultTables
    h2: ResultTables

    def get_results_table(self, metric: Text) -> Text:
        return r"""
\begin{table}[H]
\centering
\caption{}
\label{tab:my-table}
\begin{tabular}{cccccc}
\rowcolor[HTML]{EFEFEF} 
\multicolumn{1}{c|}{\cellcolor[HTML]{EFEFEF}\textbf{Warunek}} &
  \multicolumn{1}{c|}{\cellcolor[HTML]{EFEFEF}\boldmath$P_{05}$} &
  \multicolumn{1}{c|}{\cellcolor[HTML]{EFEFEF}\boldmath$\mu$} &
  \multicolumn{1}{c|}{\cellcolor[HTML]{EFEFEF}\boldmath$P_{95}$} &
  \multicolumn{1}{c|}{\cellcolor[HTML]{EFEFEF}\boldmath$p$} &
  \boldmath$d$ \\ \hline
\rowcolor[HTML]{EFEFEF} 
\multicolumn{6}{c}{\cellcolor[HTML]{EFEFEF}Hipoteza $H_1$ -- zmiana w metryce XXXX}                                                                                                        \\ \hline
        """ + \
               get_latex_row(r'$W_1$', "high quality feedback", metric, self.h1.ci, self.h1.p_value, self.h1.cohen_d) + \
               get_latex_row(r'$W_2$', "medium quality feedback", metric, self.h1.ci, self.h1.p_value,
                             self.h1.cohen_d) + \
               get_latex_row(r'$W_3$', "low quality feedback", metric, self.h1.ci, self.h1.p_value, self.h1.cohen_d) + \
               r"""
\rowcolor[HTML]{EFEFEF} 
\multicolumn{6}{c}{\cellcolor[HTML]{EFEFEF}Hipoteza $H_2$ -- zmiana w metryce XXXX}                                                                                                        \\ \hline
        """ + \
               get_latex_row(r'$W_1 - W_3$', "high_low", metric, self.h2.ci, self.h2.p_value, self.h2.cohen_d) + \
               get_latex_row(r'$W_1 - W_2$ ', "high_medium", metric, self.h2.ci, self.h2.p_value, self.h2.cohen_d) + \
               get_latex_row(r'$W_2 - W_3$', "medium_low", metric, self.h2.ci, self.h2.p_value, self.h2.cohen_d) + \
               r"""
\rowcolor[HTML]{EFEFEF} 
\multicolumn{6}{c}{\cellcolor[HTML]{EFEFEF}Pytanie $P_2$ -- zmiana w szybkości pracy anotatorów}                                                                                                        \\ \hline
        """ + \
               get_latex_row(r'$W_1$', "high quality feedback", "annotation_time", self.h1.ci, self.h1.p_value,
                             self.h1.cohen_d) + \
               get_latex_row(r'$W_2$', "medium quality feedback", "annotation_time", self.h1.ci, self.h1.p_value,
                             self.h1.cohen_d) + \
               get_latex_row(r'$W_3$', "low quality feedback", "annotation_time", self.h1.ci, self.h1.p_value,
                             self.h1.cohen_d) + \
               r"""
\rowcolor[HTML]{EFEFEF} 
\multicolumn{6}{c}{\cellcolor[HTML]{EFEFEF}Pytanie $P_3$ -- zmiana w liczbie wykonanych anotacji}                                                                                                        \\ \hline
        """ + \
               get_latex_row(r'$W_1$', "high quality feedback", "count", self.h1.ci, self.h1.p_value,
                             self.h1.cohen_d) + \
               get_latex_row(r'$W_2$', "medium quality feedback", "count", self.h1.ci, self.h1.p_value,
                             self.h1.cohen_d) + \
               get_latex_row(r'$W_3$', "low quality feedback", "count", self.h1.ci, self.h1.p_value,
                             self.h1.cohen_d) + \
               r"""
\end{tabular}
\end{table}
        """


def create_latex_tables_generator(
        df_percentage_ci_h1: pd.DataFrame,
        df_p_value_h1: pd.DataFrame,
        df_cohen_d_h1: pd.DataFrame,
        df_ci_h2: pd.DataFrame,
        df_p_value_h2: pd.DataFrame,
        df_cohen_d_h2: pd.DataFrame
) -> LatexTablesGenerator:
    return LatexTablesGenerator(
        h1=ResultTables(
            df_percentage_ci_h1,
            df_p_value_h1,
            df_cohen_d_h1
        ),
        h2=ResultTables(
            df_ci_h2,
            df_p_value_h2,
            df_cohen_d_h2
        )
    )
