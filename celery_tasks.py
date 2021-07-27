import yagmail
from celery import Celery

from app import app
import config
from models import User


def make_celery(app):

    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379/3',
        broker='redis://localhost:6379/4'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task()
def send_email():
    users = User.query.all()
    emails = [user.email for user in users]
    yagmail.SMTP(config.SENDER_EMAIL, config.SENDER_PASSWORD).send(emails, config.EMAIL_SUBJECT, config.EMAIL_MESSAGE)
    return 'message delivered'
