from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics


class LaserGuidedV3(AI.SuperAI):
    "spinning weapon monted on servo motor tend to aim toward ennemy bot"
    name = "LaserGuidedV3"
    # brought  to you by PhiletBabe with the help of the incredible Madiaba
    # same as laserGuided but use Madiaba SMFE_TurretMachinGun Aiming functions
    # binding :
    #mayFire :True if piston or burst motor attached to servo
    # servonose : angle factor  of attachement of extender to the servo ( typical value 1,-1, 0,25,0.5, -0,25, -0.5)
    #    list.append(("myBotName","LaserGuidedV3",{ 'servonose':1, 'range':80, 'radius':0.5, 'servospeed':60, 'topspeed':99, 'mayFire':False, 'throttle':130,'weapons':(1,2,3,4,5,6,7,8,9)}))
    # name of Servo controler is 'Servo'
    # name of Firind controler attached to servo is 'ServoFire'

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.triggers1 = ["ServoFire"]
        self.mayFire = True
        self.servospeed = 100 # speed of servo motor
        self.armlength = 3 # not used,
        self.delta = 0.2 #tolerance between full Aim
        self.Motor = 1
        self.servoNose = 1 # servoNose is a factor from -1 to 1 that take into account the fact that the components attached to the
                           # servo motor are not always attached to its straight heading
        self.spin_range = 3.0 # used if you mount a spin motor onn your servo motor
        self.servo_range = 3.5 # use if you want to use the servoFire trigger
        if 'range' in args:
            self.spin_range = args.get('range')
        if 'zone' in args: self.zone = args['zone']
        if 'servospeed' in args: self.servospeed=args['servospeed']
        if 'delta' in args: self.delta=args['delta']
        if 'servorange' in args: self.servo_range=args['servorange']
        if 'mayfire' in args: self.mayFire = args['mayfire']
        if 'servonose' in args: self.servoNose = args['servonose']
        # to display the current angle of the servo motor uncomment thoses lines :
        self.debug = False
        AI.SuperAI.debugging = False
        self.tactics.append(Tactics.Engage(self))

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
            #define identifier of servo-motor
            goon = 1
            i = 0
            while goon == 1:
                if i  == self.GetNumComponents(): break
                currentType =  self.GetComponentType(i)
                if currentType == "ServoMotor": self.Motor = i
                i = i+ 1

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        enemy, range = self.GetNearestEnemy()
        # if  spinner in range :  do spin :
        if enemy is not None and range < self.spin_range:
            self.Input("Spin", 0, 1)
        elif self.GetInputStatus("Spin", 0) != 0:
            self.Input("Spin", 0, 0)

        if enemy != None :
            # time to move or fire the laser Guided (ser -motor mounted) gun :
            enemyHead = self.GetHeadingToID(enemy, False)
            selfangle = self.servoNose * self.GetMotorAngle(self.Motor)
            Winkel = ( enemyHead - selfangle)
            if self.debug :
                self.DebugString(5, "winkel : " + str(Winkel))
                self.DebugString(6, "range : " + str(range))
            if self.AimTowards(Winkel):
                # if range <=  range of the mounted gun
                # LaserGuided gun aim ennemy : par Saint Georges ! Montjoie ! Saint Denis ! pas de quartier !
                if range <= self.servo_range and self.mayFire : self.Input("ServoFire", 0, 1)

        return AI.SuperAI.Tick(self)

    def Aim(self, level):

        level = min(max(level, -self.servospeed), self.servospeed)
        self.Input('Servo', 0, level)


    def AimTowards(self, heading):
        dreh = 0

        if (heading < -self.delta or heading > self.delta):

            dire = -1
            if heading < 0: dire = 1

            h = min(abs(heading), 1.75)
            dreh = dire * (int((h / 1.5) * 100)+20)

            self.Aim(  dreh)
            return False
        else:
            self.Aim(0)
            return True

    def InvertHandler(self):
        # fire weapon once per second (until we're upright!)
        while 1:
            self.Input("Srimech", 0, 2)

            for i in range(0, 8):
                yield 0


    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)

        if not self.weapons:
            tactic = [x for x in self.tactics if x.name == "Engage"]
            if len(tactic) > 0:
                self.tactics.remove(tactic[0])

                self.tactics.append(Tactics.Shove(self))
                self.tactics.append(Tactics.Charge(self))

        return AI.SuperAI.LostComponent(self, id)

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


AI.register(LaserGuidedV3)

