import matplotlib.pyplot as plt

def plot_feature_importance(importances, features):
    plt.barh(features, importances)
    plt.xlabel("Importance")
    plt.ylabel("Features")
    plt.show()
