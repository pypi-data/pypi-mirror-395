import argparse
from dataclasses import dataclass, field, fields
from typing import Any, Callable, Optional, Sequence, Tuple, Type, Union

from .formatters import CustomHelpFormatter

ARGPARSE_META = {"argparse": True}

ParserLike = Union[
    argparse.ArgumentParser,
    argparse._ArgumentGroup,
    argparse._MutuallyExclusiveGroup,
]

SubparsersLike = argparse._SubParsersAction


def arg_field(*, default: Any = None) -> Any:
    return field(default=default, metadata=ARGPARSE_META)


def bounded(
    converter: Callable[[str], Any],
    *,
    lower: Optional[float] = None,
    upper: Optional[float] = None,
    label: Optional[str] = None,
) -> Callable[[str], Any]:
    def validate(token: str):
        try:
            value = converter(token)
        except Exception as exc:
            raise argparse.ArgumentTypeError(
                f"{label or 'value'} invalid: {token}"
            ) from exc

        if isinstance(value, (int, float)):
            if lower is not None and value < lower:
                raise argparse.ArgumentTypeError(
                    f"{label or 'value'} must be ≥ {lower}"
                )
            if upper is not None and value > upper:
                raise argparse.ArgumentTypeError(
                    f"{label or 'value'} must be <= {upper}"
                )
        return value

    return validate


@dataclass
class BaseCli:
    @property
    def kwargs(self):
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if f.metadata.get("argparse") and getattr(self, f.name) is not None
        }


@dataclass
class Option(BaseCli):
    name_or_flags: Sequence[str]

    default: Any = arg_field()
    type: Optional[Any] = arg_field()
    choices: Optional[Sequence[str]] = arg_field()
    action: Optional[Any] = arg_field()
    nargs: Optional[Any] = arg_field()
    metavar: Optional[str] = arg_field()
    dest: Optional[str] = arg_field()
    required: Optional[bool] = arg_field()
    const: Optional[Any] = arg_field()
    version: Optional[Any] = arg_field()
    help: str = arg_field(default="")

    bounds: Optional[Tuple[Any, Any]] = None

    def register(self, parser: ParserLike):
        kwargs = self.kwargs

        kwargs["help"] = self._generate_help()

        if self.bounds and self.type and not self.action:
            lo, hi = self.bounds
            kwargs["type"] = bounded(
                self.type,
                lower=lo,
                upper=hi,
                label=self.name_or_flags[-1],
            )

        parser.add_argument(*self.name_or_flags, **kwargs)

    def _generate_help(self) -> str:
        parts = []

        if self.bounds is not None:
            parts.append(f"range: {self.bounds[0]}-{self.bounds[1] or 'unlimited'}")

        if self.choices is not None:
            parts.append(f"choices: {', '.join(map(str, self.choices))}")

        if self.default is not None:
            parts.append("default: %(default)s")

        extra = f" ({', '.join(parts)})" if parts else ""

        return f"{self.help}{extra}".strip()


@dataclass
class MutualExclusiveGroup(BaseCli):
    name: Optional[str] = None
    options: Sequence[Option] = field(default_factory=tuple)
    required: bool = False

    def register(self, parser: ParserLike):
        target = parser.add_argument_group(self.name) if self.name else parser
        mx = target.add_mutually_exclusive_group(required=self.required)
        for opt in self.options:
            opt.register(mx)


@dataclass
class Group(BaseCli):
    name: Optional[str] = None
    options: Sequence[Union[Option, MutualExclusiveGroup]] = field(
        default_factory=tuple
    )

    def register(self, parser: ParserLike):
        target = parser.add_argument_group(self.name) if self.name else parser
        for opt in self.options:
            opt.register(target)


@dataclass
class Command(BaseCli):
    name: str = arg_field(default="")
    help: str = arg_field(default="")
    add_help: Optional[bool] = arg_field(default=False)
    formatter_class: Optional[Type[argparse.HelpFormatter]] = arg_field(
        default=CustomHelpFormatter
    )

    options: Sequence[Union[Option, Group]] = field(default_factory=tuple)
    callback: Optional[Callable] = None

    def register(self, subparser: SubparsersLike):
        parser = subparser.add_parser(**self.kwargs)
        for opt in self.options:
            opt.register(parser)
        if self.callback is not None:
            parser.set_defaults(callback=self.callback)


@dataclass
class CommandGroup(BaseCli):
    dest: Optional[str] = arg_field()
    required: Optional[bool] = arg_field()
    metavar: Optional[str] = arg_field()

    commands: Sequence[Command] = field(default_factory=tuple)

    def register(self, parser: argparse.ArgumentParser):
        subparsers = parser.add_subparsers(**self.kwargs)
        for command in self.commands:
            command.register(subparsers)


@dataclass
class Cli(BaseCli):
    prog: str = arg_field(default="")
    description: str = arg_field(default="")
    add_help: bool = arg_field(default=True)
    formatter_class: Optional[Type[argparse.HelpFormatter]] = arg_field(
        default=CustomHelpFormatter
    )
    options: Sequence[Union[Option, Group, MutualExclusiveGroup]] = field(
        default_factory=tuple
    )
    command_groups: Sequence[CommandGroup] = field(default_factory=tuple)

    def parse_args(self, args=None) -> argparse.Namespace:
        parser = argparse.ArgumentParser(**self.kwargs)

        for opt in self.options:
            opt.register(parser)

        for group in self.command_groups:
            group.register(parser)

        return parser.parse_args(args)
