import os
import sys
import time
from builtins import input

from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.console import Console
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.common.variables import Variables
from cloudmesh.common.Shell import Shell


class TerminalCommand(PluginCommand):
    from cloudmesh.common.variables import Variables
    from cloudmesh.shell.command import PluginCommand
    from cloudmesh.shell.command import command

    # noinspection PyUnusedLocal,PyIncorrectDocstring
    @command
    def do_term(self, args, arguments):
        """
        ::

          Usage:
            term COMMAND

          Arguments:
            COMMAND   The command to execute in the terminal

           Opens a new terminal and executes the command in it
           The terminal stays openafter executing it in an interctive mode
           The terminal is started in the background

        """
        Shell.terminal(arguments.COMMAND)

        return ""

    # noinspection PyUnusedLocal,PyIncorrectDocstring
    @command
    def do_banner(self, args, arguments):
        """
        ::

          Usage:
            banner [-c CHAR] [-n WIDTH] [-i INDENT] [-r COLOR] TEXT...

          Arguments:
            TEXT...   The text message from which to create the banner
            CHAR      The character for the frame.
            WIDTH     Width of the banner
            INDENT    indentation of the banner
            COLOR     the color

            Options:
                -c CHAR   The character for the frame. [default: #]
                -n WIDTH  The width of the banner. [default: 70]
                -i INDENT  The width of the banner. [default: 0]
                -r COLOR  The color of the banner. [default: NORMAL]

            Prints a banner form a one line text message.
        """
        Console.ok("banner")
        n = int(arguments['-n'])
        c = arguments['-c']
        i = int(arguments['-i'])
        color = arguments['-r'].upper()

        line = ' '.join(arguments['TEXT'])

        Console.init()
        hline = i * " " + str((n - i) * c)
        Console.cprint(color=color, prefix="", message=hline)
        Console.cprint(color=color, prefix="", message=i * " " + c + " " + line)
        Console.cprint(color=color, prefix="", message=hline)

        return ""

    # noinspection PyUnusedLocal
    @command
    def do_stopwatch(self, args, arguments):
        """
        ::

          Usage:
            stopwatch start TIMER
            stopwatch stop TIMER
            stopwatch print [TIMER]
            stopwatch benchmark
            
          Arguments:
            TIMER  the name of the timer

          Description:
            THIS IS NOT YET WORKING
            starts and stops named timers and prints them
        """
        t = arguments.TIMER
        if arguments.start:
            StopWatch.start(t)
        elif arguments.stop:
            StopWatch.stop(t)
        elif arguments.benchmark:
            StopWatch.benchmark()
        elif arguments.print:
            t = arguments.TIMER
            if t is None:
                print(StopWatch.__str__)
            else:
                StopWatch.print("Timer " + t + ":", t)

    # noinspection PyUnusedLocal
    @command
    def do_clear(self, args, arguments):
        """
        ::

          Usage:
            clear



          Clears the screen."""

        sys.stdout.write(os.popen('clear').read())

    # noinspection PyUnusedLocal
    @command
    def do_sleep(self, args, arguments):
        """
        ::

          Usage:
            sleep SECONDS

          Clears the screen."""

        seconds = arguments["SECONDS"]
        time.sleep(float(seconds))

    # noinspection PyUnusedLocal
    @command
    def do_echo(self, args, arguments):
        """
        ::

          Usage:
            echo  [-r COLOR] TEXT

            Arguments:
                TEXT   The text message to print
                COLOR  the color

            Options:
                -r COLOR  The color of the text. [default: NORMAL]

            Prints a text in the given color
        """
        color = arguments["-r"] or "normal"
        color = color.upper()
        text = arguments["TEXT"]
        if color == "NORMAL":
            Console.msg(text)
        else:
            Console.cprint(color=color, prefix="", message=text)

        return ""

    @command
    def do_pause(self, arg, arguments):
        """
        ::

          Usage:
            pause [MESSAGE]

          Arguments:
            MESSAGE  message to be displayed

          Description:
            Displays the specified text then waits for the user to press RETURN.

        """

        if arguments["MESSAGE"] is None:
            arg = 'Press ENTER to continue'
        input(arg + '\n')

        return ""

    #
    # Echo
    #
    def set_verbose(self, on):
        # self.echo = on
        pass

    # noinspection PyAttributeOutsideInit
    def set_banner(self, banner):
        self.banner = banner

    # @command
    # def do_loglevel(self, args, arguments):
    #     """
    #     ::
    #
    #       Usage:
    #           loglevel
    #           loglevel critical
    #           loglevel error
    #           loglevel warning
    #           loglevel info
    #           loglevel debug
    #
    #           Shows current log level or changes it.
    #
    #           loglevel - shows current log level
    #           critical - shows log message in critical level
    #           error    - shows log message in error level including critical
    #           warning  - shows log message in warning level including error
    #           info     - shows log message in info level including warning
    #           debug    - shows log message in debug level including info
    #
    #       NOTE:
    #         NOT YET IMPLEMENTED
    #     """
    #
    #
    #     if arguments['debug']:
    #         self.loglevel = "DEBUG"
    #     elif arguments['error']:
    #         self.loglevel = "ERROR"
    #     elif arguments['warning']:
    #         self.loglevel = "WARNING"
    #     elif arguments['info']:
    #         self.loglevel = "INFO"
    #     elif arguments['critical']:
    #         self.loglevel = "CRITICAL"
    #     else:
    #         Console.ok("Log level: {0}".format(self.loglevel))
    #         return ""
    #     Console.ok ("Log level: {0} is set".format(self.loglevel))
    #
    #     config = Config()
    #     config["cloudmesh.logging.level"] = self.loglevel
    #     config.write("aaa.yaml")
    #     #config.write(filename=filename,
    #                   output="yaml",
    #                   attribute_indent="    ")
    #     return ""

    '''
    @command
    def do_verbose(self, args, arguments):
        """
        Usage:
            verbose (True | False)
            verbose

        NOTE: NOT YET IMPLEMENTED.
        If it sets to True, a command will be printed before execution.
        In the interactive mode, you may want to set it to False.
        When you use scripts, we recommend to set it to True.

        The default is set to False

        If verbose is specified without parameter the flag is
        toggled.

        """
        # if args == '':
        #    self.echo = not self.echo
        # else:
        #    self.echo = arguments['True']

        Console.error("verbose NOT YET IMPLEMENTED")

        return ""
        '''
