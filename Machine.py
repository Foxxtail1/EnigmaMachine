from typing import List, Dict
from Rotor import Rotor

class Machine:

    def __init__(self, **others):
        self.__rotors = None
        self.__plugboard: Dict[chr, chr] = None
        self.__reflector: Dict[int, int] = None
        self.__charset: Dict[chr, int] = None
        self.__decoder: Dict[int, chr] = None
        self.setAtt(**others)
        

    def setAtt(self, **attrs):
        for k, v in attrs.items():
            if(k.lower() == 'reflector'):
                self.reflector = v
            elif(k.lower() == 'plugboard'):
                self.plugboard = v
            elif(k.lower() == 'rotors'):
                self.rotors = v
            elif(k.lower() == 'charset'):
                self.charset = v
            else:
                raise AttributeError(f'{self.__class__.__name__}.{k.lower()} is invalid')

    @property
    def charset(self) -> Dict[chr, int]:
        return self.__charset
    
    @charset.setter
    def charset(self, value: Dict[chr, int]):
        self.__charset = value
        self.__decoder =  {v: k for k, v in self.__charset.items()}

    @property
    def pos(self) -> List[int]:
        return [item.getPos() for item in self.__rotors]

    @pos.setter
    def pos(self, rotorNum: int, position: int):
        if(rotorNum is not None and rotorNum >= 1 and rotorNum <= len(self.__rotors)):
            if(position is not None and position >= 1 and position <= self.__rotors[rotorNum - 1].maxPos):
                self.__rotors[rotorNum - 1].setPos(position)
            else:
                raise ValueError("Invalid rotor position: " + str(position) )
        else:
            raise ValueError("Invalid rotor: " + str(rotorNum) )

    @property
    def rotors(self) -> List[Rotor]:
        return self.__rotors

    @rotors.setter
    def rotors(self, rotors: List[Rotor]):
        self.__rotors: List[Rotor] = rotors

    @property
    def reflector(self) -> Dict[int,int]:
        return self.__reflector
    
    @reflector.setter
    def reflector(self, value: Dict[int,int]):
        self.__reflector = value
    
    @property
    def plugboard(self) -> Dict[chr,chr]:
        return self.__plugboard

    @plugboard.setter
    def plugboard(self, value: Dict[chr,chr]):
        self.__plugboard = value

    def enter(self, letter: chr) -> chr:
        outputLetter = letter.upper()
        if(self.__charset is not None and outputLetter in self.__charset):
            outputLetter = self.__passPlugboard(outputLetter)
            outputLetter = self.__decoder[self.__firstPass(self.__charset[outputLetter])]
            return self.__passPlugboard(outputLetter)
        else:
            return letter
    
    def __passPlugboard(self, letter: chr) -> chr:
        outputLetter = letter
        if(self.__plugboard is not None and outputLetter in self.__plugboard):
            outputLetter = self.__plugboard[outputLetter]
        return outputLetter
    
    def __passReflector(self, pin: int) -> int:
        if(self.__reflector is not None and pin in self.__reflector):
            return self.__secondPass(self.__reflector[pin])
        return pin
    
    def __secondPass(self, pin: int) -> int:
        currentPin = pin
        for rotor in self.__rotors[::-1]:
            currentPin = rotor.leftToRight(currentPin)
        return currentPin

    def __firstPass(self, pin: int) -> int:
        currentPin = pin
        if(self.__rotors is not None):
            self.__turnRotors()
            for rotor in self.__rotors:
                currentPin = rotor.rightToLeft(currentPin)
            return self.__passReflector(currentPin)        
        else:
            return currentPin

    def __turnRotors(self):
        turnTheNext = True
        for rotor in self.__rotors:
            if(turnTheNext):
                turnTheNext = rotor.turn()
            else:
                break
