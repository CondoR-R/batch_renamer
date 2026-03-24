import dataclasses


@dataclasses.dataclass()
class Args:
    path: str
    pattern: str
    dry_run: bool
