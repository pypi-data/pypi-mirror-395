from typing import Sequence

from .sender import BaseSender, Sender


class SenderPool(BaseSender):
    def __init__(
        self,
        senders: Sequence[Sender],
    ):
        self.senders = senders

    def open(self):
        for s in self.senders:
            s.open()

    def close(self):
        for s in self.senders:
            s.close()

    def send(self, dmx_data: Sequence[int]):
        for s in self.senders:
            s.send(dmx_data)
