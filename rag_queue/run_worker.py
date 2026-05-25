from rq import SimpleWorker

from .client.rq_client import queue


def main() -> None:
    worker = SimpleWorker([queue], connection=queue.connection)
    worker.work()


if __name__ == "__main__":
    main()
