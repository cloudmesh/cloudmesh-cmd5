Cloudmesh cmd5
==============

An dynamically extensible CMD based command shell. For en extensive
documentation please see

* <https://github.com/cloudmesh-community/book/blob/master/vonLaszewski-cloud.epub?raw=true>

where we also document how to use pyenv virtualenv.

Requirements
------------

* Python greater equal 3.7.2
* Python greater equal 2.7.15

Cloudmesh was able to run on earlier versions of python, but we do prefer to test it on the newest version.

Installation from source
------------------------

Setup a virtualenv either with virtualenv or pyenv.
We have a tutorial on cloudmesh classes for the use of
pyenv. Pyenv is easy to unstall via the installer documented at

* <https://github.com/pyenv/pyenv-installer>

```bash
$ curl https://pyenv.run | bash
```

Add the following lines to your .bashrc or .bash_profile

```
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

to install 3.7.2 use and activate it 

```
pyenv install 3.7.2
pyenv activate 3.7.2
```

    
Now you need to get two source directories. We assume yo place them in
~/github::

    mkdir ~/github
    cd ~/github
    git clone https://github.com/cloudmesh/cloudmesh.common.git
    git clone https://github.com/cloudmesh/cloudmesh.cmd5.git
    git clone https://github.com/cloudmesh/cloudmesh.bar.git
    git clone https://github.com/cloudmesh/cloudmesh.sys.git

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
    cd ~/github/cloudmesh.sys
    python setup.py install
    pip install .
  
:o: The following has to  be tested (pip instaltion not yet working):

> In case you like to install the cloudmesh client, you can isna\stall it either from source
>
>     git clone https://github.com/cloudmesh/cloudmesh.client.git
>     cd ~/github/cloudmesh.client
>     python setup.py install
>     pip install .
>
> or from pip:
>
>     pip install cloudmesh_client
    

Instalation from pip
--------------------

---

> :warning: we do recommend that you install cmd5 from source as not all 
> features will be accessible to you if you do a pip install

---

To install cmd5 from pip please use::

    pip install cloudmesh.cmd5

The cloudmesh.bar repository you want to download as source so you can
learn how to write your own commands::

    mkdir ~/github
    cd ~/github
    git clone https://github.com/cloudmesh/cloudmesh.bar.git

Commands are shared in the `cloudmesh` namespace.

The better method on writing a command is to install cloudmesh.sys and use the 
sys command to generate a new command template via a program. You can generate 
a new command with::

    cms sys command generate NAME
	
A directory with the name cloudmesh.NAME will be generated that contains the template
for the command NAME. 

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

To see the manual page for a specific command, please use::

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


Features
--------

The following changes are available in the cloudmesh.cmd5 and cloudmesh.common,
that are available as source. So you must clone them. They are not yet available in pypi

### Execution shell commands

You can execute shell commands when the beginning charater is ! ::

    cms \!pwd
    cms shell pwd


### Timers

To switch timers on or off you can use

    cms var timer=on

Than every command you type is timed::

    $ cms banner hallo
    banner
    ######################################################################
    # hallo
    ######################################################################
    Timer: 0.0011s (banner hallo)

### Variables

you can store variables with::

    var a=1

you can access them on the commandline with ::

    var.a
    \$a

You can list all variables with::

    var list

OS Variables can also be integrated. `os.HOME` will be replaced
with the HOME variable from the shell, try it with::

     cms banner os.HOME


### Defaults

Defaults are variables with a context in which the default applies.
For example we can set default images for a cloud. General defaults
are placed in the context `general`. To set the default cloud you can use::

    default cloud=kilo

To List the defaults use::

     default list

To use the defaults in a command preceed it with the the keyword `default.`
and append the context and the name of the default variable. If the context
is missing, the `general` context will be used. Examples::

    banner default.cloud
    default image=ubnuntu --context=chameleon
    banner default.chameleon.image


### Stopwatch

for some (not all) benchmarks this could be helpful. It only works in script mode of cmd5

put this in a file called s.cm::

    stopwatch start g
    stopwatch stop g
    stopwatch print g

Then execute::

    cat s.cm | cms

You will get something like this::

    cat s.cm | cms


    +-------------------------------------------------------+
    |   ____ _                 _                     _      |
    |  / ___| | ___  _   _  __| |_ __ ___   ___  ___| |__   |
    | | |   | |/ _ \| | | |/ _` | '_ ` _ \ / _ \/ __| '_ \  |
    | | |___| | (_) | |_| | (_| | | | | | |  __/\__ \ | | | |
    |  \____|_|\___/ \__,_|\__,_|_| |_| |_|\___||___/_| |_| |
    +-------------------------------------------------------+
    |                  Cloudmesh CMD5 Shell                 |
    +-------------------------------------------------------+
    cms> Timer g started ...
    cms> Timer g started ...
    cms> Timer g: 0.000274181365967 s


## Docker

Cloudmesh can be run easily in a container with the help of docker. A
Dockefile is provided as an example that you may adapt for your needs

To use the docker file we have included a numbe or convenient
targets also in our makefile.

You can create the image with

    make image

You can run teh image and enter a shell with

    make shell

This allows you to try things out in the image from bash which is good
for development and debugging.  You can directly enter the cloudmesh
shell `cms` with

    make cms

or say

    docker run -it cloudmesh/cmd5:1.0

It will create a default .cloudmesh/yaml file whihc your would have to
modify. The reason we have not mounted the yaml file in the make files
form your directory is that we need a clean image to test the initial
setup.

If you have an example on how to mount teh yaml file please let us
know and we add it here.
