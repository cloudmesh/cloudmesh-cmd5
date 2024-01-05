import sys

def cms(arguments):
    """
    Usage:
      cms --help
      cms [--echo] [--debug] [--nosplash] [-i] [--file=SCRIPT] [COMMANDS...]

    Arguments:
      COMMANDS                 Commands to be executed
    """
    # Your logic here
    echo = '--echo' in arguments
    debug = '--debug' in arguments
    nosplash = '--nosplash' in arguments
    i = '-i' in arguments
    file_index = arguments.index('--file') if '--file' in arguments else None
    file = arguments[file_index + 1] if file_index is not None and file_index + 1 < len(arguments) else None
    commands = [arg for arg in arguments if arg not in [
        '--echo',
        '--debug',
        '--nosplash',
        '-i',
        '--file', file]]

    # Print values for demonstration purposes
    print(f'Echo: {echo} \n'
               f'Debug: {debug}\n'
               f'Nosplash: {nosplash}\n'
               f'Interactive: {i}\n'
               f'File: {file}\n'
               f'Command: {commands}\n')

if __name__ == '__main__':
    cms(sys.argv[1:])
