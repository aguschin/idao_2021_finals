# IDAO 2021 Finals

## Background information.

Bank Otkritie is one of the top 10 major banks in Russia and a systemically important credit institution, which offers a full range of cutting-edge financial services to its corporate, retail, SMEs and Private banking clients.

The single shareholder of Bank Otkritie is the Central Bank of the Russian Federation with 100% interest in the share capital.

In May 2018, the Supervisory Board of Bank Otkritie approved its three-year business development strategy until the end of 2020. The key strategic target of the bank is to become the market leader providing excellent quick and convenient services to clients.
Bank Otkritie operates through 524 offices in 227 cities located in 73 regions of the Russian Federation.

Solid financial stability of the bank is proved by credit ratings assigned by domestic agencies ACRA (АА(RU)), RAEX (ruAA-) and NCR (AA+.ru), as well as international rating agency Moody’s (Ba2).

Today, Otkritie is a large-scale financial group with a great potential for the further business growth. The companies of the group hold leading positions in the Russian financial market, such as Rosgosstrakh and Rosgosstrakh Life insurance companies, Otkritie Non-State Pension Fund, Otkritie Asset Management Company, Otkritie Broker, Baltic Leasing, and Customs Payment System.

Moving on to the task. We offer you to solve one of the Retail business's problem, namely one of campaign management tasks. On a regular basis, Bank Otkritie forms special offers for the most loyal private individual customers. The call center manager provides the offers to the specific customers. In case of the customer's positive response, the bank receives income proportional to the amount of the loan issued. At the same time, different customers require different time for consultation, respectively, communications on customers differ in cost for the bank. In addition, we don’t know in advance the loan amount the customer will take.

## Objective.

You task is to identify clients which will accept the offer and take the credit and maximize average net profitability.

## Quality metric.

Submissions are evaluated using the formula below. For each client we calculate the amount of money earned and find average value for all clients (average net income per client - ANIC).

Net income per client:

```NIC = sale_flg * sale_amount - contacts * CALL_COST```

Average Net Income per Client (ANIC):

```
ANIC = Σ_{i=1:N} NIC_i / N, 
where N is the number of clients (regardless of the their decision on the offer)
```

For each client you will need to submit either 0 or 1. We assume that the clients you select receive the communication from the bank. Each of them will either accept or decline the offer. If you identified the client as a class 0, we assume we did not offer him the loan. For each client we calculate the amount of money, the bank earned or lost in the process (earned if a loan was accepted, lost if a loan was rejected). These values are averaged for all clients in the test data. Thus, we get "the average money earned from offering the loans". The better the model, the more relevant client it will identify and more money will be earned per client. To provide few relevant values, the perfect model on train data could get around 6700, and the perfectly bad model should get a negative score. You can calculate more relevant baseline values to estimate your model quality by comparison using the scorer script.

- `CALL_COST` - is an estimated communication cost, which could include direct and indirect costs (like time the operator spent on call or loyalty decrease after repeated communications). Because we resample the data to provide more samples with class 1, there is a resampling multiplier, which is already taken into account in this constant.
- `contacts` - is the number of contacts held with the particular client.
- `sale_flg` - a 0 or 1, indicating either the client took a loan as a result.
- `sale_amount` - amount of money the bank earned on this particular loan.
- `N` - the exact number of clients in the data subset for which the metric is calculated.

The metric implementation [could be found here](https://github.com/aguschin/idao_2021_finals/blob/main/scorer.py).

## Input format

You are provided with historical data for one year on customers who receive an offer to purchase PACL (Pre-Approved Credit Loan). Train data [could be downloaded here](https://disk.yandex.ru/d/XaSzELIxOveSnw). Note, that the test data is not available to you directly, but will be available to your submission when Yandex.Contest will run it.

Data consists of the following files:
- `trxn.csv`: Card operations data.
  Contains the following columns:
  - `client_id`: Client ID. 
  - `card_id`: Card ID.
  - `tran_time`: Operation datetime.
  - `tran_amt_rur`: Operation sum in RUB.
  - `mcc_cd`: MCC - Merchant Category Code.
  - `merchant_cd`: Merchant Code.
  - `txn_country`: Country, where the operation happened.
  - `txn_city`: City, where the operation happened.
  - `tsp_name`: Merchant name.
  - `txn_comment_1`: Comment #1
  - `txn_comment_2`: Comment #2
  
- `aum.csv`: AUM (Assets Under Management) data.
  Contains the following columns:
  - `client_id`: Client ID.
  - `month_end_dt`: Date (in the "end of the month" format).
  - `product_code`: Account type.
  - `balance_rur_amt`: EOP (End Of Period) sum of balance in RUB.

- `balance.csv`: Balance data.
  Contains the following columns:
  - `client_id`: Unique client ID.
  - `prod_cat_nanme`: Product category.
  - `prod_group_name`: Product group.
  - `crncy_cd`: Currency ID.
  - `eop_bal_sum_rur`: EOP (End Of Period) sum of balance in current month in RUB.
  - `min_bal_sum_rur`: Minimum sum of balance in current month in RUB.
  - `max_bal_sum_rur`: Maximum sum of balance in current month in RUB.
  - `avg_bal_sum_rur`: Average sum of balance in current month in RUB.

- `client.csv`: Social-demographic data.
  Contains the following columns:
  - `client_id`: Client ID.
  - `gender`: Gender.
  - `age`: Age.
  - `region`: Region ID.
  - `city`: City ID.
  - `education`: Education level.
  - `citizenship`: Client citizenship.
  - `job_type`: Job status.

- `com.csv`: Campaign data. 
  Contains the following columns:
  - `client_id`: Client ID.
  - `channel`: Channel.
  - `prod`: Offered product name.
  - `agr_flg`: client agreed to take the offer (binary var).
  - `otkaz`: client rejected the offer (binary var).
  - `dumaet`: client is not sure about the offer (binary var).
  - `ring_up_flg`: number of ring up cases.
  - `not_ring_up_flg`: number of no ring up cases.
  - `count_comm`: number of communications.

- `deals.csv`: Deals data.
  Contains the following columns:
  - `client_id`: Client ID.
  - `prod_type_name`: Product type.
  - `agrmnt_start_dt`: Deal start date.
  - `agrmnt_close_dt`: Deal close date.
  - `crncy_cd`: Currency ID.
  - `agrmnt_rate_active`: Deal interest rate.
  - `agrmnt_rate_passive`: Deal interest rate.
  - `agrmnt_sum_rur`: Deal sum.    

- `dict_mcc.csv`: MCC (Merchant Category Code) dictionary.
  Contains the following columns:
  - `mcc_cd`: MCC code.
  - `brs_mcc_group`: MCC group.
  - `brs_mcc_subgroup`: MCC subgroup.
    
- `payments.csv`: Salary and pension payments.
  Contains the following columns:
  - `client_id` : Client ID.
  - `day_dt` : Payment date. 
  - `sum_rur` : Payment sum in RUB.
  - `pmnts_name` : Payment type.
    
- `funnel.csv`: PACL sales funnel.
  Contains the following columns:
  - `client_id` : Client ID.
  - `sale_flg` : Sold flag.
  - `sale_amount` : Amount of money bank earned in RUB.
  - `contacts` : Number of contacts per offer.
  - `client_segment`: Business segment of the client.
  - `region_cd`: Region ID.

Names of several fields have been anonymized intentionally. These fields are called `feature_1`, `feature_2`, etc.


## Output format

Please submit a `.zip` or `.tar.gz` archive that includes a Makefile with tags **build:** and **run:** that will be executed one after another in a container.
The log, produced during the build and run phases, will not be visible on the submission page, so it is only possible to debug the installation using Docker on your working machine. Read more in the example submission repo. 
For the run phase your code should process the data in the `data/` folder and is expected to produce the file `submission.csv` with predictions.
Test data in `data/` folder has the same format and set of columns as the train data, but the values in the (`contacts`, `sale_amount`, `sale_flg`) columns are missing. Note that `tests/test_data` has the exact same set of columns and could be used to test your solution locally.
**submission.csv** should contain only two columns: `client_id` and `target`.

Example solution, along with `Dockerfile` and `requirements.txt` [can be found here](https://github.com/aguschin/idao_2021_finals). `requirements.txt` contains all the libraries which are installed in the docker container. The container you build will have Python 3.8.5 installed. The version of gcc/g++ installed is 9.3.0. Note that Makefile should be contained in the archive immediately, not inside additional folder.

Public leaderboard is based on 1/3 of the test data. 
Private leaderboard is based on the remaining 2/3 and will be revealed after the end of competition.

**Only the last successful submission** is used to compute public and private leaderbord scores.
You should make sure, that at the end of competition the last successful submission is actually your very best attempt!

## Resource constraints

The solution your submit will run with resource constraints of 1 CPU and 2 Gb RAM. The time limit is 15 minutes. Note that the running time on your machine and on Yandex.Contest servers could be different due to different hardware.

## Notes

You may use additional information, data, advice on your own risk. 
All solutions will be checked by the jury to guarantee fair play. 
Please ask us in any vague or unclear case.

If you face any problems or have questions, please contact us via e-mail: hello@idao.world.
