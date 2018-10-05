import os.path
import pickle

from model.miscellaneous import save_estimator
from model.globalvalues import GlobalValues
from .regression import Regression


def prepare_regression_estimator(X, y, title, features_file_path, targets_file_path):
    rg = Regression(X, y)
    save_estimator(title=title, est_type="regression", est_py_obj=rg, features_file_path=features_file_path, targets_file_path=targets_file_path)


def get_prediction(X, est_id):
    gv = GlobalValues()
    dir_path = os.path.join(gv.get_estimators_path(), str(est_id))
    pkl_path = os.path.join(dir_path, str(est_id)+".pkl")
    with open(pkl_path, 'rb') as f:
        ob = pickle.load(f)
    y = ob.predict(X)
    return y
