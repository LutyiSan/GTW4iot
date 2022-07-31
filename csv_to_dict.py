import pandas as pd


def get_device_dict(file):
    device_dict = pd.read_csv(file, delimiter=";", index_col=False).to_dict('list')
    return device_dict
