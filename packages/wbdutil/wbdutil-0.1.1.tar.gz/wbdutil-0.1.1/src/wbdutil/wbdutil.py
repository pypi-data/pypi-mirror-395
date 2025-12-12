import sys
from collections import OrderedDict

from knack import CLI, ArgumentsContext
from knack.commands import CLICommandsLoader, CommandGroup
from knack.help import CLIHelp

from . import __VERSION__, CLI_NAME, MODULE_NAME

OSDU_MESSAGE = r"""
 ___  ___  ___  _ _
| . |/ __]| . \| | |
| | |\__ \| | || | |
`___'[___/|___/ \__|
Welcome to the DDMS command line data loader!"""

BASE_MESSAGE = f"{OSDU_MESSAGE}\nVersion {__VERSION__}\n\nUsage:\n  {CLI_NAME} [command]\n\nAvailable Commands:"


class CommandHelp(CLIHelp):
    """OSDU DDMS CLI loader help"""

    def __init__(self, cli_ctx=None):
        super(CommandHelp, self).__init__(cli_ctx=cli_ctx, welcome_message=BASE_MESSAGE)


class DdmsCommandLoader(CLICommandsLoader):
    """ Implementation of CLICommandsLoader for the DDMS data loader CLI """

    def __init__(self, *args, **kwargs):
        super(DdmsCommandLoader, self).__init__(
            *args,
            excluded_command_handler_args=[],
            **kwargs)

    def load_command_table(self, args):
        """Load all commands"""

        with CommandGroup(self, 'parse', MODULE_NAME + '.commands.parse#{}') as group:
            group.command('convert', 'convert')
            group.command('print', 'printlas')

        with CommandGroup(self, 'ingest', MODULE_NAME + '.commands.ingest#{}') as group:
            group.command('wellbore', 'wellbore')
            group.command('data', 'welllog_data')

        with CommandGroup(self, 'list', MODULE_NAME + '.commands.list_osdu#{}') as group:
            group.command('wellbore', 'wellbore')
            group.command('welllog', 'welllog')
            group.command('curves', 'welllog_data')

        with CommandGroup(self, 'update', MODULE_NAME + '.commands.update#{}') as group:
            group.command('welllog', 'welllog')

        with CommandGroup(self, 'search', MODULE_NAME + '.commands.search#{}') as group:
            group.command('wellbore', 'wellbore_search')

        with CommandGroup(self, 'download', MODULE_NAME + '.commands.download#{}') as group:
            group.command('welllog', 'download_las')

        return OrderedDict(self.command_table)

    def load_arguments(self, command):
        """Load arguments for commands"""

        with ArgumentsContext(self, '') as arg_context:
            arg_context.argument('config_path', type=str, options_list=('-c', '--config_path'),
                                 help='''The path and filename of the configuration file.
                                  Defaults to \'CONFIGPATH\' environment variable if not set.''')

        # 'parse'
        with ArgumentsContext(self, 'parse') as arg_context:
            self._register_input_path_argument(arg_context)

        with ArgumentsContext(self, 'parse convert') as arg_context:
            self._register_wellbore_id_flag(arg_context)

        # 'ingest'
        with ArgumentsContext(self, 'ingest') as arg_context:
            self._register_input_path_argument(arg_context)
            self._register_token_argument(arg_context)

        with ArgumentsContext(self, 'ingest wellbore') as arg_context:
            arg_context.argument('no_recognize', options_list=('--norecognize'), action='store_true',
                                 help='If specified the application won\'t attempt to recognize the curve families.')

        with ArgumentsContext(self, 'ingest data') as arg_context:
            self._register_welllog_id_argument(arg_context)

        # 'list'
        with ArgumentsContext(self, 'list') as arg_context:
            self._register_token_argument(arg_context)

        with ArgumentsContext(self, 'list wellbore') as arg_context:
            self._register_wellbore_id_flag(arg_context)

        with ArgumentsContext(self, 'list welllog') as arg_context:
            self._register_welllog_id_argument(arg_context)
            arg_context.argument('curves', options_list=('--curveids'), action='store_true',
                                 help='Show only the curve ids.')

        with ArgumentsContext(self, 'list curves') as arg_context:
            self._register_welllog_id_argument(arg_context)
            self._register_curves_argument(arg_context)

        # 'update'
        with ArgumentsContext(self, 'update') as arg_context:
            self._register_token_argument(arg_context)

        with ArgumentsContext(self, 'update welllog') as arg_context:
            self._register_welllog_id_argument(arg_context)
            arg_context.argument('recognize', options_list=('--recognize'), action='store_true',
                                 help='If present or set to True the application will attempt to recognize and update the curve families.')

        # 'Search'
        with ArgumentsContext(self, 'search') as arg_context:
            self._register_token_argument(arg_context)

        with ArgumentsContext(self, 'search wellbore') as arg_context:
            arg_context.argument('wellbore_name', type=str, options_list=('--name'),
                                 help='The facility name of wellbore ids to retrieve.')

        # 'download'
        with ArgumentsContext(self, 'download') as arg_context:
            self._register_token_argument(arg_context)
            self._register_welllog_id_argument(arg_context)
            self._register_curves_argument(arg_context)
            arg_context.argument('outfile', type=str, options_list=('--out'),
                                 help='The output file path')

        super(DdmsCommandLoader, self).load_arguments(command)

    def _register_input_path_argument(self, arg_context):
        arg_context.argument('input_path', type=str, options_list=('-p', '--path'),
                             help='Path to a file or folder containing one or more LAS file(s).')

    def _register_curves_argument(self, arg_context):
        arg_context.argument('curves', type=str, options_list=('--curves'), nargs='*',
                             help='The list of curves to retrieve (space separated list), returns all curves if not specified.')

    def _register_wellbore_id_flag(self, arg_context):
        arg_context.argument('wellbore_id', type=str, options_list=('--wellbore_id'),
                             help='The wellbore id of the record.')

    def _register_welllog_id_argument(self, arg_context):
        arg_context.argument('welllog_id', type=str, options_list=('--welllog_id'),
                             help='The welllog id of the record.')

    def _register_token_argument(self, arg_context):
        arg_context.argument('token', type=str, options_list=('-t', '--token'),
                             help='''A valid bearer token used to authenticate with the OSDU instance.
                              Defaults to \'OSDUTOKEN\' environment variable if not set.''')


def main():
    """Main entry point for the command line interface"""
    try:
        args_list = sys.argv[1:]

        ddmscli = CLI(cli_name=CLI_NAME,
                      commands_loader_cls=DdmsCommandLoader,
                      help_cls=CommandHelp)

        exit_code = ddmscli.invoke(args_list)
        sys.exit(exit_code)

    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
