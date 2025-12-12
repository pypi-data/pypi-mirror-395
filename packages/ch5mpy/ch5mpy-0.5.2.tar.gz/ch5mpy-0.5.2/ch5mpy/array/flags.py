from typing import Any

from ch5mpy.objects.dataset import Dataset, DatasetWrapper


class FlagDict:
    _flags: dict[str, bool]

    # region magic methods
    def __init__(self, dset: Dataset[Any] | DatasetWrapper[Any]) -> None:
        object.__setattr__(
            self,
            "_flags",
            {
                "C_CONTIGUOUS": dset.chunks is not None,
                "F_CONTIGUOUS": False,
                "OWNDATA": True,
                "WRITEABLE": True,
                "ALIGNED": False,  # TODO:
                "WRITEBACKIFCOPY": False,
            },
        )

    def __getitem__(self, key: str, /) -> bool:
        match key:
            case "FNC":
                return self._flags["F_CONTIGUOUS"] and not self._flags["C_CONTIGUOUS"]

            case "FORC":
                return self._flags["F_CONTIGUOUS"] or self._flags["C_CONTIGUOUS"]

            case "BEHAVED":
                return self._flags["ALIGNED"] and self._flags["WRITEABLE"]

            case "CARRAY":
                return self._flags["ALIGNED"] and self._flags["WRITEABLE"] and self._flags["C_CONTIGUOUS"]

            case "FARRAY":
                return (
                    self._flags["ALIGNED"]
                    and self._flags["WRITEABLE"]
                    and self._flags["F_CONTIGUOUS"]
                    and not self._flags["C_CONTIGUOUS"]
                )

            case _:
                return self._flags[key]

    def __setitem__(self, key: str, value: bool) -> None:
        assert key in self._flags.keys()
        self._flags[key] = value

    def __getattr__(self, name: str) -> bool:
        return self[name.upper()]

    def __setattr__(self, name: str, value: bool, /) -> None:
        self[name.upper()] = value

    # endregion
