import configparser
import pathlib as path
import logging

import numpy as np
import pandas as pd
import joblib

from SimpleModel import SimpleModel


logging.basicConfig(format='%(asctime)s %(message)s', filename='training.log', level=logging.DEBUG)


def main(cfg):
    # parse config
    DATA_FOLDER = path.Path(cfg["DATA"]["DatasetPath"])
    MODEL_PATH = path.Path(cfg["MODEL"]["FilePath"])
    # do something with data
    X = pd.read_csv(f'{DATA_FOLDER}/{cfg["DATA"]["UsersFile"]}')
    model = SimpleModel()
    model.fit(X[['feature_1']], X['sale_flg'])
    joblib.dump(model, MODEL_PATH)
    logging.info("model was trained")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")
    main(cfg=config)
