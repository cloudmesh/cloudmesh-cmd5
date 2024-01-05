import click

@click.command()
@click.option('--echo', is_flag=True, help='Enable echo')
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--nosplash', is_flag=True, help='Do not show the banner')
@click.option('-i', is_flag=True, help='After start, keep the shell interactive')
@click.option('--file', '-f', type=str, help='Execute the script')
@click.argument('COMMAND', required=False, nargs=-1)
def cms(echo, debug, nosplash, i, file, command):
    """
    Usage:
      cms --help
      cms [--echo] [--debug] [--nosplash] [-i] [--file=SCRIPT] [COMMAND ...]

    Arguments:
      COMMAND                  A command to be executed
    """
    # Your logic here
    # You can access the values of options using the provided arguments (echo, debug, nosplash, i, file, command)
    click.echo(f'Echo: {echo} \n'
               f'Debug: {debug}\n'
               f'Nosplash: {nosplash}\n'
               f'Interactive: {i}\n'
               f'File: {file}\n'
               f'Command: {command}\n')

    print ("COMMAND:", command)

if __name__ == '__main__':
    cms()
