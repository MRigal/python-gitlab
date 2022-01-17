"""
Ensure objects defined in gitlab.v4.objects are imported in
`gitlab/v4/objects/__init__.py`

"""
import os
import pkgutil
from typing import Set

import gitlab.v4.objects


def test_verify_v4_objects_imported() -> None:
    assert len(gitlab.v4.objects.__path__) == 1
    v4_objects_init_file = os.path.join(gitlab.v4.objects.__path__[0], "__init__.py")

    init_files: Set[str] = set()
    with open(v4_objects_init_file, "r") as in_file:
        for line in in_file.readlines():
            if line.startswith("from ."):
                init_files.add(line.rstrip())

    object_files = set()
    for module in pkgutil.iter_modules(gitlab.v4.objects.__path__):
        object_files.add(f"from .{module.name} import *")

    missing_in_init = object_files - init_files
    error_message = (
        f"\nThe file {v4_objects_init_file!r} is missing the following imports:"
    )
    for missing in sorted(missing_in_init):
        error_message += f"\n    {missing}"

    assert not missing_in_init, error_message
