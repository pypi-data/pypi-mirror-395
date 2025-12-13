from queue import SimpleQueue
from typing import Any
from dataclasses import dataclass, field


@dataclass
class Job:
    operation: str
    source: str
    target: str
    payload: dict[Any, Any] = field(default_factory=dict)


class JobRunner:
    def __init__(self) -> None:
        self.queue: SimpleQueue = SimpleQueue()

    def add_job(self, job):
        return self.queue.put(job)

    def run(self):
        while not self.queue.empty():
            job = self.queue.get()
            print(job)

