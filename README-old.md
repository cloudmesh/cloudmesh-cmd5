
### Execution shell commands (not yet activated)

You can execute shell commands when the beginning charater is ! ::

    cms \!pwd
    cms shell pwd


### Timers (not yet activated)

To switch timers on or off you can use

    cms var timer=True

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
