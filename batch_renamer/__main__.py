from . import cli
from . import validators


def main():
    args = cli.get_args()
    print(args)
    path = validators.validate_path(args.path)
    print(path)


if __name__ == "__main__":
    main()
