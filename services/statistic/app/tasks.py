import requests
from clickhouse_driver import Client
from sqlalchemy import create_engine
from requests.exceptions import RequestException

from .celery import app

db_string = 'postgresql://admin:mypass@postgresql:5432/geo'
pg_db = create_engine(db_string)
ch_db = Client(host='clickhouse', database='geo')


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls collect_data() every 60 seconds.
    sender.add_periodic_task(60.0, collect_data.s(), name='collect_data')


@app.task(autoretry_for=(RequestException,),
          retry_backoff=True)
def notification(user_id, points):
    """Send POST notification"""
    url = 'some/notification/url/'
    json = {'user_id': user_id, 'points': points}
    print("*** Request sent ***")
    # requests.post(url=url, json=json)


@app.task
def collect_data():
    """Get data from Postgres and store it in ClickHouse"""
    user_data = pg_db.execute('SELECT user_id, SUM(points) AS POINTS FROM api_balance GROUP BY user_id').fetchall()
    # Compare previous and new user points
    for user_id, points in user_data:
        previous_points = ch_db.execute("SELECT points FROM balance WHERE (user_id, created) IN "
                                        "(SELECT user_id, max(created) FROM balance WHERE user_id=%(user_id)s "
                                        "GROUP BY user_id)", {'user_id': user_id})
        # Send notification
        if previous_points and previous_points[0][0] != points:
            if points == 0:
                notification.delay(user_id, points)
            elif previous_points[0][0] <= 1000 < points:
                notification.delay(user_id, points)
            elif points > 100000:
                notification.delay(user_id, points)

    ch_db.execute("INSERT INTO balance (user_id, points) VALUES", (line for line in user_data))
