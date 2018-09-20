# Values in this file are manually set.

import os


class GlobalValues(object):
    def __init__(self, **kwargs):
        self.app_dir = '/home/shahed/ShdHomeData/ILPS'


    def get_persistent_data_file_path(self):
        p = 'data/persistent_data.json'
        return os.path.join(self.app_dir, p)


    def get_estimators_path(self):
        p = 'data/estimators'
        return os.path.join(self.app_dir, p)
