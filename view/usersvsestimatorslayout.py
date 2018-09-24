from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty


from .miscellaneous import represent_user_in_rv, represent_estimator_in_rv
from .rv import RV
from model import database


class RVViewClass(BoxLayout):
    user_id = NumericProperty(None, allownone=True)
    estimator_id = NumericProperty(None, allownone=True)
    db = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(RVViewClass, self).__init__(**kwargs)

        self.label_user_info = Label(text='', bold=True, italic=True)
        self.add_widget(self.label_user_info)
        self.label_estimator_info = Label(text='', bold=True, italic=True)
        self.add_widget(self.label_estimator_info)
        self.switch_is_accessible = Switch(active=True)
        self.add_widget(self.switch_is_accessible)

        self.bind(user_id=self.represent_info)
        self.bind(estimator_id=self.represent_info)
        self.bind(db=self.represent_info)
        self.switch_is_accessible.bind(active=self.switch_is_accessible_bind)


    def switch_is_accessible_bind(self, *args):
        user = self.db.get_user_by_id(self.user_id)
        estimator = self.db.get_estimator_by_id(self.estimator_id)

        if self.switch_is_accessible.active:
            if not (estimator in user.estimators):
                user.estimators.append(estimator)
        else:
            user.estimators.remove(estimator)


    def represent_info(self, *args):
        if self.user_id and self.estimator_id and self.db:
            user = self.db.get_user_by_id(self.user_id)
            estimator = self.db.get_estimator_by_id(self.estimator_id)

            self.label_user_info.text = represent_user_in_rv(user)
            self.label_estimator_info.text = represent_estimator_in_rv(estimator)
            self.switch_is_accessible.active = True


class RVUsersVSEstimators(RV):
    def __init__(self, **kwargs):
        super(RVUsersVSEstimators, self).__init__(**kwargs)
        self.viewclass = 'RVViewClass'


class UsersVSEstimatorsLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(UsersVSEstimatorsLayout, self).__init__(**kwargs)

        n = 18
        idx = 16
        self.btn_add_new = Button(text='Add new access', italic=True, on_release=self.btn_add_new_do, size_hint=(0.20, 1/n), pos_hint={'x': 0.05, 'y': 1/n*idx})
        self.add_widget(self.btn_add_new)
        self.add_widget(Label(text='Search bar:', bold=True, italic=True, size_hint=(0.10, 1/n), pos_hint={'x': 0.45, 'y': 1/n*idx}))
        self.text_input_search_username = TextInput(text='', hint_text='username like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.20, 1/n), pos_hint={'x': 0.55, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_username)
        self.text_input_search_estimator_title = TextInput(text='', hint_text='estimator title like', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.20, 1/n), pos_hint={'x': 0.77, 'y': 1/n*idx})
        self.add_widget(self.text_input_search_estimator_title)

        idx -= 1
        self.rv = RVUsersVSEstimators(size_hint=(1, 1/n*(idx-2)), pos_hint={'x': 0, 'y': 1/n*(2)})

        db = database.DB()
        L = db.get_users_estimators_access_list()
        self.rv.data = [{'user_id': u.id, 'estimator_id': e.id, 'db': db} for u, e in L]

        self.db = db
        self.add_widget(self.rv)

        idx = 1
        self.btn_reset = Button(text='Reset', italic=True, on_release=self.btn_reset_do, size_hint=(0.25, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})
        self.add_widget(self.btn_reset)
        self.btn_done = Button(text='Done', italic=True, on_release=self.btn_done_do, size_hint=(0.25, 1/n), pos_hint={'x': 0.50, 'y': 1/n*idx})
        self.add_widget(self.btn_done)

        self.text_input_search_username.bind(text=self.search_bind)
        self.text_input_search_estimator_title.bind(text=self.search_bind)


    def btn_add_new_do(self, *args):
        pass


    def btn_done_do(self, *args):
        self.db.session.commit()
        self.btn_reset_do()


    def btn_reset_do(self, *args):
        self.text_input_search_username.text = ''
        self.text_input_search_estimator_title.text = ''
        self.search_bind()
        self.db.session.flush()


    def update_rv_data(self, user_estimator_pair_list, *args):
        self.rv.data = [{'user_id': u.id, 'estimator_id': e.id, 'db': self.db} for u, e in user_estimator_pair_list]


    def search_bind(self, *args):
        usernamelike = '%' + self.text_input_search_username.text + '%'
        estimatortitlelike = '%' + self.text_input_search_estimator_title.text + '%'

        qry = self.db.session.query(database.User, database.Estimator).filter(database.User.estimators)

        if len(usernamelike) > 2:
            qry = qry.filter(database.User.username.like(usernamelike))
        if len(estimatortitlelike) > 2:
            qry = qry.filter(database.Estimator.title.like(estimatortitlelike))

        user_estimator_pair_list = qry.all()
        self.update_rv_data(user_estimator_pair_list)
