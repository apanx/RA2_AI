from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
import time
from Omni import Omni

class OmniServo(Omni):
    "Omni strategy with use of 1 servo motor"
    name = "OmniServo"
# ==============================================================
# class omni servo : like omni AI but allow the monitoring of 1 servo motor.
# the servo motor may be mount to spin horizontaly or verticvaly
# minimum binding.py declaration :    list.append(("mBotName","OmniServo",{'weapons':( 1)}))
# maximum binding.py declaration :   list.append(("myBotName","OmniServo",{'minangle':value, 'maxangle':value, 'servoVS':value,
#  'delta':value, 'servospeed':value,'weapons':(1)}))
# role of arguments and default value
#  minangle : angle the servo motor tries to reach when ennemy bot in custom zone named 'zoneservo2'. Default : 0 (radian)
#  maxangle : angle the servo motor tries to reach when ennemy bot in custom zone named 'zoneservo1'. Default: math.pi (radian)
# servospeed :  speed of the servo motor.  Default : 30 (hight for a servo !)
# delta :  servo motor is rarely equal to minangle or maxangle, so the servomotor oscillate widly  (like the beautiful music of 'the smiths'.) around theses angles
#           the value of delta define how wide the servo motor will oscillate. the higher, the wider. Default : 0.2 (radian)
# servoVS : mostly use if the servo motor spin verticaly : may autorize only positive of negatives angles. Useful for the realistic rules.
#              servoVS = 1 : only positives angles / servoVS = -1 : only negatives values / ServoVS = 0 : no control. Default : 0
#
# bot construction : must have a servo-motor controler  named 'Servo'.
#                           must have 2 custom zones named 'zoneservo1' and 'zoneservo2'
#                           must have only 1 servo motor in its components, otherwise only the last one will be controlled.
#  note1 :  RA2 angles goes from -math.pi to Math.pi. spinning clockwise (positive servospeed) decrease angle.
#  note2:  seems to have problem when stopping servo ( selfinput("Servo",0,0) )
#  note3:  sometime your bot may fly, lovely but fully useless
# note4: give bad result when others custom zones (ie 'weapon'for piston or 'flip' )  exists
# author : PhiletBabe supported by the irreplaceable Madiaba. 2008
# ==============================================================

    def __init__(self, **args):
        Omni.__init__(self, **args)
        # declare  zone and variables associated with the servo motor :
        self.zone2 = "zoneservo1"
        self.zone3 = "zoneservo2"
        # declare the Id of the motor, and angle of turn
        self.motor = 1
        self.minangle = 0
        self.maxangle = math.pi
        self.servospeed = 30
        # servoVS = 1 indicates that the servo spin vertically : do  not authorized negative servo motor angle
        # servoVS = -1 indicates that the servo spin vertically : do  not authorized positive servo motor angle
        # servoVS = 0 : no restriction to servo angle motor. Default value.
        self.servoVS = 0
        #read theses values from bindings.py :
        if 'minangle' in args: self.minangle = args['minangle']
        if 'maxangle' in args: self.maxangle = args['maxangle']
        if self.minangle > self.maxangle:
            xxx = self.minangle
            self.minangle = self.maxangle
            self.maxangle = xxx
        if 'servoVS' in args: self.servoVS = args['servoVS']
        if 'servospeed' in args: self.servospeed = args['servospeed']
        self.delta = 0.3
        if 'delta' in args: self.delta = args['delta']
        # to display the current angle of the servo motor uncomment thoses lines :
        #AI.SuperAI.debugging = True


    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 150, 250, 240)
                tbox = self.debug.addText("line0", 0, 0, 250, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 250, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 0, 30, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line4", 0, 60, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line5", 0, 75, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line6", 0, 90, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line7", 0, 105, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line8", 0, 120, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line9", 0, 135, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line10", 0, 150, 250, 15)
                tbox.setText("")
            # standard smart zone :
            self.RegisterSmartZone(self.zone, 1)
            self.RegisterSmartZone(self.zone2, 2)
            self.RegisterSmartZone(self.zone3, 3)
            #define identifier of servo-motor
            for i in range(self.GetNumComponents()):
                currentType =  self.GetComponentType(i)
                if currentType == "ServoMotor": self.motor = i

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon
        bReturn = Omni.Tick(self)
        if self.weapons:
            servoangle = self.GetMotorAngle(self.motor)
            self.DebugString(10, "Current servo motor angle : " + str(servoangle))

        servoangle = self.GetMotorAngle(self.motor)
        self.DebugString(10, "servo motor angle :" + str(servoangle))
        if ( self.servoVS == 1 ) and ( servoangle < 0):
            if ( servoangle > -math.pi/2):
                self.Input("Servo", 0, -15)
            else:
                self.Input("Servo", 0, 15)
        elif ( self.servoVS == -1 ) and ( servoangle > 0):
            if ( servoangle > math.pi/2):
                self.Input("Servo", 0, -15)
        else:
            self.Input("Servo", 0, 0)

        return bReturn


    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)
            elif id == 6: self.debug.get("line6").setText(string)
            elif id == 7: self.debug.get("line7").setText(string)
            elif id == 8: self.debug.get("line8").setText(string)
            elif id == 9: self.debug.get("line9").setText(string)
            elif id == 10: self.debug.get("line10").setText(string)
            elif id == 11: self.debug.get("line11").setText(string)
            elif id == 12: self.debug.get("line12").setText(string)
            elif id == 13: self.debug.get("line13").setText(string)
            elif id == 14: self.debug.get("line14").setText(string)
            elif id == 15: self.debug.get("line15").setText(string)

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if direction == 1:
                AI.SuperAI.SmartZoneEvent(self, direction, id, robot, chassis)
        elif id == 2:
            if robot > 0:
                if direction == 1:
                    # if not already well-positionned : move servo motor :
                    servoangle = self.GetMotorAngle(self.motor)
                    if servoangle < (self.maxangle -self.delta): self.Input("Servo", 0, -self.servospeed)
                    elif servoangle > (self.maxangle+ self.delta): self.Input("Servo", 0, self.servospeed)
                    #else: self.Input("Servo", 0, 0)
        elif id == 3:
            if robot > 0:
                if direction == 1:
                    # if not already well-positionned : move servo motor :
                    servoangle = self.GetMotorAngle(self.motor)
                    if servoangle > (self.minangle + self.delta): self.Input("Servo", 0, self.servospeed)
                    elif servoangle < (self.minangle - self.delta): self.Input("Servo", 0, -self.servospeed)
                    #else: self.Input("Servo", 0, -self.servospeed)

        return True

AI.register(OmniServo)
