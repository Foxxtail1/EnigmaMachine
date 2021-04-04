from typing import List, Dict

class Rotor:

    def __init__(self, wiring: Dict[int, int], name: str = ""):
        self.__rightSide = None
        self.__leftSide = None
        self.__maxPos = None
        self.__initRotor(wiring)
        self.__pos = 0
        self.__name = name
    
    def __str__(self):
        return self.name
    
    def __initRotor(self, wiring: Dict[int, int]):
        self.__rightSide = wiring
        self.__leftSide = {v: k for k, v in self.__rightSide.items()}
        self.__maxPos = len(wiring)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def maxPos(self) -> int:
        return self.__maxPos

    @property
    def pos(self) -> int:
        return self.__pos + 1
    
    @pos.setter
    def pos(self, value: int):
        if(value is None or value - 1 < 0 or value > self.__maxPos):
            raise ValueError(f'Value for {self.__class__.__name__}.pos is invalid: {value}')
        self.__pos = value - 1 

    def rightToLeft(self, pinIn: int) -> int:
        return self.__OffsetLeftSide(self.__rightSide[self.__OffsetRightSide(pinIn)])

    def leftToRight(self, pinIn: int) -> int:
        return self.__OffsetLeftSide(self.__leftSide[self.__OffsetRightSide(pinIn)])

    def turn(self) -> bool:
        tempPos = self.__pos + 1

        if(tempPos >= self.__maxPos):
            self.__pos = 0
            return True
        else:
            self.__pos = tempPos
            return False

    def __OffsetRightSide(self, pinIn: int) -> int:
        offset = self.__pos + pinIn
        if (offset >= self.__maxPos):
            offset -= self.__maxPos
        return offset
    
    def __OffsetLeftSide(self, pinOut: int) -> int:
        offset = pinOut - self.__pos
        if (offset <= -1):
            offset += self.__maxPos
        return offset 