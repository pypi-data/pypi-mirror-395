# aECG (Python parser for annotated ECG HL7 files)

Python library to parse and visualize [aECG files](https://en.wikipedia.org/wiki/HL7_aECG).

<img src="res/aecg.png" width="900">

## Demo
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://annotated-ecg.streamlit.app/)

## Installation
```
pip install aecg
```

## Usage
- Read your aECG xml file.
```python
import aecg

file_path = r"tests/data/Example aECG.xml"
aecg_o = aecg.read(file_path)
```

- Use `summary` to get an overview of the data. 
```python
aecg_o.summary()
```
```python
{
    'id': UUID('61d1a24f-b47e-41aa-ae95-f8ac302f4eeb'),
    'date': datetime.datetime(2002, 11, 22, 9, 10),
    'series_count': 1,
    'annotations_count': 167,
}
```

- Get waveforms dataframes and their associated plots.
```python
titles = []
dfs = []
figs = []

for serie in aecg_o.series:
    for i, seq_set in enumerate(serie.sequence_sets, 1):
        title = f"Serie {serie.id} | Sequence set {i}"
        df = seq_set.get_sequences_df()
        fig = aecg.plotter.plot_seq_set(df, title=title)
        dfs.append(df)
        titles.append(title)
        figs.append(fig)

    for i, seq_set in enumerate(serie.derived_sequence_sets, 1):
        title = f"Serie {serie.id} | Derived sequence set {i}"
        df = seq_set.get_sequences_df()
        fig = aecg.plotter.plot_seq_set(df, title=title)
        dfs.append(df)
        titles.append(title)
        figs.append(fig)
```

```python
dfs[0]
```
<img src="res/df_1.png">

```python
figs[0].show()
```

<img src="res/seq_plot_1.png">

- You can choose to plot all the curves together.

```python
aecg.plotter.plot_seq_set(dfs[0], plot_mode="one")
```

<img src="res/seq_plot_1_mode_one.png">