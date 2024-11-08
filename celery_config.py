from celery import Celery
from flask import Flask

def make_celery(app: Flask):
    celery = Celery(app.import_name, broker=app.config['broker_url'], backend=app.config['result_backend'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery