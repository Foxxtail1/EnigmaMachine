import tkinter as tk
from tkinter import ttk
from Rotor import Rotor
from MyToolKit import MyToolKit
from Machine import Machine
from RotorList import allRotors
from typing import List, Dict, Optional

class EnigmaFrame(tk.Tk):

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ*"
    charaArray = [char for char in alphabet]

    def __init__(self) -> None:
        super().__init__()
        #Items for the keys
        self.__keys_frame: tk.Frame = None
        self.__keys_frames: Dict[chr, tk.LabelFrame] = None
        self.__keys_lables: Dict[chr, tk.Label] = None

        self.__io_frame: tk.Frame = None

        self.__outputFrame:  tk.LabelFrame = None
        self.__text_output: tk.Entry =  None
        self.__str_output: tk.StringVar = None

        self.__inputFrame: tk.LabelFrame = None
        self.__text_input: tk.Entry = None
        self.__str_input: tk.StringVar = None

        self.__buttonGo: tk.Button = None
        
        self.__rotorFrame: tk.Frame = None
        self.__activeRotors: tk.LabelFrame = None
        self.__rotorCmb: ttk.Combobox = None

        self.__machine: Machine = None
        self.__rotors: List[Rotor] = []
        self.__rotorEntries: List[tk.Entry] = []
        self.__rotorPositionFrame: tk.Frame = None
        self.__rotorPosSubFrame: List[tk.Frame] = []
        self.__rotorPosLables: List[tk.Label]  = []
        self.__rotorStringVars: List[tk.StringVar] = []
        self.mechineSetup()

        self.__setup_keys_frame()
        self.__setup_IO_frame()
        self.__link_events()
        self.__setupRotorFrame()
        self.__setup_rotor_position_frame()

    def __setup_keys_frame(self):
        self.__keys_frame = tk.Frame()
        self.__keys_frame.grid()

        self.__keys_frames = {}
        self.__keys_lables = {}

        maxRow = 8
        currentLine = 0
        currentLetter = 0

        while currentLetter < len(EnigmaFrame.charaArray):
            currentRow = 0
            self.__keys_frame.grid_rowconfigure(currentLine, weight=1)
            self.__keys_frame.grid_columnconfigure(currentLine, weight=1)
            while currentRow < maxRow and currentLetter < len(EnigmaFrame.charaArray):
                letter = EnigmaFrame.charaArray[currentLetter]
                tempFrame = tk.LabelFrame(self.__keys_frame, width=20, height=10)
                self.__keys_frames[letter] = tempFrame
                tempFrame.grid(row=currentLine, column=currentRow, sticky="wse")
                tempLbl = tk.Label(tempFrame, text=letter)
                self.__keys_lables[letter] = tempLbl
                tempLbl.pack()
                currentLetter += 1
                currentRow += 1
            currentLine += 1

        self.__keys_frame.pack()

    def __setup_rotor_position_frame(self):
        self.__rotorPositionFrame = tk.Frame()
        
        self.__rotors = self.__machine.rotors

        

        for rotor in self.__rotors:
            tempoBack = self.register(self.validate_pos), '%P', '%V', '%W'
            tempFrame = tk.Frame(self.__rotorPositionFrame)
            self.__rotorPosSubFrame.append(tempFrame)

            tempLbl = tk.Label(tempFrame, text=rotor.name)
            self.__rotorPosLables.append(tempLbl)

            tempVar = tk.StringVar()
            self.__rotorStringVars.append(tempVar)
            tempEntry = tk.Entry(tempFrame, textvariable=tempVar, validate='all', validatecommand=(tempoBack, '%P', '%V', tempVar))
            self.__rotorEntries.append(tempEntry)

            tempVar.set(rotor.pos)

            tempLbl.pack(side=tk.LEFT)
            tempEntry.pack(side=tk.RIGHT)
            tempFrame.pack()

        self.__rotorPositionFrame.pack()

    def updateRotorPos(self):
        i = 0 
        while i < len(self.__rotors):
            self.__rotorStringVars[i].set(self.__rotors[i].pos)
            print(self.__rotors[i].pos)
            self.__rotorEntries[i].pack()
            i += 1



    def __setup_IO_frame(self):
        self.__io_frame = tk.Frame()
        
        self.__outputFrame = tk.LabelFrame(self.__io_frame, text="Output")
        self.__str_output = tk.StringVar()
        self.__text_output = tk.Entry(self.__outputFrame, width=40, textvariable=self.__str_output, state="readonly")

        self.__outputFrame.pack()
        self.__text_output.pack()

        self.__inputFrame = tk.LabelFrame(self.__io_frame, text="Input")
        self.__str_input = tk.StringVar()
        self.__text_input = tk.Entry(self.__inputFrame, width=40, textvariable=self.__str_input)
    
        self.__buttonGo = tk.Button(self.__inputFrame, text="Enter")

        self.__text_input.pack(side=tk.LEFT)
        self.__buttonGo.pack(side=tk.RIGHT)
        self.__inputFrame.pack()

        self.__io_frame.pack()

    def __setupRotorFrame(self):
        self.__rotorFrame = tk.Frame()

        self.__rotorCmb = ttk.Combobox(self.__rotorFrame, width=16, state="readonly", values=[k for k, v in allRotors.items()])
        self.__rotorCmb.current(1)
        self.__rotorCmb.pack()

        self.__activeRotors = tk.LabelFrame(self.__rotorFrame, text="rotors")
        self.__activeRotors.pack()

        self.__rotorFrame.pack()

    def turnOff(self, letter: chr):
        if letter in self.__keys_frames:
            self.__keys_lables[letter].config(bg="SystemButtonFace")
        else:
            self.turnOff('*')

    def lightUp(self, letter: chr):
        if letter in self.__keys_frames:
            self.__keys_lables[letter].config(bg="yellow")
        else:
            self.lightUp('*')
  
    def lighter(self, textCode: str):
        charaArrayInput = [char for char in textCode]
        self.__str_output.set("")
        tempoChr = ''
        for item in charaArrayInput:
            tempoChr = self.__machine.enter(item)
            self.updateRotorPos()
            self.__str_output.set(self.__str_output.get() + tempoChr)
            self.lightUp(tempoChr)
            self.__keys_frame.update()
            self.__keys_frame.after(300)
            self.turnOff(tempoChr)
            self.__keys_frame.update()
            self.__keys_frame.after(300)

    def validate_pos(self, input: str, eventType: str, strvar: tk.StringVar):
        print(strvar.get())
        if eventType == 'focusout':
            if input == "":
                print("empty")
                return False
            else:
                return True

        elif eventType == 'key':
            if input.isdigit() or input == "":
                return True
            else:
                return False
        else:
            return True

        

    def __button_enter_press(self, event = None):
        self.lighter(self.__str_input.get().strip())

    def __link_events(self):
        self.__text_input.bind('<Return>', self.__button_enter_press)
        self.__buttonGo.config(command=self.__button_enter_press)

    def mechineSetup(self):
        toolKit = MyToolKit()
        roto1 = toolKit.genRotor(allRotors["IC - 1924"])
        roto2 = toolKit.genRotor(allRotors["IIC - 1924"])
        roto3 = toolKit.genRotor(allRotors["IIIC - 1924"])

        plugboard = MyToolKit.genPlugboard({'E': 'W', 'L': 'Y'})
        reflector = MyToolKit.genReflector(len(MyToolKit.alphabet))
        self.__machine = Machine( rotors=[roto1, roto2, roto3], charset=MyToolKit.genAlphaNum(MyToolKit.alphabet), reflector=reflector, plugboard=plugboard)

root = EnigmaFrame()
root.geometry("300x450")

root.title("Enigma")
root.mainloop()