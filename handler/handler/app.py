from argparse import ArgumentParser

from .deduplicationlog.redis import RedisDeduplicationLog
from .rest import get_app
from .workqueue.celery import CeleryWorkQueue

def health_check():
    return "OK\n"

def main():
    """A rest server to defer requests to celery worker

    This function generates a script through entry_points into setup.py.

    $ grh_handler --host 127.0.0.1 --port 5000 &

    To check if the server is up and running, poll for a 200 on:

    $ curl http://127.0.0.1:5000/health
    """
    parser = ArgumentParser(description=__doc__)

    parser.add_argument(
            "--host", default="0.0.0.0",
            help="The hostname to listen on (defaults to %(default)s)"
            )
    parser.add_argument(
            "--port", default=5000, type=int,
            help="The port of the webserver (defaults to %(default)s)"
            )
    parser.add_argument(
            "backend", default="redis://localhost",
            help=("Celery's backend URL (defaults to %(default)s); note "
                  "that celery's workers need to be configured accordingly")
            )
    parser.add_argument(
            "broker", default="redis://localhost",
            help=("Celery's broker URL (defaults to %(default)s); note "
                  "that celery's workers need to be configured accordingly")
            )
    parser.add_argument(
            "dedup_backend", default="redis://localhost",
            help=("Dedup backend URL (defaults to %(default)s); note that this "
                  "URL must conform to a Redis server database or be empty. If "
                  "empty, no deduplication is done.")
            )
    parser.add_argument(
            "dedup_slot_ms", default=500, type=int,
            help=("Request, which is similar to an already registered "
                  "request younger than dedup_slot_ms milliseconds, "
                  "creates no new request. If dedup_slot_ms is inferior "
                  "or equal to 0, no deduplication is done.")
            )

    args = parser.parse_args()

    if args.dedup_backend and args.dedup_slot_ms > 0:
        deduplication_log = RedisDeduplicationLog(args.dedup_slot_ms,
                                                  args.dedup_backend)
    else:
        deduplication_log = None

    app = get_app(CeleryWorkQueue(args.backend, args.broker), deduplication_log)
    app.add_url_rule('/health', 'health', health_check, methods=['GET'])
    app.run(host=args.host, port=args.port)

if __name__ == "__main__":
    if __package__ is None:
        __package__ = "handler"
    __import__(__package__)
    main()
