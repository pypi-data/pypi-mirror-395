from typing import List, Union


class Fun:
    def __init__(
        self, left: Union[float, None] = None, right: Union[float, None] = None
    ):
        self.__left = left
        self.__right = right

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, val):
        if isinstance(val, float) or val is None:
            if self.__left is not None:
                if self.__right is not None and self.__left <= self.__right:
                    self.__left = val
                elif self.__right is None:
                    self.__left = val
                else:
                    raise ValueError("Left must be less or equal then Right")
            else:
                self.__left = val
        else:
            raise ValueError("Left must be float or None type")

    @left.deleter
    def left(self):
        del self.__left

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, val):
        if isinstance(val, float) or val is None:
            if self.__right is not None:
                if self.__left is not None and not self.__left > self.__right:
                    self.__right = val
                elif self.__left is None:
                    self.__right = val
                else:
                    print(f"Left {self.__left}")
                    print(f"Right {self.__right}")
                    raise ValueError("Right must be greater or equal then Right")
            else:
                self.__right = val
        else:
            raise ValueError("Right must be float or None type")

    @right.deleter
    def right(self):
        del self.__right

    def eval(self, x: float) -> float:
        raise NotImplementedError("eval() not implemented for subclass !!!")


class piecewiseFun(Fun):
    def __init__(
        self, x: Union[List[float], None] = None, fx: Union[List[float], None] = None
    ):
        super().__init__()
        if x is None:
            x = []

        if fx is None:
            fx = []

        self.__x = x
        self.__fx = fx

        if len(x) != len(fx):
            raise ValueError(f"Len of x <{self.__x}> must be same of fx <{self.__fx}>")

        if len(x) > 0:
            self.left = self.__x[0]
            self.right = self.__x[len(self.__x) - 1]

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val):
        if isinstance(val, list):
            for v in val:
                if not isinstance(v, float):
                    raise ValueError(f"The value {v} must be float")
            self.__x = val
        else:
            raise ValueError("Need to assign only list of float to piecewiseFun")

    @x.deleter
    def x(self):
        del self.__x

    @property
    def fx(self):
        return self.__fx

    @fx.setter
    def fx(self, val):
        if isinstance(val, list):
            for v in val:
                if not isinstance(v, float):
                    raise ValueError(f"The value {v} must be float")
            self.__fx = val
        else:
            raise ValueError("Need to assign only list of float to piecewiseFun")

    @fx.deleter
    def fx(self):
        del self.__fx

    def eval(self, x: float) -> float:

        if len(self.__x) != len(self.__fx):
            raise ValueError(f"Len of x <{self.__x}> must be same of fx <{self.__fx}>")

        self.left = self.__x[0]
        self.right = self.__x[len(self.__x) - 1]

        for i in range(0, len(self.__x) - 1):
            x1 = self.__x[i]
            x2 = self.__x[i + 1]
            fx1 = self.__fx[i]
            fx2 = self.__fx[i + 1]
            if x2 == x1:
                raise ValueError(f"Value x2 <{x1}> is same of x1")
            if x > x1 and x < x2:
                A = fx2 - fx1 / (x2 - x1)
                B = fx1 - A * x1
                return A * x + B
            elif x == x1:
                return fx1
            elif x == x2:
                return fx2
            else:
                pass

        raise ValueError(
            "Value x must inside ({},{})".format(
                self.__x[0], self.__x[len(self.__x) - 1]
            )
        )
