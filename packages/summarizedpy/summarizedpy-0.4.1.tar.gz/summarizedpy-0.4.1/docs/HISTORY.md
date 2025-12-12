# History

## 0.4.1 (2025-12-04)

* Patched a minor bug in filter_features and filter_samples.

## 0.4.0 (2025-11-27)

* Added new features to allow saving and loading SP objects using pickle.

## 0.3.1 (2025-11-26)

* Added plot_pca method to visualize data with PCA.
* Updated package Python dependency to 3.11+
* Fixed a bug due to recent dependency breaks (pyjanitor, pandas_flavor)

## 0.2.0 (2025-10-24)

* Added select_variable_features method to allow filtering for highly variable features based on mean-variance trend deviation.

## 0.1.4 (2025-10-23)

* Fixed a minor bug in filtering functions that would sometimes cause failure when running multiple filters in succession.

## 0.1.3 (2025-10-17)

* Added loads of extra documentation and usage examples.

## 0.1.2 (2025-10-16)

* Patched bug in limma_trend_dea that would sometimes break design_formula.

## 0.1.1 (2025-10-16)

* Patched bug that accidentally omitted R modules.

## 0.1.0 (2025-10-14)

* First (beta) release of on PyPI.
