EXTRA_DIST = handler/app.py \
             handler/__init__.py \
             handler/rest.py \
             handler/deduplicationlog/__init__.py \
             handler/deduplicationlog/redis/__init__.py \
             handler/workqueue/__init__.py \
             handler/workqueue/celery/__init__.py \
             handler/workqueue/celery/worker.py \
             systemd/grh_handler.service \
             systemd/grh_handler.conf \
             systemd/grh_celery.service \
             systemd/grh_celery.conf \
             tests/__init__.py \
             tests/test_dedup_request.py \
             tests/test_rest_api.py \
             setup.py

check-local:
	python3 -m unittest discover -s tests

# vim:noexpandtab:shiftwidth=8:tabstop=8:softtabstop=8:
