from __future__ import print_function

from datetime import datetime

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.var.command.var import VarCommand



class SetCommand(PluginCommand):
    # noinspection PyUnusedLocal
    @command
    def do_set(self, args, arguments):
        """
        ::

          Usage:
            set list
            set clear
            set delete NAME
            set NAME=VALUE
            set NAME
                          
          Arguments:
            NAME      the name of the setiable
            VALUE     the value of the setiable
            FILENAME  the filename of the setiable

          Description:
            Manage persistent setiables
            
            set NAME=VALUE
               sets the setiable with the name to the value
               if the value is one of data, time, now it will be 
               replaced with the value at this time, the format will be
                date    2017-04-14
                time    11:30:33
                now     2017-04-14 11:30:41
            It will wbe replaced accordingly    
            
            The value can also refer to another setiable name.
            In this case the current value will be copied in the named
            setiable. As we use the $ sign it is important to distinguish
            shell setiables from cms setiables while using proper quoting.
            
            Examples include:
            
               cms set a=\$b
               cms set 'a=$b'
               cms set a=val.b
               
            The previous command copy the value from b to a. The val command
            was added to avoid quoting.
            
            
        """
        c = VarCommand()
        c.do_var(args)
