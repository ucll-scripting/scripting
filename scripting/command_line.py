import argparse
import sys
import os
import types
from scripting.version import __version__
from scripting.fileutils import find_files_recursively, has_name, execute_code, inside_directory
from scripting.scoring import Score, keep_score
from scripting.counting import keep_counts
from scripting.tested import tested_file



def _version_command(args):
    '''
    Runs when using version command
    '''
    print(__version__)


def _test_command(args):
    '''
    Runs when using test command
    '''
    with keep_score() as current_score, keep_counts() as current_counts:
        for filename in find_files_recursively(predicate=has_name(args.tests_file)):
            with inside_directory(os.path.dirname(filename)), tested_file(args.tested_file):
                execute_code(filename)

        score = current_score()
        counts = current_counts()

    print(score)
    print(counts)


def create_command_line_arguments_parser():
    '''
    Creates parsers and subparsers
    '''
    # Top level parser
    parser = argparse.ArgumentParser(prog='scripting')
    parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers(help='sub-command help')

    # Version command parser
    test_parser = subparsers.add_parser('version', help='returns version')
    test_parser.set_defaults(func=_version_command)

    # Test command parser
    test_parser = subparsers.add_parser('test', help='runs tests in all subdirectories')
    test_parser.add_argument('--tested-file', help='File where tested code resides (default: student.py)', default='student.py')
    test_parser.add_argument('--tests-file', help='File where tests resides (default: tests.py)', default='tests.py')
    test_parser.set_defaults(func=_test_command)

    return parser


def shell_entry_point():
    '''
    Called from shell using 'scripting' command
    '''
    parser = create_command_line_arguments_parser()
    args = parser.parse_args(sys.argv[1:])

    args.func(args)
