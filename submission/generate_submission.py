import configparser
import pathlib as path

import numpy as np
import pandas as pd
import joblib


def main(cfg):
    # parse config
    DATA_FOLDER = path.Path(cfg["DATA"]["DatasetPath"])
    USER_ID = cfg["COLUMNS"]["USER_ID"]
    PREDICTION = cfg["COLUMNS"]["PREDICTION"]
    MODEL_PATH = path.Path(cfg["MODEL"]["FilePath"])
    SUBMISSION_FILE = path.Path(cfg["SUBMISSION"]["FilePath"])
    # do something with data
    X = pd.read_csv(f'{DATA_FOLDER}/{cfg["DATA"]["UsersFile"]}')
    model = joblib.load(MODEL_PATH)
    
    submission = X[[USER_ID]].copy()
    # submission[PREDICTION] = np.random.choice([0, 1], len(submission))
    submission[PREDICTION] = model.predict(X)
    submission.to_csv(SUBMISSION_FILE, index=False)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")
    main(cfg=config)
