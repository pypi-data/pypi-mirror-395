"""
Modify h5 File, Group and Dataset objects to allow pickling.

Modified from https://github.com/DaanVanVugt/h5pickle/blob/master/h5pickle
"""

from __future__ import annotations

from typing import Any

import h5py


class PickleableH5Object(h5py.HLObject):
    """Save state required to pickle and unpickle h5py objects and groups.
    This class should not be used directly, but is here as a base for inheritance
    for Group and Dataset"""

    def __getstate__(self) -> dict[str, Any] | None:
        """Save the current name and a reference to the root file object."""
        return {"name": self.name, "file": self.file_info}

    def __setstate__(self, state: dict[str, Any]) -> None:
        """File is reopened by pickle. Create an object and steal its identity."""
        # we re-create the object by calling __init__, this is technically unsafe, but I found no alternative for now
        self.__init__(state["file"][state["name"]].id)  # type: ignore[misc]
        self.file_info = state["file"]

    def __getnewargs__(self) -> tuple[()]:
        """Override the h5py getnewargs to skip its error message"""
        return ()
