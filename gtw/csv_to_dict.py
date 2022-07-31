import pandas as pd
from loguru import logger


def get_device_dict(file):
    try:
        device_dict = pd.read_csv(file, delimiter=";", index_col=False).to_dict('list')
        return device_dict
    except Exception as e:
        logger.exception(f"FAIL read csv{file}", e)
        return False
