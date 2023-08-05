from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator


def testing_slack_notify():
    a = 3 + '4'
    return a


def slack_alert(context):
    ti = context.get('task_instance')
    dag_name = context.get('task_instance').dag_id
    task_name = context.get('task_instance').task_id    
    execution_date = context.get('execution_date')
    log_url = context.get('task_instance').log_url 
    dag_run = context.get('dag_run') 
   
    mssg = f"""
        :red_circle: Pipeline Failed.        
        *Dag*:{dag_name}
        *Task*: {task_name}
        *Execution Date*: {execution_date}
        *Task Instance*: {ti}
        *Log Url*: {log_url}
        *Dag Run*: {dag_run}        
    """   
    slack_notification = SlackWebhookOperator(
            task_id = "tsk_slack_notification",
            http_conn_id = "slack_conn_id",
            message = mssg,
            channel = "#financedeptpipeline"
        )
    return slack_notification.execute(context=context)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 8),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=3)
}


with DAG('Addition_Pipeline',
        default_args=default_args,
        schedule_interval = '@daily',
        on_failure_callback = slack_alert,
        catchup=False) as dag:

        addtion_of_numbers = PythonOperator(
            task_id= 'tsk_addtion_of_numbers',
            python_callable=testing_slack_notify
            )