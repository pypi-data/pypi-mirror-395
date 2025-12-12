import argparse


class CustomHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def __init__(self, *args, **kwargs):
        kwargs["max_help_position"] = 45
        kwargs["width"] = 120
        super().__init__(*args, **kwargs)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super()._format_action_invocation(action)
        options = ", ".join(action.option_strings)
        if action.nargs == 0:
            return options
        return f"{options} {self._format_args(action, action.dest.upper())}"

    def _get_help_string(self, action):
        return action.help
