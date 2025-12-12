from typing import Any, List, Union

from pycivil.EXAUtils.EXAExceptions import EXAExceptions as ex


def validateFloat(
    var: List[Any],
    typeStr: List[Any],
    leftLimit: Union[float, None] = None,
    leftLimitEq: Union[float, None] = None,
    rightLimit: Union[float, None] = None,
    rightLimitEq: Union[float, None] = None,
) -> None:
    if not isinstance(var, list):
        raise ex("001", "var must be a list", type(var))

    if not isinstance(typeStr, list):
        raise ex("001", "typeStr must be a list of str type", type(typeStr))

    for v in var:
        if type(v) not in typeStr:
            raise ex("002", "var must be a typeStr", type(v))

        if all(
            [
                leftLimit is None,
                leftLimitEq is None,
                rightLimit is None,
                rightLimitEq is None,
            ]
        ):
            return
        else:
            if leftLimit is not None and leftLimitEq is None:
                if v <= leftLimit:
                    raise ex(
                        "003",
                        f"var must be greater than {leftLimit:.3f}",
                        type(v),
                    )
            if leftLimitEq is not None and leftLimit is None:
                if v < leftLimit:
                    raise ex(
                        "004",
                        f"var must be greater or equal than {leftLimitEq:.3f}",
                        type(v),
                    )
            if rightLimit is not None and rightLimitEq is None:
                if v <= leftLimit:
                    raise ex(
                        "005",
                        f"var must be less than {rightLimit:.3f}",
                        type(v),
                    )
            if rightLimitEq is not None and rightLimit is None:
                if v < leftLimit:
                    raise ex(
                        "006",
                        f"var must be less or equal than {rightLimitEq:.3f}",
                        type(v),
                    )
