from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def train_linear(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def train_rf(X_train, y_train):
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    return model
