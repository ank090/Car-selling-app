import joblib
def singleton(cls):
    """
    decoratror function that make sures only one instance of Model class is active in the session.
    avoiding unccessary loading of pickle models everytime class is instanciated.
    """
    instances = {}
    def get_instances(*args):
        if cls not in instances:
            instances[cls] = cls(*args)
        return instances[cls]
    return get_instances

@singleton
class Models:
    """
    Model class holds encoder and regression model as its attribute which are loaded from pickle file.
    """
    def __init__(self) -> None:
        with open("static/encode_scale.pkl", "rb") as f:
            self.encoder = joblib.load(f)
        with open("static/model.pkl", "rb") as f:
            self.regression_model = joblib.load(f)