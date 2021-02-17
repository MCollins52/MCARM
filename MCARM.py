# MCARM Software

#############################################################
# Import packages

import serial
import time
from tkinter import *
import tkinter.ttk
import numpy as np
from math import cos, sin, sqrt, pi, atan2
import matplotlib.pyplot as plt
import tinyik


#############################################################
# Initialize program / Look for Teensy 3.6

serPort = "COM5"
baudRate = 115200
teensy = serial.Serial(serPort, baudRate)
print("Serial port " + serPort + " opened  Baudrate " + str(baudRate) + "\n")
print("If taking more than a couple of seconds, disconnect the Teensy and try again.\n"
      "If connecting instantly fails while the Teensy is on, try again. It probably reset itself.\n"
      "If connecting fails multiple times, try to upload the arduino sketch to the teensy and verify the COM port.")




#############################################################
# Global parameters / variables

# Every message the teensy sends out should begin with < and end with > to mark the start and end of the message
startMarker = 60  # This is < in ASCII
endMarker = 62    # This is > in ASCII

functionValue = ''

# Current joint positions in degrees
j1CurrentDegPos = 0.
j2CurrentDegPos = 0.
j3CurrentDegPos = 0.
j4CurrentDegPos = 0.
j5CurrentDegPos = 0.
j6CurrentDegPos = 0.
TCCurrentPercentPos = 0.  # Tool changer jogging is in percentages from min to max

XCurrentPos = 0.
YCurrentPos = 0.
ZCurrentPos = 0.

########################################
# Motor parameters

speedMultiplier = 1.

J1StepsPerRev = 200.  # 200 steps per revolution
J2StepsPerRev = 200.
J3StepsPerRev = 200.
J4StepsPerRev = 200.
J5StepsPerRev = 200.
J6StepsPerRev = 200.
TCStepsPerRev = 200.

J1Gearbox = 50.  # Gearbox reduction. 50 is a 50:1
J2Gearbox = 50.
J3Gearbox = 50.
J4Gearbox = 50.
J5Gearbox = 50.
J6Gearbox = 50.
TCGearbox = 50.

J1MicroStep = 2.  # Half stepping  # Change this
J2MicroStep = 2.
J3MicroStep = 2.
J4MicroStep = 2.
J5MicroStep = 2.
J6MicroStep = 2.
TCMicroStep = 2.



#############################################################
# Communicate with Teensy


def startTeensy():
    outData = "999"
    sendToTeensy(outData)


def sendToTeensy(sendStr):  # sends data to the teensy
    sendStr = ('<' + sendStr + '>')
    teensy.write(sendStr.encode('utf-8'))
    teensy.flushInput()
    print('Data sent: ', sendStr)
    if sendStr != '<999>':  # Don't send startup and ending command values to GUI. Closing value is pointless (won't see it) and causes an error.
        outputToGUI(sendStr)


def recvFromTeensy():
    global startMarker, endMarker

    ck = ""
    x = "0"  # any value that is not an end or startMarker
    byteCount = -1  # to allow for the fact that the last increment will be one too many

    # wait for the start character
    while ord(x) != startMarker:
        x = teensy.read()

    # save data until the end marker is found
    while ord(x) != endMarker:
        if ord(x) != startMarker:
            ck = ck + x.decode("ISO-8859-1")
            byteCount += 1
        x = teensy.read()

    return (ck)


def waitForTeensy():
    # wait until the teensy sends 'Teensy is ready'

    global startMarker, endMarker

    msg = ""
    while msg.find("Teensy is ready") == -1:

        while teensy.inWaiting() == 0:
            pass

        msg = recvFromTeensy()
        print(msg + '\n')







#############################################################
# GUI Functions (Buttons)

# Every function must have a value assigned to it to send to the Teensy


def home():
    functionValue = '0'
    sendToTeensy(functionValue)


def restPosition():
    functionValue = '1'
    sendToTeensy(functionValue)


def calibrate():
    functionValue = '2'
    sendToTeensy(functionValue)


def fineCalibrate():
    functionValue = '3'
    sendToTeensy(functionValue)


def teachPosition():
    functionValue = '4'
    sendToTeensy(functionValue)


def goToTeachPosition():
    functionValue = '5'
    sendToTeensy(functionValue)


def jogX():
    functionValue = '6'
    sendToTeensy(functionValue)


def jogY():
    functionValue = '7'
    sendToTeensy(functionValue)


def jogZ():
    functionValue = '8'
    sendToTeensy(functionValue)


def yee():
    functionValue = '9'
    sendToTeensy(functionValue)


def updateSpeed():
    functionValue = '10'
    sendToTeensy(functionValue)


def calibrateJ1():
    functionValue = '11'
    sendToTeensy(functionValue)


def calibrateJ2():
    functionValue = '12'
    sendToTeensy(functionValue)


def calibrateJ3():
    functionValue = '13'
    sendToTeensy(functionValue)


def calibrateJ4():
    functionValue = '14'
    sendToTeensy(functionValue)


def calibrateJ5():
    functionValue = '15'
    sendToTeensy(functionValue)


def calibrateJ6():
    functionValue = '16'
    sendToTeensy(functionValue)


def calibrateTC():
    functionValue = '17'
    sendToTeensy(functionValue)


def grabTC():
    functionValue = '18'
    sendToTeensy(functionValue)


def releaseTC():
    functionValue = '19'
    sendToTeensy(functionValue)


def q():
    functionValue = '20'
    sendToTeensy(functionValue)


def w():
    functionValue = '21'
    sendToTeensy(functionValue)


def e():
    functionValue = '22'
    sendToTeensy(functionValue)


def r():
    functionValue = '23'
    sendToTeensy(functionValue)


def t():
    functionValue = '24'
    sendToTeensy(functionValue)


def y():
    functionValue = '25'
    sendToTeensy(functionValue)


def u():
    functionValue = '26'
    sendToTeensy(functionValue)


def i():
    functionValue = '27'
    sendToTeensy(functionValue)


def o():
    functionValue = '28'
    sendToTeensy(functionValue)





def turnLedOn():
    functionValue = '34'
    sendToTeensy(functionValue)


def turnLedOff():
    functionValue = '58'
    sendToTeensy(functionValue)




def getJ1JogValPos():
    j1JogVal = str(jogJ1Entry.get())
    jog('1', j1JogVal, j1CurrentDegPos)


def getJ1JogValNeg():
    j1JogVal = str(jogJ1Entry.get())
    j1JogVal = '-' + j1JogVal
    jog('1', j1JogVal, j1CurrentDegPos)


def getJ2JogValPos():
    j2JogVal = str(jogJ2Entry.get())
    jog('2', j2JogVal, j2CurrentDegPos)


def getJ2JogValNeg():
    j2JogVal = str(jogJ2Entry.get())
    j2JogVal = '-' + j2JogVal
    jog('2', j2JogVal, j2CurrentDegPos)


def getJ3JogValPos():
    j3JogVal = str(jogJ3Entry.get())
    jog('3', j3JogVal, j3CurrentDegPos)


def getJ3JogValNeg():
    j3JogVal = str(jogJ3Entry.get())
    j3JogVal = '-' + j3JogVal
    jog('3', j3JogVal, j3CurrentDegPos)


def getJ4JogValPos():
    j4JogVal = str(jogJ4Entry.get())
    jog('4', j4JogVal, j4CurrentDegPos)


def getJ4JogValNeg():
    j4JogVal = str(jogJ4Entry.get())
    j4JogVal = '-' + j4JogVal
    jog('4', j4JogVal, j4CurrentDegPos)


def getJ5JogValPos():
    j5JogVal = str(jogJ5Entry.get())
    jog('5', j5JogVal, j5CurrentDegPos)


def getJ5JogValNeg():
    j5JogVal = str(jogJ5Entry.get())
    j5JogVal = '-' + j5JogVal
    jog('5', j5JogVal, j5CurrentDegPos)


def getJ6JogValPos():
    j6JogVal = str(jogJ6Entry.get())
    jog('6', j6JogVal, j6CurrentDegPos)


def getJ6JogValNeg():
    j6JogVal = str(jogJ6Entry.get())
    j6JogVal = '-' + j6JogVal
    jog('6', j6JogVal, j6CurrentDegPos)


def getTCJogValPos():
    TCJogVal = str(jogTCEntry.get())
    jog('7', TCJogVal, TCCurrentPercentPos)


def getTCJogValNeg():
    TCJogVal = str(jogTCEntry.get())
    TCJogVal = '-' + TCJogVal
    jog('7', TCJogVal, TCCurrentPercentPos)


def getXJogValPos():
    XJogVal = str(jogXEntry.get())
    jog('X', XJogVal, XCurrentPos)


def getXJogValNeg():
    XJogVal = str(jogXEntry.get())
    XJogVal = '-' + XJogVal
    jog('X', XJogVal, XCurrentPos)


def getYJogValPos():
    YJogVal = str(jogYEntry.get())
    jog('Y', YJogVal, YCurrentPos)


def getYJogValNeg():
    YJogVal = str(jogYEntry.get())
    YJogVal = '-' + YJogVal
    jog('Y', YJogVal, YCurrentPos)


def getZJogValPos():
    ZJogVal = str(jogZEntry.get())
    jog('Z', ZJogVal, ZCurrentPos)


def getZJogValNeg():
    ZJogVal = str(jogZEntry.get())
    ZJogVal = '-' + ZJogVal
    jog('Z', ZJogVal, ZCurrentPos)






def outputToGUI(outputText):
    # StatusOutput.delete("1.0", "end")
    outputText = outputText + '\n'
    StatusOutput.insert(END, outputText)





#############################################################
# Functions


def jog(jointJogging, jogAmountDeg, currentDegPos):

    outputText = 'Jogging J' + jointJogging + ' ' + jogAmountDeg + ' degrees\n'

    if jointJogging == '7':  # change 'Jogging J7' to 'Jogging TC'
        outputText = 'Jogging TC ' + jogAmountDeg + ' %\n'
    StatusOutput.insert(END, outputText)

    if jointJogging == '1':
        global j1CurrentDegPos  # must define the current position as a global variable to be modified
        jogAmountDeg = float(jogAmountDeg)  # convert to float from string
        j1CurrentDegPos = j1CurrentDegPos + jogAmountDeg  # accumulate current joint position
        J1DegShow.delete(0., 'end')  # delete previous entry. The 0 must be a float
        J1DegShow.insert(END, j1CurrentDegPos)  # insert the current joint position
        jogAmountDeg = str(jogAmountDeg)  # convert back to string

    if jointJogging == '2':
        global j2CurrentDegPos  # must define the current position as a global variable to be modified
        jogAmountDeg = float(jogAmountDeg)  # convert to float from string
        j2CurrentDegPos = j2CurrentDegPos + jogAmountDeg  # accumulate current joint position
        J2DegShow.delete(0., 'end')  # delete previous entry. The 0 must be a float
        J2DegShow.insert(END, j2CurrentDegPos)  # insert the current joint position
        jogAmountDeg = str(jogAmountDeg)  # convert back to string

    if jointJogging == '3':
        global j3CurrentDegPos  # must define the current position as a global variable to be modified
        jogAmountDeg = float(jogAmountDeg)  # convert to float from string
        j3CurrentDegPos = j3CurrentDegPos + jogAmountDeg  # accumulate current joint position
        J3DegShow.delete(0., 'end')  # delete previous entry. The 0 must be a float
        J3DegShow.insert(END, j3CurrentDegPos)  # insert the current joint position
        jogAmountDeg = str(jogAmountDeg)  # convert back to string

    if jointJogging == '4':
        global j4CurrentDegPos  # must define the current position as a global variable to be modified
        jogAmountDeg = float(jogAmountDeg)  # convert to float from string
        j4CurrentDegPos = j4CurrentDegPos + jogAmountDeg  # accumulate current joint position
        J4DegShow.delete(0., 'end')  # delete previous entry. The 0 must be a float
        J4DegShow.insert(END, j4CurrentDegPos)  # insert the current joint position
        jogAmountDeg = str(jogAmountDeg)  # convert back to string

    if jointJogging == '5':
        global j5CurrentDegPos  # must define the current position as a global variable to be modified
        jogAmountDeg = float(jogAmountDeg)  # convert to float from string
        j5CurrentDegPos = j5CurrentDegPos + jogAmountDeg  # accumulate current joint position
        J5DegShow.delete(0., 'end')  # delete previous entry. The 0 must be a float
        J5DegShow.insert(END, j5CurrentDegPos)  # insert the current joint position
        jogAmountDeg = str(jogAmountDeg)  # convert back to string

    if jointJogging == '6':
        global j6CurrentDegPos  # must define the current position as a global variable to be modified
        jogAmountDeg = float(jogAmountDeg)  # convert to float from string
        j6CurrentDegPos = j6CurrentDegPos + jogAmountDeg  # accumulate current joint position
        J6DegShow.delete(0., 'end')  # delete previous entry. The 0 must be a float
        J6DegShow.insert(END, j6CurrentDegPos)  # insert the current joint position
        jogAmountDeg = str(jogAmountDeg)  # convert back to string

    if jointJogging == '7':
        global TCCurrentPercentPos  # must define the current position as a global variable to be modified
        jogAmountDeg = float(jogAmountDeg)  # convert to float from string
        TCCurrentPercentPos = TCCurrentPercentPos + jogAmountDeg  # accumulate current joint position
        TCDegShow.delete(0., 'end')  # delete previous entry. The 0 must be a float
        TCDegShow.insert(END, TCCurrentPercentPos)  # insert the current joint position
        jogAmountDeg = str(jogAmountDeg)  # convert back to string

    if jointJogging == 'X':
        global XCurrentPos  # must define the current position as a global variable to be modified
        jogAmountDeg = float(jogAmountDeg)  # convert to float from string
        XCurrentPos = XCurrentPos + jogAmountDeg  # accumulate current X position
        XPosShow.delete(0., 'end')  # delete previous entry. The 0 must be a float
        XPosShow.insert(END, XCurrentPos)  # insert the current joint position
        jogAmountDeg = str(jogAmountDeg)  # convert back to string

    if jointJogging == 'Y':
        global YCurrentPos  # must define the current position as a global variable to be modified
        jogAmountDeg = float(jogAmountDeg)  # convert to float from string
        YCurrentPos = YCurrentPos + jogAmountDeg  # accumulate current Y position
        YPosShow.delete(0., 'end')  # delete previous entry. The 0 must be a float
        YPosShow.insert(END, YCurrentPos)  # insert the current joint position
        jogAmountDeg = str(jogAmountDeg)  # convert back to string

    if jointJogging == 'Z':
        global ZCurrentPos  # must define the current position as a global variable to be modified
        jogAmountDeg = float(jogAmountDeg)  # convert to float from string
        ZCurrentPos = ZCurrentPos + jogAmountDeg  # accumulate current Z position
        ZPosShow.delete(0., 'end')  # delete previous entry. The 0 must be a float
        ZPosShow.insert(END, ZCurrentPos)  # insert the current joint position
        jogAmountDeg = str(jogAmountDeg)  # convert back to string




    functionValue = '<25>'  # change to whatever the jogging function number is
    jointJogging = ('<' + jointJogging + '>')
    jogAmountDeg = ('<' + jogAmountDeg + '>')
    teensy.write(functionValue.encode('utf-8'))  # Send teensy the function value to tell it to enter the jog function
    teensy.flushInput()
    teensy.write(jointJogging.encode('utf-8'))   # Send teensy the joint to be jogged
    teensy.flushInput()
    teensy.write(jogAmountDeg.encode('utf-8'))   # Send teensy amount to be jogged in degrees
    teensy.flushInput()

    return j1CurrentDegPos





















#############################################################
# Kinematics






#############################################################
# GUI and all components within it

# root GUI

root = Tk()
root.wm_title("MCARM Software")
root.resizable(width=True, height=True)
root.state('zoomed')  # Opens the window in windowed fullscreen
root.runTrue = 0




######################
# Tabs and Tab Labels

nb = tkinter.ttk.Notebook(root, width=2100, height=1200)
nb.place(x=0, y=0)

tab1 = tkinter.ttk.Frame(nb)
nb.add(tab1, text=' Main ')

tab2 = tkinter.ttk.Frame(nb)
nb.add(tab2, text=' Program ')

tab3 = tkinter.ttk.Frame(nb)
nb.add(tab3, text=' Log ')


mainTabLabel = Label(tab1, font = ("Arial", 22), text = "Main Controls")
mainTabLabel.place(x = 25, y = 60)

programTabLabel = Label(tab2, font = ("Arial", 22), text = "Program")
programTabLabel.place(x = 25, y = 60)

logTabLabel = Label(tab3, font = ("Arial", 22), text = "Log")
logTabLabel.place(x = 25, y = 60)


###############################
# Tab1 Main
####################################################################################################################################################




#################
# Main Functions

homeButton = Button(tab1, text = "Home", bg = "salmon", height = 4, width = 16, command = home)
homeButton.place(x = 360, y = 50)

calibrateButton = Button(tab1, text = "Calibrate", bg = "salmon", height = 4, width = 16, command = calibrate)
calibrateButton.place(x = 500, y = 50)

# fineCalibrateButton = Button(tab1, text = "Fine Calibrate", bg = "salmon", height = 4, width = 16, command = fineCalibrate)
# fineCalibrateButton.place(x = 600, y = 100)

restButton = Button(tab1, text = "Rest", bg = "salmon", height = 4, width = 16, command = restPosition)
restButton.place(x = 640, y = 50)

statusLabel = Label(tab1, font = ("Arial", 20), text = "Status")
statusLabel.place(x = 40, y = 220)

StatusOutput = Text(tab1, height = 55, width = 55, bg = "light cyan")
StatusOutput.place(x = 20, y = 270)

####################################
# Jog buttons, entries, and individual joint calibration
# The entry box will be +2 x from the buttons
# The spacing will be 120 x

degLabel = Label(tab1, font = ("Arial", 20), text = "Current degree position from home")
degLabel.place(x = 705, y = 480)


# J1
j1Label = Label(tab1, font = ("Arial", 18), text = "J1")
j1Label.place(x = 545, y = 270)

jogJ1Entry = Entry(tab1,width=12)
jogJ1Entry.place(x = 522, y = 383)

J1JogPosButton = Button(tab1, text = "J1 Jog +", bg = "lightblue", height = 2, width = 10, command = getJ1JogValPos)
J1JogPosButton.place(x = 520, y = 330)

J1JogNegButton = Button(tab1, text = "J1 Jog -", bg = "lightblue", height = 2, width = 10, command = getJ1JogValNeg)
J1JogNegButton.place(x = 520, y = 415)

J1CalibrateButton = Button(tab1, text = "J1 Calibrate", bg = "lightgreen", height = 2, width = 10, command = calibrateJ1)
J1CalibrateButton.place(x = 520, y = 605)

J1DegShow = Text(tab1, height = 1, width = 6, bg = "light cyan", font = ("Arial", 18))
J1DegShow.place(x = 519, y = 525)

# J2
j2Label = Label(tab1, font = ("Arial", 18), text = "J2")
j2Label.place(x = 665, y = 270)

jogJ2Entry = Entry(tab1,width=12)
jogJ2Entry.place(x = 642, y = 383)

J2JogPosButton = Button(tab1, text = "J2 Jog +", bg = "lightblue", height = 2, width = 10, command = getJ2JogValPos)
J2JogPosButton.place(x = 640, y = 330)

J2JogNegButton = Button(tab1, text = "J2 Jog -", bg = "lightblue", height = 2, width = 10, command = getJ2JogValNeg)
J2JogNegButton.place(x = 640, y = 415)

J2CalibrateButton = Button(tab1, text = "J2 Calibrate", bg = "lightgreen", height = 2, width = 10, command = calibrateJ2)
J2CalibrateButton.place(x = 640, y = 605)

J2DegShow = Text(tab1, height = 1, width = 6, bg = "light cyan", font = ("Arial", 18))
J2DegShow.place(x = 639, y = 525)

# J3
j3Label = Label(tab1, font = ("Arial", 18), text = "J3")
j3Label.place(x = 785, y = 270)

jogJ3Entry = Entry(tab1,width=12)
jogJ3Entry.place(x = 762, y = 383)

J3JogPosButton = Button(tab1, text = "J3 Jog +", bg = "lightblue", height = 2, width = 10, command = getJ3JogValPos)
J3JogPosButton.place(x = 760, y = 330)

J3JogNegButton = Button(tab1, text = "J3 Jog -", bg = "lightblue", height = 2, width = 10, command = getJ3JogValNeg)
J3JogNegButton.place(x = 760, y = 415)

J3CalibrateButton = Button(tab1, text = "J3 Calibrate", bg = "lightgreen", height = 2, width = 10, command = calibrateJ3)
J3CalibrateButton.place(x = 760, y = 605)

J3DegShow = Text(tab1, height = 1, width = 6, bg = "light cyan", font = ("Arial", 18))
J3DegShow.place(x = 759, y = 525)

# J4
j4Label = Label(tab1, font = ("Arial", 18), text = "J4")
j4Label.place(x = 905, y = 270)

jogJ4Entry = Entry(tab1,width=12)
jogJ4Entry.place(x = 882, y = 383)

J4JogPosButton = Button(tab1, text = "J4 Jog +", bg = "lightblue", height = 2, width = 10, command = getJ4JogValPos)
J4JogPosButton.place(x = 880, y = 330)

J4JogNegButton = Button(tab1, text = "J2 Jog -", bg = "lightblue", height = 2, width = 10, command = getJ4JogValNeg)
J4JogNegButton.place(x = 880, y = 415)

J4CalibrateButton = Button(tab1, text = "J4 Calibrate", bg = "lightgreen", height = 2, width = 10, command = calibrateJ4)
J4CalibrateButton.place(x = 880, y = 605)

J4DegShow = Text(tab1, height = 1, width = 6, bg = "light cyan", font = ("Arial", 18))
J4DegShow.place(x = 879, y = 525)

# J5
j5Label = Label(tab1, font = ("Arial", 18), text = "J5")
j5Label.place(x = 1025, y = 270)

jogJ5Entry = Entry(tab1,width=12)
jogJ5Entry.place(x = 1002, y = 383)

J5JogPosButton = Button(tab1, text = "J5 Jog +", bg = "lightblue", height = 2, width = 10, command = getJ5JogValPos)
J5JogPosButton.place(x = 1000, y = 330)

J5JogNegButton = Button(tab1, text = "J5 Jog -", bg = "lightblue", height = 2, width = 10, command = getJ5JogValNeg)
J5JogNegButton.place(x = 1000, y = 415)

J5CalibrateButton = Button(tab1, text = "J5 Calibrate", bg = "lightgreen", height = 2, width = 10, command = calibrateJ5)
J5CalibrateButton.place(x = 1000, y = 605)

J5DegShow = Text(tab1, height = 1, width = 6, bg = "light cyan", font = ("Arial", 18))
J5DegShow.place(x = 999, y = 525)

# J6
j6Label = Label(tab1, font = ("Arial", 18), text = "J6")
j6Label.place(x = 1145, y = 270)

jogJ6Entry = Entry(tab1,width=12)
jogJ6Entry.place(x = 1122, y = 383)

J6JogPosButton = Button(tab1, text = "J6 Jog +", bg = "lightblue", height = 2, width = 10, command = getJ6JogValPos)
J6JogPosButton.place(x = 1120, y = 330)

J6JogNegButton = Button(tab1, text = "J6 Jog -", bg = "lightblue", height = 2, width = 10, command = getJ6JogValNeg)
J6JogNegButton.place(x = 1120, y = 415)

J6CalibrateButton = Button(tab1, text = "J6 Calibrate", bg = "lightgreen", height = 2, width = 10, command = calibrateJ6)
J6CalibrateButton.place(x = 1120, y = 605)

J6DegShow = Text(tab1, height = 1, width = 6, bg = "light cyan", font = ("Arial", 18))
J6DegShow.place(x = 1119, y = 525)

# TC
TCLabel = Label(tab1, font = ("Arial", 18), text = "TC")
TCLabel.place(x = 1265, y = 270)

jogTCEntry = Entry(tab1,width=12)
jogTCEntry.place(x = 1242, y = 383)

TCJogPosButton = Button(tab1, text = "TC Jog +", bg = "lightblue", height = 2, width = 10, command = getTCJogValPos)
TCJogPosButton.place(x = 1240, y = 330)

TCJogNegButton = Button(tab1, text = "TC Jog -", bg = "lightblue", height = 2, width = 10, command = getTCJogValNeg)
TCJogNegButton.place(x = 1240, y = 415)

TCCalibrateButton = Button(tab1, text = "TC Calibrate", bg = "lightgreen", height = 2, width = 10, command = calibrateTC)
TCCalibrateButton.place(x = 1240, y = 605)

TCDegShow = Text(tab1, height = 1, width = 6, bg = "light cyan", font = ("Arial", 18))
TCDegShow.place(x = 1239, y = 525)

# X
XLabel = Label(tab1, font = ("Arial", 18), text = "X")
XLabel.place(x = 1385, y = 270)

jogXEntry = Entry(tab1,width=12)
jogXEntry.place(x = 1362, y = 383)

XJogPosButton = Button(tab1, text = "X Jog +", bg = "lightblue", height = 2, width = 10, command = getXJogValPos)
XJogPosButton.place(x = 1360, y = 330)

XJogNegButton = Button(tab1, text = "X Jog -", bg = "lightblue", height = 2, width = 10, command = getXJogValNeg)
XJogNegButton.place(x = 1360, y = 415)

XPosShow = Text(tab1, height = 1, width = 6, bg = "light cyan", font = ("Arial", 18))
XPosShow.place(x = 1359, y = 525)

# Y
YLabel = Label(tab1, font = ("Arial", 18), text = "Y")
YLabel.place(x = 1505, y = 270)

jogYEntry = Entry(tab1,width=12)
jogYEntry.place(x = 1482, y = 383)

YJogPosButton = Button(tab1, text = "Y Jog +", bg = "lightblue", height = 2, width = 10, command = getYJogValPos)
YJogPosButton.place(x = 1480, y = 330)

YJogNegButton = Button(tab1, text = "Y Jog -", bg = "lightblue", height = 2, width = 10, command = getYJogValNeg)
YJogNegButton.place(x = 1480, y = 415)

YPosShow = Text(tab1, height = 1, width = 6, bg = "light cyan", font = ("Arial", 18))
YPosShow.place(x = 1479, y = 525)

# Z
ZLabel = Label(tab1, font = ("Arial", 18), text = "Z")
ZLabel.place(x = 1625, y = 270)

jogZEntry = Entry(tab1,width=12)
jogZEntry.place(x = 1602, y = 383)

ZJogPosButton = Button(tab1, text = "Z Jog +", bg = "lightblue", height = 2, width = 10, command = getZJogValPos)
ZJogPosButton.place(x = 1600, y = 330)

ZJogNegButton = Button(tab1, text = "Z Jog -", bg = "lightblue", height = 2, width = 10, command = getZJogValNeg)
ZJogNegButton.place(x = 1600, y = 415)

ZPosShow = Text(tab1, height = 1, width = 6, bg = "light cyan", font = ("Arial", 18))
ZPosShow.place(x = 1599, y = 525)







#############################################################
# Run Program

startTeensy()  # Used with Teensy as it doesn't reboot whenever python starts communication. Need to wait until python tells it to start
waitForTeensy()

tab1.mainloop()

functionValue = '999'
sendToTeensy(functionValue)
print("Program ended")

