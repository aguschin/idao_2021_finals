# IDAO 2021 Finals - example submission

## Python version
Docker image will have python 3.8.5. The `scorer.py` is tested with the same python version. You will need to install Docker and docker-compose to your working machine.

## TLDR; running example train script and submitting example solution
1. Run `docker-compose -f docker-compose.train.yaml up`. This should produce a `submission/model.joblib` file with trained model and a tar archive with your model in `generated_submissions` folder. First time docker-compose could run for some time to build the docker image. Next time it will be much quicker.
2. Run `docker-compose -f docker-compose.test.yaml up`. This will produce a .csv file with your predictions in `generated_submissions` folder.

Both steps should run without any errors. Test and train data samples required to run this could be found in `tests/` folder.

## How to check that your submission is working as expected inside the docker container?
1. Review `docker-compose.train.yaml` and `docker-compose.test.yaml` and make sure you understand how your folders with submission and data are mapped inside the container. If your train/val data or submission files are located in different directories, make changes in docker-compose file. To speed up initial debug, you could remove memory & cpu resource constraints.
2. Run following: `docker-compose -f docker-compose.train.yaml up`. You can of course train your model without any docker container (read on that below), but using docker ensures that the environment in which you train it remains the same as in the Yandex.Contest. This prevents some errors, arising from the library version differences.
3. Run following: `docker-compose -f docker-compose.test.yaml up`. During the execution you can track the CPU and Memory resources used with `docker stats`. If you exceed memory/cpu resources or time limit here, there is a good chance that your submission will fail to run when submitted to Yandex.Contest. Note that different CPU could run your solution for different amount of time, thus running time on your machine and Yandex.Contest will probably differ.
Otherwise, if this executes succesfully (namely, the submission file is saved in `generated_submissions/` folder), then it should work correctly when you send this archive to the Yandex.Contest. But still, because the test_data (which is not available to you directly, but only be provided for your submission in Yandex.Contest) could be different from the train_data, you could encounter other errors there. The obvious one would happen if you somehow expect the target column to be available in the test data. You could check the test data example in `tests/test_data_sample` folder - but the only difference in data schema are the missing target columns in the `funnel.csv`.
4. Now you can use generated submission file to check if metric is calculated correctly. You can first split data to train and val parts and calculate the exact score on your validation part. Using the scorer.py script, for example:
    ```
    python scorer.py tests/y_true.csv tests/y_pred.csv
    ```

## How to set up local virtual env to use it for model development?
You have at least two options here:
1. You could build and run docker container, and develop your model inside it (for example, see VSCode tutorial to do that https://code.visualstudio.com/docs/remote/containers). You could start a container using:
    ```
    docker-compose -f docker-compose.train.yaml run app bash
    ```
2. You could create new virtual env and install requirements.txt there. For this purpose you could any tool you like to manage virtual envs - for example: virtualenv, conda, pipenv, poetry.

## Notes

1. Note that you need to edit both `train_model.py` and `generate_submission.py` if you are making changes in one of them. For example, if you use LogisticRegression instead of SimpleModel while training, you need to do the same while testing. Thus, it is convenient to keep all model and data processing logic in `SimpleModel.py`.

2. Note that a submission archive name is displayed in "Compilation log" (Лог компиляции). You could use that to identify which exact archive was sent in the particular submission. The other way around is to download your submission.

## Issues

1. Running the solution on Windows we encountered a bug when sometimes submission folder caches inside the docker image (which is not supposed to happen). In that case try to add `--build` flag to your docker-compose command.
