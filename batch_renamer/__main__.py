from . import cli
from . import validators
from . import renamer


def main():
    args = cli.get_args()
    path = validators.validate_path(args.path)
    r = renamer.Renamer(path=path, pattern=args.pattern)
    r.execute(args.dry_run)


if __name__ == "__main__":
    main()
