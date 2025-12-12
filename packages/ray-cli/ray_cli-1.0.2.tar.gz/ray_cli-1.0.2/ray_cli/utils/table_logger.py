class TableLogger:
    def __init__(
        self,
        channels: int,
    ):
        self.table = []
        self.channels = channels

    def report(self, frame_count, payload):
        if not self.table:
            row = self.format_table_head(self.channels)
            self.table.append(row)
            print(row)

        row = self.format_table_row(frame_count, payload)
        self.table.append(row)
        print(row)

    @staticmethod
    def template() -> str:
        return "{a:^6s}|{b:<10s}"

    @classmethod
    def format_table_head(cls, channels) -> str:
        padding = 6
        width = padding + 1 + padding * channels

        columns = ""
        for i in range(channels):
            columns += f"{'C' + str(i + 1):>5s} "

        row = cls.template().format(
            a="FRAME",
            b=columns,
        )

        return row + "\n" + ("-" * width)

    @classmethod
    def format_table_row(cls, frame_count, payload) -> str:
        payload_str = ""

        for item in payload:
            payload_str += f"{item:>5n} "

        return cls.template().format(
            a=str(frame_count),
            b=payload_str,
        )
