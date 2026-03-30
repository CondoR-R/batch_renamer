from . import cli
from . import validators
from . import renamer
from . import exceptions


def main():
    args = cli.get_args()
    try:
        path = validators.validate_path(args.path)
        ext_arr = None
        if args.ext:
            ext_arr = validators.validate_ext(args.ext)
        r = renamer.Renamer(path=path, pattern=args.pattern, ext_arr=ext_arr)
        r.execute(args.dry_run)
    except exceptions.BatchRenamerError as err:
        cli.show_error(err)


if __name__ == "__main__":
    main()
