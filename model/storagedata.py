from kivy.storage.jsonstore import JsonStore

class StorageData(object):
    def __init__(self, store_file_path, *args, **kwargs):
        print("DEBUG")
        store = JsonStore(store_file_path)

        if not store.exists('admin'):
            store.put('admin', username='shd', password='1234')






