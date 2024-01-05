import argparse

def cms(args):
    """
    Logic to execute based on the provided arguments.
    """
    echo = args.echo
    debug = args.debug
    nosplash = args.nosplash
    i = args.interactive
    file = args.file
    commands = args.commands

    # Your logic here
    print(f'Echo: {echo} \n'
            f'Debug: {debug}\n'
            f'Nosplash: {nosplash}\n'
            f'Interactive: {i}\n'
            f'File: {file}\n'
            f'Command: {commands}\n')
    
def main():
    parser = argparse.ArgumentParser(description="Command-line utility")

    parser.add_argument('--echo', action='store_true', help='Enable echo')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--nosplash', action='store_true', help='Do not show the banner')
    parser.add_argument('-i', '--interactive', action='store_true', help='After start, keep the shell interactive')
    parser.add_argument('--file', '-f', type=str, help='Execute the script')
    parser.add_argument('commands', nargs='*', help='Commands to be executed')

    args = parser.parse_args()
    cms(args)

if __name__ == '__main__':
    main()
