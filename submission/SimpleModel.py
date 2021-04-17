from sklearn.linear_model import LogisticRegression


class SimpleModel():
    def __init__(self):
        self.model = LogisticRegression()

    def fit(self, X, y):
        self.features = [c for c in X]
        self.model.fit(X, y)

    def predict(self, X):
        X_test = X[self.features]
        y_pred = self.model.predict(X_test)
        return y_pred
