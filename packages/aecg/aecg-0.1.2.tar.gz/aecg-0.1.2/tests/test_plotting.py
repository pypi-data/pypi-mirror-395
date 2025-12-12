import pandas as pd
from plotly import graph_objects as go

import aecg
import aecg.parser
import aecg.plotter


def test_plotter_plot_seq_set():
    file_path = r"tests/data/Example aECG.xml"
    aecg_o = aecg.parser.read(file_path)

    seq = aecg_o.series[0].sequence_sets[0].get_sequences_df()
    df = pd.DataFrame(seq)

    figs = []
    for tm in ["relative", "absolute"]:
        for pm in ["one", "multiple"]:
            fig = aecg.plotter.plot_seq_set(df, time_mode=tm, plot_mode=pm)
            figs.append(fig)

    for f in figs:
        assert isinstance(f, go.Figure)
