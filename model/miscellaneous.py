import hashlib
import os.path
import datetime
import shutil
import pickle

from sqlalchemy import text

from model import database
from .globalvalues import GlobalValues


def get_next_free_id(engine, table_name, column_name='id'):
    '''Returns the next id to be used. Also checks gap in the sequence.
    `engine` is SQLAlchemy object returned by create_engine().'''

    sql_cmd = text('''SELECT MIN(a.{colname} + 1) AS next
    FROM {tablename} AS a
    LEFT OUTER JOIN {tablename} AS b
    ON a.{colname} + 1 = b.{colname}
    WHERE b.{colname} IS NULL;'''.format(tablename=table_name, colname=column_name))

    qry_res = engine.execute(sql_cmd)
    next_id = qry_res.fetchone()[0]

    # If the table is empty, next_id will be None. In that case, id starts from 1.
    next_id = next_id if next_id else 1

    return next_id


def get_sha256_hex_digest(s):
    '''Returns SHA256 hex digest of string `s`.'''
    # Converting to bytes string and getting hex digest
    return hashlib.sha256(bytes(s, 'utf-8')).hexdigest()


def save_estimator(title, est_type, est_py_obj, features_file_path, targets_file_path):
    est = database.Estimator()
    est.title = title
    est.type = est_type
    est.n_features = est_py_obj.n_features
    est.n_targets = est_py_obj.n_targets
    est.build_datetime = datetime.datetime.now()

    db = database.DB()
    db.add_estimator(est)

    gv = GlobalValues()
    dir_path = os.path.join(gv.get_estimators_path(), str(est.id))
    os.makedirs(dir_path)

    with open(os.path.join(dir_path, str(est.id)+'.pkl'), 'wb') as fp:
        pickle.dump(est_py_obj, fp)

    shutil.copyfile(features_file_path, os.path.join(dir_path, str(est.id)+'_features.txt'))
    shutil.copyfile(targets_file_path, os.path.join(dir_path, str(est.id)+'_targets.txt'))

