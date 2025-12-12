import sys
import argparse
from portableenv import create_env, DEFAULT_VERSION

def main():
    parser = argparse.ArgumentParser(description='Create a virtual environment with embedded Python.')
    parser.add_argument('env_name', help='Name of the virtual environment to create')
    parser.add_argument('-v', '--version', default=DEFAULT_VERSION, help='Python version to use')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    create_env(args.env_name, args.version)

if __name__ == "__main__":
    main()
