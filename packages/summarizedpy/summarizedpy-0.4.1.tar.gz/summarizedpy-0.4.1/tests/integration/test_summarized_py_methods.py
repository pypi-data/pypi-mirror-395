#!/usr/bin/env python

"""Integration tests for SummarizedPy methods."""
import pytest
import numpy as np
import re
from depy.summarized_py import SummarizedPy

@pytest.mark.integration
@pytest.mark.parametrize("strategy", [
    "overall",
    "all_conditions",
    "any_condition"
])
def test_filter_missingness(load_data_sp, strategy):
    obj = load_data_sp
    obj.samples["condition"] = ["ADC"] * 6 + ["SCC"] * 6

    filtered = obj.filter_missingness(strategy=strategy, condition_column="condition")
    assert isinstance(filtered, SummarizedPy)
    assert filtered.data.shape[0] < obj.data.shape[0]

@pytest.mark.integration
def test_transform_features(load_data_sp):
    obj = load_data_sp

    log2_data = obj.transform_features(method="log", by=2).data
    assert np.any(np.isclose(obj.data, 2 ** log2_data))

    z_data = obj.transform_features(method="z-score", axis=0).data
    assert np.isclose(np.nanmean(z_data), 0)

    center_data = obj.transform_features(method="center", by="mean", axis=0).data
    assert np.isclose(np.nanmean(center_data), 0)

    vsn_data = obj.transform_features(method="vsn").data
    assert vsn_data.shape == obj.data.shape

@pytest.mark.integration
def test_impute_missing_values(load_data_sp):
    obj = load_data_sp
    data = obj.impute_missing_values(method="Hybrid").data
    assert not np.any(np.isnan(data))

@pytest.mark.integration
def test_filter_samples(load_data_sp):
    obj = load_data_sp
    obj = obj.filter_samples(expr="sample in ['Intensity.092.1']")
    assert obj.data.shape[1] == 1

@pytest.mark.integration
def test_filter_features(load_data_sp):
    obj = load_data_sp
    obj = obj.filter_features(expr="protein_id in ['REV__Q9H0I9']")
    assert obj.data.shape[0] == 1

@pytest.mark.integration
def test_filter_index_reset(load_data_sp):
    obj = load_data_sp
    obj_filter = obj.filter_missingness(strategy="overall")
    assert obj.features.index[-1] != obj_filter.features.index[-1]

@pytest.mark.integration
def test_multiple_filters(load_data_sp):
    obj = load_data_sp
    obj = obj.filter_missingness(strategy="overall")
    rev_hits = obj.features["protein_id"].apply(lambda x: bool(re.match("REV", x)))
    obj.features["rev"] = rev_hits
    obj_mask = obj.filter_features(mask=~rev_hits)
    obj_expr = obj.filter_features(expr="~rev")
    obj_expr_local = obj.filter_features(expr="~@rev_hits")
    assert obj_mask.features.shape == obj_expr.features.shape
    assert obj_mask.features.shape[0] < obj.features.shape[0]
    assert obj_expr.features.shape[0] == obj_expr_local.features.shape[0]

@pytest.mark.integration
def test_select_variable_features(load_data_sp, mocker):
    obj = load_data_sp
    mock_show = mocker.patch("matplotlib.pyplot.show")
    obj = obj.filter_missingness(strategy="overall")
    obj_hvf = obj.select_variable_features(top_n=100, plot=True)
    mock_show.assert_called_once()
    assert obj_hvf.data.shape[0] < obj.data.shape[0]

@pytest.mark.integration
def test_import_from_delim_file(tmp_path, test_df):
    test_df = test_df

    file_path = tmp_path / "test_import_from_delim_file.csv"
    test_df.to_csv(file_path, index=False)

    obj = SummarizedPy.import_from_delim_file(path=str(file_path), delim=",")

    assert isinstance(obj, SummarizedPy)
    assert obj.data.shape == (3, 3)
    assert "proteinID" in obj.features.columns

@pytest.mark.integration
def test_save_and_load_sp(tmp_path, toy_data_sp):
    path = tmp_path / "test_save_sp.pkl"
    path = str(path)
    toy_data_sp = toy_data_sp

    toy_data_sp.save_sp(path=path)
    loaded_sp = SummarizedPy.load_sp(path=path)

    assert isinstance(loaded_sp, SummarizedPy)
    assert np.array_equal(loaded_sp.data, toy_data_sp.data)
    assert loaded_sp.features.equals(loaded_sp.features)
    assert loaded_sp.samples.equals(loaded_sp.samples)

@pytest.mark.integration
def test_surrogate_variable_analysis(load_data_sp):
    obj = load_data_sp
    obj.samples["condition"] = ["ADC"] * 6 + ["SCC"] * 6
    obj = obj.filter_missingness(strategy="all_conditions", condition_column="condition")
    obj = obj.transform_features(method="log", by=2)
    obj = obj.surrogate_variable_analysis(mod="~condition")

    assert "sv_1" in obj.samples.columns

@pytest.mark.integration
def test_limma_trend_dea(load_data_sp):
    obj = load_data_sp
    obj.samples["condition"] = ["ADC"] * 6 + ["SCC"] * 6
    obj = obj.filter_missingness(strategy="all_conditions", condition_column="condition")
    obj = obj.limma_trend_dea(design_formula="~0+condition", contrasts={"Test": "SCC-ADC"}, array_weights=True)

    assert hasattr(obj, "results")

@pytest.mark.integration
def test_volcano_plot(load_data_sp):
    import matplotlib.pyplot as plt
    obj = load_data_sp
    obj.samples["condition"] = ["ADC"] * 6 + ["SCC"] * 6
    obj = obj.filter_missingness(strategy="all_conditions", condition_column="condition")
    obj = obj.limma_trend_dea(design_formula="~0+condition", contrasts={"Test": "SCC-ADC"}, array_weights=True)
    figs, axs = obj.volcano_plot()

    assert isinstance(figs, dict) and isinstance(axs, dict)
    assert isinstance(figs["Test"], plt.Figure) and isinstance(axs["Test"], plt.Axes)

@pytest.mark.integration
def test_plot_pca(load_data_sp, mocker):
    import matplotlib.pyplot as plt
    obj = load_data_sp
    mock_show = mocker.patch("matplotlib.pyplot.show")
    fig, ax = obj.plot_pca(standardize=True)
    mock_show.assert_called_once()

    assert isinstance(fig, plt.Figure) and isinstance(ax, plt.Axes)
