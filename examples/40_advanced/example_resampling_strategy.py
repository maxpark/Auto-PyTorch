"""
======================
Tabular Classification with different resampling strategy
======================

The following example shows how to fit a sample classification model
with different resampling strategies in AutoPyTorch
By default, AutoPyTorch uses Holdout Validation with
a 67% train size split.
"""
import os
import tempfile as tmp
import warnings

os.environ['JOBLIB_TEMP_FOLDER'] = tmp.gettempdir()
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

import sklearn.datasets
import sklearn.model_selection

from autoPyTorch.api.tabular_classification import TabularClassificationTask
from autoPyTorch.datasets.resampling_strategy import CrossValTypes, HoldoutValTypes

############################################################################
# Default Resampling Strategy
# ============================

############################################################################
# Data Loading
# ------------
X, y = sklearn.datasets.fetch_openml(data_id=40981, return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
    X,
    y,
    random_state=1,
)

############################################################################
# Build and fit a classifier with default resampling strategy
# -----------------------------------------------------------
api = TabularClassificationTask(
    # 'HoldoutValTypes.holdout_validation' with 'val_share': 0.33
    # is the default argument setting for TabularClassificationTask.
    # It is explicitly specified in this example for demonstrational
    # purpose.
    resampling_strategy=HoldoutValTypes.holdout_validation,
    resampling_strategy_args={'val_share': 0.33}
)

############################################################################
# Search for an ensemble of machine learning algorithms
# -----------------------------------------------------
api.search(
    X_train=X_train,
    y_train=y_train,
    X_test=X_test.copy(),
    y_test=y_test.copy(),
    optimize_metric='accuracy',
    total_walltime_limit=150,
    func_eval_time_limit_secs=30
)

############################################################################
# Print the final ensemble performance
# ------------------------------------
y_pred = api.predict(X_test)
score = api.score(y_pred, y_test)
print(score)
# Print the final ensemble built by AutoPyTorch
print(api.show_models())

# Print statistics from search
print(api.sprint_statistics())

############################################################################

############################################################################
# Cross validation Resampling Strategy
# =====================================

############################################################################
# Build and fit a classifier with Cross validation resampling strategy
# --------------------------------------------------------------------
api = TabularClassificationTask(
    resampling_strategy=CrossValTypes.k_fold_cross_validation,
    resampling_strategy_args={'num_splits': 3}
)

############################################################################
# Search for an ensemble of machine learning algorithms
# -----------------------------------------------------------------------

api.search(
    X_train=X_train,
    y_train=y_train,
    X_test=X_test.copy(),
    y_test=y_test.copy(),
    optimize_metric='accuracy',
    total_walltime_limit=150,
    func_eval_time_limit_secs=30
)

############################################################################
# Print the final ensemble performance
# ------------
y_pred = api.predict(X_test)
score = api.score(y_pred, y_test)
print(score)
# Print the final ensemble built by AutoPyTorch
print(api.show_models())

# Print statistics from search
print(api.sprint_statistics())

############################################################################

############################################################################
# Stratified Resampling Strategy
# ===============================

############################################################################
# Build and fit a classifier with Stratified resampling strategy
# --------------------------------------------------------------
api = TabularClassificationTask(
    # For demonstration purposes, we use
    # Stratified hold out validation. However,
    # one can also use CrossValTypes.stratified_k_fold_cross_validation.
    resampling_strategy=HoldoutValTypes.stratified_holdout_validation,
    resampling_strategy_args={'val_share': 0.33}
)

############################################################################
# Search for an ensemble of machine learning algorithms
# -----------------------------------------------------
api.search(
    X_train=X_train,
    y_train=y_train,
    X_test=X_test.copy(),
    y_test=y_test.copy(),
    optimize_metric='accuracy',
    total_walltime_limit=150,
    func_eval_time_limit_secs=30
)

############################################################################
# Print the final ensemble performance
# ====================================
y_pred = api.predict(X_test)
score = api.score(y_pred, y_test)
print(score)
# Print the final ensemble built by AutoPyTorch
print(api.show_models())

# Print statistics from search
print(api.sprint_statistics())
