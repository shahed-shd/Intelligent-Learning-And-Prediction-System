from model.miscellaneous import save_estimator
from .regression import Regression


def prepare_regression_estimator(X, y, title, features_file_path, targets_file_path):
    rg = Regression(X, y)
    save_estimator(title=title, est_type="regression", est_py_obj=rg, features_file_path=features_file_path, targets_file_path=targets_file_path)

