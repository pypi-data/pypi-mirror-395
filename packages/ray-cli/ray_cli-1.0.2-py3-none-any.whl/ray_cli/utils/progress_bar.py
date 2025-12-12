from typing import Optional


class FiniteProgressBar:
    def __init__(self, total: int):
        self.total = total

    @staticmethod
    def template() -> str:
        return "{perc:>4.0%} |{bar:.<50s}| packet: {count} of {total} in {time:.2f}s"

    def report(
        self,
        count: int,
        elapsed_time: float,
    ):
        template = self.template()

        progress = template.format(
            perc=count / self.total,
            count=count,
            total=self.total,
            bar="#" * round(50 * count / self.total),
            time=elapsed_time,
        )

        print(progress, end="\n" if count == self.total else "\r")


class InfiniteProgressBar:
    @staticmethod
    def template() -> str:
        return "packet: {count} in {time:.2f}s"

    @classmethod
    def report(
        cls,
        count: int,
        elapsed_time: float,
    ):
        template = cls.template()

        progress = template.format(
            count=count + 1,
            time=elapsed_time,
        )

        print(progress, end="\r")


class ProgressBar:
    def __init__(
        self,
        total: Optional[int] = None,
    ):
        self.progress_bar = (
            InfiniteProgressBar() if total is None else FiniteProgressBar(total)
        )

    def report(
        self,
        count: int,
        elapsed_time: float,
    ):
        self.progress_bar.report(count, elapsed_time)
