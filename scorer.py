from __future__ import print_function
from sys import argv
from sys import exit
from sys import stderr
import pandas as pd


USER_ID = 'client_id'
PREDICTION = 'target'
SPLIT = 'split'
CONTACTS = 'contacts'
SALE_FLAG = 'sale_flg'
SALE_AMOUNT = 'sale_amount'
TRUTH_COLUMNS = [USER_ID, SPLIT, CONTACTS, SALE_AMOUNT, SALE_FLAG]
PREDICTION_COLUMNS = [USER_ID, PREDICTION]
CALL_COST = 400 / 0.1
PUBLIC = 'public'
PRIVATE = 'private'


def show_presentation_error(message):
    print(message, file=stderr)
    exit(4)


def read_truth_file(path):
    """READ AND CHECK TRUTH FILE"""
    truth = pd.read_csv(path)
    assert set(truth) == set(TRUTH_COLUMNS)
    assert set(truth[SPLIT]) == set([PUBLIC, PRIVATE])
    return truth


def read_user_file(path):
    """READ AND CHECK PREDICTIONS FILE"""
    user = pd.read_csv(path)
    if set(user) != set(PREDICTION_COLUMNS):
        show_presentation_error(
            "prediction.csv is expected to have {} columns, but has {set(user)} columns"
            .format(set(PREDICTION_COLUMNS))
        )
    if len(set(user[PREDICTION]).difference([1, 0])) > 0:
        show_presentation_error("predictions should be either 1 or 0")
    return user


def calculate_metric(truth_file, user_file):

    truth = read_truth_file(truth_file)
    user = read_user_file(user_file)

    """CHECK USER FILE AGAINST TRUTH FILE"""
    prediction_dict = {row[USER_ID]: row[PREDICTION] for i, row in user.iterrows()}
    if set(prediction_dict.keys()) != set(truth[USER_ID]):
        show_presentation_error(
            "{} from y_true.csv and predictions.csv are not the same".format(USER_ID)
        )

    """MERGE THEM TOGETHER"""
    truth[PREDICTION] = truth[USER_ID].map(prediction_dict)

    """CALCULATE METRIC VALUES"""
    selected = truth.query("{} == 1".format(PREDICTION))
    selected['gain'] = selected[SALE_FLAG] * selected[SALE_AMOUNT].fillna(0) - selected[CONTACTS] * CALL_COST
    money_earned = selected.groupby(SPLIT).gain.sum()
    money_earned[PUBLIC] = (
        money_earned.get(PUBLIC, 0) / len(truth.query('{} == "{}"'.format(SPLIT, PUBLIC)))
    )
    money_earned[PRIVATE] = (
        money_earned.get(PRIVATE, 0) / len(truth.query('{} == "{}"'.format(SPLIT, PRIVATE)))
    )
    return money_earned[PUBLIC], money_earned[PRIVATE]


if __name__ == '__main__':
    # the Yandex.Contest use case
    if len(argv) == 4:
        user_file, input_file, truth_file = argv[1], argv[2], argv[3]
    # the usual use case
    elif len(argv) == 3:
        truth_file, user_file = argv[1], argv[2]
    public, private = calculate_metric(truth_file, user_file)
    print('{} is final (private) score; {} - public score'.format(private, public))
