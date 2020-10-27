# Cloudmesh cmd5

[![DOI](https://zenodo.org/badge/82920490.svg)](https://zenodo.org/badge/latestdoi/82920490)


[![image](https://img.shields.io/pypi/v/cloudmesh-cmd5.svg)](https://pypi.org/project/cloudmesh-cmd5/)
[![Python](https://img.shields.io/pypi/pyversions/cloudmesh-cmd5.svg)](https://pypi.python.org/pypi/cloudmesh-cmd5)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/cloudmesh/cloudmesh-cmd5/blob/main/LICENSE)
[![Format](https://img.shields.io/pypi/format/cloudmesh-cmd5.svg)](https://pypi.python.org/pypi/cloudmesh-cmd5)
[![Status](https://img.shields.io/pypi/status/cloudmesh-cmd5.svg)](https://pypi.python.org/pypi/cloudmesh-cmd5)
[![Travis](https://travis-ci.com/cloudmesh/cloudmesh-cmd5.svg?branch=main)](https://travis-ci.com/cloudmesh/cloudmesh-cmd5)




## Installation and Documentation

Please note that several packages are available which are pointed to in the
installation documentation.

|  | Links |
|---------------|-------|
| Documentation | <https://cloudmesh.github.io/cloudmesh-cloud> |
| Code | <https://github.com/cloudmesh/cloudmesh-cloud> |
| Installation Instructions | <https://github.com/cloudmesh/get> |

An dynamically extensible CMD based command shell. For en extensive
documentation please see

* <https://github.com/cloudmesh-community/book/blob/main/vonLaszewski-cloud.epub?raw=true>

where we also document how to use pyenv virtualenv.

## Requirements

* Python greater equal 3.8.1

Cloudmesh was able to run on earlier versions of python, but we do prefer to
test it on the newest version.

We recommend that you use venv first before you install cloudmesh. This

You can as user install cmd5 with


```bash
pip install cloudemsh-cmd5
```

Developers should look at our cloudmesh manual.

* <https://cloudmesh.github.io/cloudmesh-manual/>

## CMD5 Shell and Commandline


to run the shell you can activate it with the cms command. cms stands
for cloudmesh shell::

```bash
$ cms
```

It will print the banner and enter the shell::

```
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
```

To see the list of commands you can say::

```
cms> help
```

```bash
Documented commands (type help <topic>):
========================================
EOF     commands  default  help  pause   q     shell      sys   version
banner  config    echo     info  plugin  quit  sleep      test
clear   debug     gui      man   py      set   stopwatch  var 
```

To see the manual page for a specific command, please use::

```
cms> help COMMANDNAME
```

A full manual page is available at

* <https://cloudmesh.github.io/cloudmesh-manual/>

## CMD 5 Plugin Mechanism

Cmd5 comes with a sophisticated plugin mechanism. Commands can be readily
designed from the sys command.

The sys command can be installed either from source (as discussed previously) or
via pip

```bash
$ pip install cloudmesh-sys
```

Once you have installed it, execute `cms help sys` to see the usage. Now you
simply can in a new directory execute the sys command as follows, where
`mycommnad` is than name of the command you like to implement.

```bash
$ mkdir mycommand
$ cd mycommand
$ cms sys command generate mycommand .
```

A directory with the name `cloudmesh-mycommand` will be generated that contains
the template for the command. You can enter this template and modify the
implementation in the folders `cloudmesh/mycommand/api` and
`cloudmesh/mycommand/command` when installing it with

```
$ pip install .
```

The command will be added to the cms command>

An example for the bar command is presented at:

* [cloudmesh/bar/command/bar.py](https://github.com/cloudmesh/cloudmesh.bar/blob/main/cloudmesh/bar/command/bar.py)

It shows how simple the command definition is (bar.py)::

```bash
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
```

An important difference to other CMD solutions is that our commands
can leverage (besides the standard definition), docopts as a way to
define the manual page. This allows us to use arguments as dict and
use simple if conditions to interpret the command. Using docopts has
the advantage that contributors are forced to think about the command
and its options and document them from the start. Previously we used
not to use docopts and argparse was used. However we noticed that for
some contributions the lead to commands that were either not properly
documented or the developers delivered ambiguous commands that
resulted in confusion and wrong usage by the users. Hence, we do
recommend that you use docopts.

The transformation is enabled by the `@command` decorator that takes
also the manual page and creates a proper help message for the shell
automatically. Thus there is no need to introduce a separate help
method as would normally be needed in CMD.

## Features

The following highlighted features are available:

* easy command integration through separate modules
* multi cloud environments (under development) though cloudmesh-cloud plugin
* openapi integration through cloudmesh-openapi plugin
* general commands as documented at in the

  [manual](https://cloudmesh.github.io/cloudmesh-manual/) such as
  [admin](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/admin.html),
  [banner](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/banner.html),
  [clear](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/clear.html),
  [echo](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/echo.html),
  [default](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/default.html),
  [info](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/info.html),
  [pause](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/pause.html),
  [plugin](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/plugin.html),
  [quit](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/quit.html),
  [shell](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/shell.html),
  [sleep](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/sleep.html),
  [stopwatch](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/stopwatch.html),
  [sys](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/sys.html),
  [var](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/var.html),
  [version](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/version.html),
  [open](https://cloudmesh.github.io/cloudmesh-manual/manual/cmd5/open.html),
  and others



## New Features

* Support for terminals with dark background
* Support for python in variable assignments

  ```
  cms set a=\"py 1 + 1\"
  a='2'
  ```

* Support for executing python in a py command

  ```
  cms py 1 + 1
  2
  ```
  
* Support for shell commands in the variabe value

  ```
  cms set a=\!pwd
  ```
  
* Support for reading values from a yaml configuration file in
  `~/.cloudmesh/cloudmesh.yaml`

  ```  
  cms set a=cloudmesh.profile.user
  ```
  
  where it is defined as
  
  ```
  cloudmesh:
    profile:
      user: gregor
  ```
