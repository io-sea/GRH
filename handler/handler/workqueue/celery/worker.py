"""A celery app tasked with requests"""

from celery import Celery

from ... import handle

app = Celery('celery_handler')
handle = app.task(handle)
