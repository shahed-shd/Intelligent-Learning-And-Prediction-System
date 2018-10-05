from kivy.storage.jsonstore import JsonStore

class PersistentData(object):
    def __init__(self, store_file_path, *args, **kwargs):
        store = JsonStore(store_file_path)

        if not store.exists('admin'):
            store.put('admin', username='shd', password='1234')

        self.__store = store

    def validate_admin_login(self, adminname, password):
        a = self.__store.get('admin')
        if(a['username'] == adminname and a['password'] == password):
            return True
        else:
            return False


    def change_admin_password(self, new_pw):
        a = self.__store.get('admin')

        un = a['username']
        pw = a['password']

        self.__store.put('admin', username=un, password=new_pw)



    def change_admin_username(self, new_username):
        a = self.__store.get('admin')

        un = a['username']
        pw = a['password']

        self.__store.put('admin', username=new_username, password=pw)
