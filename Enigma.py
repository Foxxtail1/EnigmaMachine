from Rotor import Rotor
from MyToolKit import MyToolKit
from Machine import Machine
from RotorList import allRotors

toolKit = MyToolKit()

roto1 = toolKit.genRotor(allRotors["IC - 1924"])
roto2 = toolKit.genRotor(allRotors["IIC - 1924"])
roto3 = toolKit.genRotor(allRotors["IIIC - 1924"])

plugboard = MyToolKit.genPlugboard({'E': 'W', 'L': 'Y'})

reflector = MyToolKit.genReflector(len(MyToolKit.alphabet))

machineBox = Machine( rotors=[roto1, roto2, roto3], charset=MyToolKit.genAlphaNum(MyToolKit.alphabet), reflector=reflector, plugboard=plugboard)

inputText = "UXVTI IGW TRP YTH"
inputArray = [char for char in inputText]

outputText = ""
for item in inputArray:
    outputText += machineBox.enter(item)

print(outputText)