import warnings
from enum import Enum
from typing import Any, Dict, List, Union

from pycivil.EXAUtils.EXAExceptions import EXAExceptions as Ex


class Table:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.__data = data
        self.__choose = -1

        # for iterables
        self.__i = -1

    def __len__(self):
        return len(self.__data["rows"])

    def __iter__(self):
        return self

    def __next__(self):
        if self.__i < self.__len__() - 1:
            self.__i += 1
            return self.__data["rows"][self.__i]
        else:
            raise StopIteration()

    def setChoose(self, idr: int) -> None:

        if "columns" in self.__data.keys():
            if "id" in self.__data["columns"]:
                idx = self.__data["columns"].index("id")
            else:
                raise Ex("0001", "one column must have id key")
        else:
            raise Ex("0002", "data must have columns key")

        for r in self.__data["rows"]:
            if r[idx] == idr:
                self.__choose = idr
                print("Scelta -->", r[1])
                return

        raise Ex("0002", "not found. wrong choose")

    def choose(self):
        return self.__choose

    def data(self):
        return self.__data

    def valueAt(self, idx: Any = -1) -> Union[Dict[str, Any], List[Any]]:

        if not isinstance(idx, int) and not isinstance(idx, Enum):
            raise Ex("ERR", "id must be int or Enum", type(idx))

        if idx is Enum:
            idx = idx.value  # type: ignore

        if idx == -1 and self.__choose == -1:
            print("ERR: not found. Use setChoose(self,id) with correct id !!!")
            return {}

        if idx == -1:
            idx = self.__choose

        for r in self.__data["rows"]:
            if r[0] == idx:
                return r

        raise Ex("ERR", "not found in tables index", idx)

    def tableValue(self):
        warnings.warn("tableValue() will be removed. Use value() instead !!!")
        if self.__choose == -1:
            print("ERR: Use setChoose(self,id) with correct id !!!")
            return ()
        else:
            for r in self.__data["rows"]:
                if r[0] == self.__choose:
                    return r

    def value(self):
        if self.__choose == -1:
            print("ERR: Use setChoose(self,id) with correct id !!!")
            return ()
        else:
            for r in self.__data["rows"]:
                if r[0] == self.__choose:
                    return r

    def __str__(self):
        dispstr = "Table Object: \n"
        dispstr = dispstr + "--------------- \n"
        if "source" in self.__data.keys():
            dispstr = dispstr + " source: {source}\n".format(
                source=self.__data["source"]
            )
        else:
            dispstr = dispstr + " source: ..."

        if "columns" in self.__data.keys():
            dispstr = dispstr + "columns: {columns}\n".format(
                columns=self.__data["columns"]
            )
        else:
            dispstr = dispstr + "columns: ..."

        if "udm" in self.__data.keys():
            dispstr = dispstr + "    udm: {udm}".format(udm=self.__data["udm"])
        else:
            dispstr = dispstr + "    udm: ..."

        dispstr += "\n"
        if "rows" in self.__data.keys():
            for row in self.__data["rows"]:
                if self.__choose != row[0]:
                    dispstr = dispstr + f"    row: {row}\n"
                else:
                    dispstr = dispstr + f"-->  row: {row}\n"
        else:
            dispstr = dispstr + "    row: ..."

        return dispstr
