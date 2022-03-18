"""A celery app tasked with requests"""

from celery import Celery

from ... import dispatch

app = Celery('celery_handler')
dispatch = app.task(dispatch)
