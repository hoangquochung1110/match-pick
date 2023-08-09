FROM apache/airflow:2.6.3
ENV PYTHONPATH=/opt/epl_scrapy
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
