Changelog
=========

All notable changes to this project will be documented in this file.
The format roughly follows `Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`_
and adheres to semantic versioning where possible.



25.12.09 - 2025-12-08
------------------

Added
~~~~~

- Feature importance computation for autoregressive synthesis

Changed
~~~~~~~

- Improved Prediction tab UX

Fixed
~~~~~
- Logistic regression prediction threshold optimization and input shape handling
- GPU locking issues in logistic regression predictions
- CSV filename collision in visualization causing data overwrites
- PCA object propagation through data pipeline for feature importance


25.12.07 - 2025-12-07
------------------

Changed
~~~~~~~

- PCA visualization now displays feature correlation matrix instead of covariance matrix for improved interpretability. Diagonal values are always 1, and all values are normalized between -1 and 1.


25.12.01 - 2025-12-01
------------------

Fixed
~~~~~

- Predictions now use the optimized threshold computed during training (via Youden's J statistic) instead of hardcoded 0.5. Applies to all model types and prediction modes.


25.11.23 - 2025-11-23
------------------

- First public release of AuToMaR.
