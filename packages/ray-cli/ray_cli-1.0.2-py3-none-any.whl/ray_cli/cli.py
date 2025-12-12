import argparse
import importlib.metadata
import ipaddress
import sys
from dataclasses import dataclass

from ray_cli.core import Sender, SenderPool
from ray_cli.modes import Mode, generator_factory
from ray_cli.protocols import ArtNetFactory, ArtNetUniverse, SACNFactory
from ray_cli.utils import (
    Cli,
    Command,
    CommandGroup,
    Feedback,
    Group,
    MutualExclusiveGroup,
    Option,
    generate_settings_report,
)

from .__version__ import __version__
from .app import App

PACKAGE_NAME = importlib.metadata.metadata("ray-cli")["Name"]
PACKAGE_SUMMARY = importlib.metadata.metadata("ray-cli")["Summary"]


@dataclass(frozen=True)
class Limits:
    channels = (1, 512)
    intensity = (1, 255)
    intensity_min = (0, 254)
    frequency = (0.001, None)
    workers = (1, 100)
    packets = (1, None)
    duration = (0.001, None)
    fps = (0.001, None)
    sacn_universes = (1, 63999)
    artnet_universes = (ArtNetUniverse(0, 0, 0), ArtNetUniverse(15, 15, 127))
    sacn_priority = (0, 200)


def print_report(args):
    title = f"{PACKAGE_NAME} {__version__}"
    body = generate_settings_report(
        args=args,
        max_channels=Limits.channels[-1],
        max_priority=Limits.sacn_priority[-1],
        max_intensity=Limits.intensity[-1],
        max_workers=Limits.workers[-1],
    )
    print(f"\n{title}\n\n{body}\n")


def sacn_sender_pool_factory(args: argparse.Namespace) -> SenderPool:
    def generate_source_name(w):
        return f"{PACKAGE_NAME} {__version__}" + (
            f" [worker:{w}]" if args.workers > 1 else ""
        )

    return SenderPool(
        senders=[
            Sender(
                universes=args.universes,
                factory=SACNFactory(
                    source_name=generate_source_name(w),
                    priority=args.priority,
                ),
                src=args.src,
                dst=args.dst,
            )
            for w in range(args.workers)
        ]
    )


def artnet_sender_poll_factory(args: argparse.Namespace) -> SenderPool:
    return SenderPool(
        senders=[
            Sender(
                universes=args.universes,
                factory=ArtNetFactory(physical=w),
                src=args.src,
                dst=args.dst,
            )
            for w in range(args.workers)
        ]
    )


def app_factory(args: argparse.Namespace):
    generator = generator_factory(
        mode=args.mode,
        channels=args.channels,
        fps=args.fps,
        frequency=args.frequency,
        intensity_upper=args.intensity,
        intensity_lower=args.intensity_min,
    )

    return App(
        generator=generator,
        sender=args.callback(args),
        channels=args.channels,
        fps=args.fps,
        max_packets=(
            args.packets
            if args.packets is not None
            else args.fps * args.duration
            if args.duration
            else None
        ),
    )


def select_feedback(args: argparse.Namespace):
    if args.quiet:
        return None
    if args.verbose or args.dry:
        return Feedback.TABULAR
    return Feedback.PROGRESS_BAR


dmx_group = Group(
    options=[
        Option(
            ("-m", "--mode"),
            type=Mode,
            default=Mode.RAMP,
            choices=list(Mode),
            metavar="MODE",
            help="DMX signal shape mode",
        ),
        Option(
            ("-c", "--channels"),
            default=24,
            type=int,
            help="DMX channels at universe to send to",
            bounds=Limits.channels,
        ),
        Option(
            ("-i", "--intensity"),
            default=10,
            type=int,
            help="DMX channels output intensity",
            bounds=Limits.intensity,
        ),
        Option(
            ("-I", "--intensity-min"),
            default=0,
            type=int,
            help="DMX channels minimum output intensity",
            bounds=Limits.intensity_min,
        ),
        Option(
            ("-f", "--frequency"),
            default=1.0,
            type=float,
            help="frequency of the generated signal",
            bounds=Limits.frequency,
        ),
    ],
)

network_group = Group(
    name="network group",
    options=[
        Option(
            ("--src",),
            type=ipaddress.IPv4Address,
            default=ipaddress.IPv4Address("0.0.0.0"),
            help="IP address of the DMX source",
        ),
        Option(
            ("--dst",),
            type=ipaddress.IPv4Address,
            default=None,
            help="IP address of the DMX destination (default: MULTICAST)",
        ),
    ],
)

runtime_group = Group(
    name="runtime group",
    options=[
        Option(
            ("-w", "--workers"),
            default=1,
            type=int,
            help="number of sender workers per universe",
            bounds=Limits.workers,
        ),
        MutualExclusiveGroup(
            options=[
                Option(
                    ("-P", "--packets"),
                    default=None,
                    type=int,
                    help="number of packets to send per universe per worker",
                    bounds=Limits.packets,
                ),
                Option(
                    ("-d", "--duration"),
                    default=None,
                    type=float,
                    help="broadcast duration in seconds",
                    bounds=Limits.duration,
                ),
            ],
        ),
        Option(
            ("--fps",),
            default=10,
            type=float,
            help="frames per second per universe",
            bounds=Limits.fps,
        ),
    ],
)

display_group = MutualExclusiveGroup(
    name="display options",
    options=[
        Option(
            ("-v", "--verbose"),
            action="store_true",
            help="run in verbose mode",
        ),
        Option(
            ("-q", "--quiet"),
            action="store_true",
            help="run in quiet mode",
        ),
    ],
)

operational_group = Group(
    name="operational options",
    options=[
        Option(
            ("--dry",),
            action="store_true",
            help="simulate outputs without broadcast",
        ),
        Option(
            ("--purge",),
            action="store_true",
            help="send zero-data on all channels and exit",
        ),
        Option(
            ("--purge-on-exit",),
            action="store_true",
            help="send zero-data on all channels upon completion",
        ),
    ],
)

query_group = Group(
    name="query options",
    options=[
        Option(
            ("-h", "--help"),
            action="help",
            help="print help and exit",
        ),
        Option(
            ("-V", "--version"),
            action="version",
            version=f"%(prog)s {__version__}",
            help="show program's version number and exit",
        ),
    ],
)

sacn_group = Group(
    options=[
        Option(
            ("-u", "--universes"),
            default=[1],
            nargs="+",
            type=int,
            help="sACN universe(s) to send to",
            bounds=Limits.sacn_universes,
        ),
        Option(
            ("-p", "--priority"),
            default=100,
            type=int,
            help="DMX source priority",
            bounds=Limits.sacn_priority,
        ),
    ]
)

artnet_group = Group(
    options=[
        Option(
            ("-u", "--universes"),
            default=[ArtNetUniverse(net=0, sub_net=0, uni=1)],
            nargs="+",
            type=ArtNetUniverse.from_str,
            help="Art-Net universe(s) to send to",
            bounds=Limits.artnet_universes,
        ),
    ],
)

shared_opts = [
    network_group,
    runtime_group,
    display_group,
    operational_group,
    query_group,
]

cli = Cli(
    prog=PACKAGE_NAME,
    description=PACKAGE_SUMMARY,
    add_help=False,
    options=shared_opts,
    command_groups=[
        CommandGroup(
            dest="command",
            required=True,
            metavar="PROTOCOL",
            commands=[
                Command(
                    "sacn",
                    help="Send DMX using sACN (E1.31)",
                    add_help=False,
                    options=[dmx_group, sacn_group] + shared_opts,
                    callback=sacn_sender_pool_factory,
                ),
                Command(
                    "artnet",
                    help="Send DMX using Art-Net 4",
                    add_help=False,
                    options=[dmx_group, artnet_group] + shared_opts,
                    callback=artnet_sender_poll_factory,
                ),
            ],
        )
    ],
)


def main(args=None):
    try:
        args = cli.parse_args(args)

        feedback = select_feedback(args)

        if not args.quiet and not args.purge:
            print_report(args)

        app = app_factory(args)

        if args.purge:
            app.purge_output()
            return

        app.run(feedback, args.dry)

        if args.purge_on_exit:
            app.purge_output()

        if not args.quiet:
            print("\nDone!")

    except KeyboardInterrupt:
        print("\nCancelling...")
        sys.exit(1)

    except Exception as exc:
        print(f"Failed with error: {exc}")
        sys.exit(1)

    else:
        sys.exit(0)
