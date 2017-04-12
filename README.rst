Cloudmesh cmd5
==============

An dynamically extensible CMD based command shell

Requirements
------------

* Python 2.7.13

Installation from source
------------------------

Setup a virtualenv either with virtualenv or pyenv.

virtualenv::

    virtualenv ~/ENV2

pyenv::

    pyenev virtualenv 2.7.13 ENV2

Now you need to get two source directories. We assume yo place them in
~/github::

    mkdir ~/github
    cd ~/github
    git clone https://github.com/cloudmesh/cloudmesh.common.git
    git clone https://github.com/cloudmesh/cloudmesh.cmd5.git
    git clone https://github.com/cloudmesh/cloudmesh.bar.git

The cmd5 repository contains the shell, while the extbar directory
contains the sample commands foo and bar. The common library contains
some useful classes and methods that we also share with other
cloudmesh code.

To install them from source simply to the following. The cloudmesh.bar
example you want as source as you want to modify the code at one point::

    cd ~/github/cloudmesh.common
    python setup.py install
    pip install .
    cd ~/github/cloudmesh.cmd5
    python setup.py install
    pip install .
    cd ~/github/cloudmesh.bar
    python setup.py install
    pip install .

Instalation from pip
--------------------

To install cmd5 from pip please use::

  pip install cloudmesh.cmd5

The cloudmesh.bar repository you want to download as source so you can
learn how to write your own commands::

  mkdir ~/github
  cd ~/github
  git clone https://github.com/cloudmesh/cloudmesh.bar.git

Commands are shared in the `cloudmesh` namespace::

Execution
---------

to run the shell you can activate it with the cms command. cms stands
for cloudmesh shell::

    (ENV2) $ cms

It will print the banner and enter the shell::

    +-------------------------------------------------------+
    |   ____ _                 _                     _      |
    |  / ___| | ___  _   _  __| |_ __ ___   ___  ___| |__   |
    | | |   | |/ _ \| | | |/ _` | '_ ` _ \ / _ \/ __| '_ \  |
    | | |___| | (_) | |_| | (_| | | | | | |  __/\__ \ | | | |
    |  \____|_|\___/ \__,_|\__,_|_| |_| |_|\___||___/_| |_| |
    +-------------------------------------------------------+
    |                  Cloudmesh CMD5 Shell                 |
    +-------------------------------------------------------+

    cms>


To see the list of commands you can say::

    cms> help

To see the manula page for a specific command, please use::

    help COMMANDNAME

Extension
---------

One of the most important features of CMD5 is its ability to extend it
with new commands.  This is done via packaged name spaces. This is
defined in the setup.py file of your enhancement. The best way to
create an enhancement is to take a look at the code in

* https://github.com/cloudmesh/cloudmesh.bar.git

Simply copy the code and modify the bar and foo commands to fit yor
needs. 

*Wraning:* do not copy the .git directory

It is important that all objects are defined in the command
itself and that no global variables be use in order to allow each
shell command to stand alone. Naturally you should develop API
libraries outside of the cloudmesh shell command and reuse them in
order to keep the command code as small as possible. We place the
command in::

    cloudmsesh/COMMANDNAME/command/COMMANDNAME.py

An example for the bar command is presented at:

* https://github.com/cloudmesh/cloudmesh.bar/blob/master/cloudmesh/bar/command/bar.py

It shows how simple the command definition is (bar.py)::

    from __future__ import print_function
    from cloudmesh.shell.command import command
    from cloudmesh.shell.command import PluginCommand

    class BarCommand(PluginCommand):

        @command
        def do_bar(self, args, arguments):
            """
            ::
	       
              Usage:
                    command -f FILE
                    command FILE
                    command list
              This command does some useful things.
              Arguments:
                  FILE   a file name
              Options:
                  -f      specify the file
            """
            print(arguments)

An important difference to other CMD solutions is that our commands
can leverage (besides the standrad definition), docopts as a way to
define the manual page. This allows us to use arguments as dict and
use simple if conditions to interpret the command. Using docopts has
the advantage that contributors are forced to think about the command
and its options and document them from the start. Previously we used
not to use docopts and argparse was used. However we noticed that for
some contributions the lead to commands that were either not properly
documented or the developers delivered ambiguous commands that
resulted in confusion and wrong ussage by the users. Hence, we do
recommend that you use docopts.

The transformation is enabled by the @command decorator that takes
also the manual page and creates a proper help message for the shell
automatically. Thus there is no need to introduce a sepaarte help
method as would normally be needed in CMD.


