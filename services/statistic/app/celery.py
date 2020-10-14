from celery import Celery


app = Celery('app', broker='amqp://admin:mypass@rabbitmq:5672//', include=['app.tasks'])


if __name__ == '__main__':
    app.start()
