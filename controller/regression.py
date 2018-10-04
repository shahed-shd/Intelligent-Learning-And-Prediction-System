import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor


class Regression(object):
    def __init__(self, X, y, **kwargs):
        # Keyword arguments
        test_set_fraction = kwargs.get('test_set_fraction', 0.20)

        # data scaling
        scaler = MinMaxScaler()
        scaler.fit(X)
        X = scaler.transform(X)

        if len(y.shape) == 1:
            # Alpha (regularization strength) of LASSO regression
            lasso_eps = 0.0001
            lasso_nalpha=20
            lasso_iter=5000

            # Min and max degree of polynomials features to consider
            degree_min = 2
            degree_max = 5

            # Test/train split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_set_fraction)

            model_list = []

            # Make a pipeline model with polynomial transformation and LASSO regression with cross-validation, run it for increasing degree of polynomial (complexity of the model)
            for degree in range(degree_min, degree_max+1):
                ml_model = make_pipeline(PolynomialFeatures(degree, interaction_only=False),
                                        LassoCV(eps=lasso_eps,n_alphas=lasso_nalpha,max_iter=lasso_iter, normalize=True,cv=5))
                model_list.append(ml_model)

            # SVR models
            svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
            svr_lin = SVR(kernel='linear', C=1e3)
            svr_poly = SVR(kernel='poly', C=1e3, degree=2)

            model_list.append(svr_rbf)
            model_list.append(svr_lin)
            model_list.append(svr_poly)

            # Now fit the models
            max_score = -1
            chosen_model = None

            for m in model_list:
                m.fit(X_train, y_train)
                score = m.score(X_test, y_test)
                print("NOW:", score, m, "\n\n\n")
                if score > max_score:
                    max_score = score
                    chosen_model = m

            self.n_targets = 1
        else:
            chosen_model = MultiOutputRegressor(GradientBoostingRegressor(), n_jobs=-1)
            chosen_model.fit(X, y)
            self.n_targets = len(y[0])

        self.n_features = len(X[0])
        self.scaler = scaler
        self.model = chosen_model
        print("SELECTED:", self.model)

    def predict(self, X):
        scaled_X = self.scaler.transform(X)
        pred = self.model.predict(scaled_X)
        return pred
