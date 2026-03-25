from . import cli
from . import validators
from . import renamer
from . import exceptions


def main():
    args = cli.get_args()
    try:
        path = validators.validate_path(args.path)
        r = renamer.Renamer(path=path, pattern=args.pattern)
        r.execute(args.dry_run)
    except exceptions.BatchRenamerError as err:
        cli.show_error(err)


if __name__ == "__main__":
    main()
