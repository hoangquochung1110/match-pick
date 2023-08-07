import datetime
import logging

import pendulum
from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator


def get_latest_finished_match():
    from epl_scrapy.epl_scrapy.spiders.arsenal_match_list_spider import \
        ArsenalMatchListSpider

@dag(
    dag_id="match-scraping",
    schedule_interval="*/5 * * * *", # https://crontab.guru/#*_12_*_*_*
    start_date=pendulum.datetime(2023, 8, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def ArsenalMatch():
    latest_finished_match = PythonOperator(
        task_id="get_latest_finished_match",
        python_callable=get_latest_finished_match
    )

    @task(task_id="logger")
    def log_match_id(id):
        logging.info(id)

    log_result = log_match_id(latest_finished_match)


dag = ArsenalMatch()
