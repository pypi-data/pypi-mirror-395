import time
from typing import Generator, Optional

from ray_cli.core.sender import BaseSender
from ray_cli.modes import DmxDataGenerator
from ray_cli.utils import Feedback, ProgressBar, TableLogger


class Throttle:
    def __init__(self, rate: int):
        self._rate = rate if rate >= 0 else 1
        self.last_tick = time.perf_counter()

    @property
    def time_step(self) -> float:
        return 1 / self._rate

    def wait_next(self):
        target_tick = self.last_tick + self.time_step
        now = time.perf_counter()

        if now < target_tick:
            time_to_sleep = target_tick - now
            time.sleep(time_to_sleep)

        self.last_tick = target_tick

    def loop(self, max_ticks: Optional[int] = None) -> Generator[int, None, None]:
        ticks = 0
        while max_ticks is None or ticks < max_ticks:
            self.wait_next()
            yield ticks
            ticks += 1


class App:
    def __init__(
        self,
        sender: BaseSender,
        generator: DmxDataGenerator,
        channels: int,
        fps: int,
        max_packets: Optional[int] = None,
    ):
        self.sender = sender
        self.generator = generator
        self.channels = channels
        self.fps = fps
        self.max_packets = max_packets
        self.throttle = Throttle(fps)

        self.table_logger = TableLogger(channels)
        self.progress_bar = ProgressBar(max_packets)

    def purge_output(self):
        with self.sender:
            for _ in range(5):
                self.sender.send([0 for _ in range(self.channels)])

    def run(
        self,
        feedback: Optional[Feedback] = None,
        dry=False,
    ):
        with self.sender:
            t_start = time.time()
            for i in self.throttle.loop(self.max_packets):
                payload = next(self.generator)

                if not dry:
                    self.sender.send(payload)

                if feedback == Feedback.TABULAR:
                    self.table_logger.report(i + 1, payload)

                elif feedback == Feedback.PROGRESS_BAR:
                    self.progress_bar.report(i + 1, time.time() - t_start)
