from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import operator
import Tactics

class SpinupOmni2(AI.SuperAI):
    "Waits for weapon to spin up before moving.  Also reverses weapon if it gets jammed."
    name = "SpinupOmni2"
    # Update 7/24/12: Fixed AI not moving to avoid immobility when the weapon is jammed.
    # ***CUSTOMIZABLE SETTINGS*** #
    # 'ticks' sets how many times per tick the AI checks its RPM (Revolutions Per Minute) (a tick is 1/8 second).  Needs to be high for accurate measurements on fast spinners, but too high causes lag.  Default is 3.75 (=30 times/second).
    # ***NOTE*** RA2 can't measure times less than 1/30 second.  Therefore the RPM calculator is only accurate for speeds of 1500, 750, 500, 375, 300, and <250 RPM.  Speeds over 1500 RPM can't be measured, and accuracy decreases with increasing RPM.
    # 'MotorID' tells the AI which motor to measure RPM on.
    # 'Motor2ID' (Optional) Set ID for a second motor to measure RPM on.
    # 'TargetRPM' is the RPM the weapon needs to be spinning at before the AI will move.  (With two motors, only one needs to exceed the target RPM.)  Default is 100.
    # 'DisplayRPM' Set this to 1 to display current RPM, average RPM, and maximum RPM during battle.  Use this to determine ticks and TargetRPM values.
    # 'JamTime' Sets the amount of time (in seconds) the weapon should be jammed for, before reversing the direction in an attempt to unjam it.  For unidirectional weapons, just set to 999.  Default is 1.5.

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.zone = "weapon"
        self.triggers = ["Fire"]
        self.trigger2 = ["Srimech"]
        self.reloadTime = 0
        self.reloadDelay = 3
        self.tickFactor = 3.75
        self.spin_range = 3.0
        self.motorID = 2
        self.motorID2 = -1
        self.RPM = 0
        self.RPM2 = 0
        self.revolution = 0
        self.revolution2 = 0
        self.measuring = 0
        self.measuring2 = 0
        self.max_RPM = 0
        self.RPMhist = []
        self.avg_RPM = 0
        self.display = 0
        self.targetRPM = 100
        self.spin_reverse = 0
        self.jamTimer = 0
        self.raspberry = 1.5
        self.stopFunction = self.Stop

        if 'range' in args:
            self.spin_range = args.get('range')

        if 'triggers' in args: self.triggers = args['triggers']
        if 'reload' in args: self.reloadDelay = args['reload']
        if 'ticks' in args: self.tickFactor = args['ticks']
        if 'MotorID' in args: self.motorID = args['MotorID']
        if 'Motor2ID' in args: self.motorID2 = args['Motor2ID']
        if 'DisplayRPM' in args: self.display = args['DisplayRPM']
        if 'TargetRPM' in args: self.targetRPM = args['TargetRPM']
        if 'JamTime' in args: self.raspberry = args['JamTime']

        self.triggerIterator = iter(self.triggers)

        self.tactics.append(Tactics.Engage(self))

    def Activate(self, active):
        plus.AI.__setattr__tickInterval__(self, 0.125/self.tickFactor)
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 75, 100, 75)
                tbox = self.debug.addText("line0", 0, 0, 100, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 100, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 0, 30, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 100, 15)
                tbox.setText("")
            if self.display != 0:
                self.tauntbox = Gooey.Plain("taunt", 10, 175, 640, 175)
                tbox = self.tauntbox.addText("taunt1", 10, 0, 640, 15)
                tbox.setText("")
                tbox2 = self.tauntbox.addText("taunt2", 10, 20, 640, 15)
                tbox2.setText("")
                tbox3 = self.tauntbox.addText("taunt3", 10, 40, 640, 15)
                tbox3.setText("")
                tbox4 = self.tauntbox.addText("taunt4", 10, 60, 640, 15)
                tbox4.setText("")

            self.RegisterSmartZone(self.zone, 1)
        else:
            # get rid of reference to self
            self.stopFunction = None

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        if self.display != 0:
            self.tauntbox.get("taunt1").setText(str(self.RPM) + " RPM")
            if self.motorID2 > 0:
                self.tauntbox.get("taunt2").setText(str(self.RPM2) + " RPM (Motor 2)")
            else:
                self.tauntbox.get("taunt2").setText("No motor 2.")
            self.tauntbox.get("taunt3").setText("Average RPM: "+str(self.avg_RPM))
            self.tauntbox.get("taunt4").setText("Maximum RPM: "+str(self.max_RPM))

        #Measure RPM
        if (self.GetMotorAngle(self.motorID) > math.pi/3 or self.GetMotorAngle(self.motorID) < 0) and self.measuring == 0:
            self.revolution = plus.getTimeElapsed()
            self.measuring = 1

        if 0 < self.GetMotorAngle(self.motorID) < math.pi/3 and self.measuring == 1:
            self.RPM = 50/(plus.getTimeElapsed() - self.revolution)
            if self.display != 0:
                self.RPMhist.append(self.RPM)
                if self.RPM > self.max_RPM:
                    self.max_RPM = self.RPM
            self.measuring = 0

        if self.motorID2 > 0:
            #Measure RPM of second motor
            if (self.GetMotorAngle(self.motorID2) > math.pi/3 or self.GetMotorAngle(self.motorID2) < 0) and self.measuring2 == 0:
                self.revolution2 = plus.getTimeElapsed()
                self.measuring2 = 1

            if 0 < self.GetMotorAngle(self.motorID2) < math.pi/3 and self.measuring2 == 1:
                self.RPM2 = 50/(plus.getTimeElapsed() - self.revolution2)
                if self.display != 0:
                    self.RPMhist.append(self.RPM2)
                    if self.RPM2 > self.max_RPM:
                        self.max_RPM = self.RPM2
                self.measuring2 = 0

        if len(self.RPMhist) > 0:
            self.avg_RPM = reduce(operator.add, self.RPMhist)/len(self.RPMhist)

        # fire weapon

        # spin up depending on enemy's range
        enemy, range = self.GetNearestEnemy()

        if enemy is not None and range < self.spin_range:
            if self.spin_reverse == 0:
                self.Input("Spin", 0, 100)
            if self.spin_reverse == 1:
                self.Input("Spin", 0, -100)
        elif self.GetInputStatus("Spin", 0) != 0:
            self.Input("Spin", 0, 0)

        # Optional turning control to aid in self righting
        if self.IsUpsideDown() and not self.bInvertible:
            self.Input("Sridrive", 0, 100)
        else:
            self.Input("Sridrive", 0, 0)

        # Try reversing weapons if they get jammed
        if plus.getTimeElapsed() - self.revolution > self.raspberry or (self.motorID2 > 0 and plus.getTimeElapsed() - self.revolution2 > self.raspberry):
            self.jamTimer += 1
        else:
            self.jamTimer = 0

        if self.jamTimer >= 24*self.tickFactor and self.spin_reverse == 0:
            self.spin_reverse = 1
            self.jamTimer = 0

        if self.jamTimer >= 24*self.tickFactor and self.spin_reverse == 1:
            self.spin_reverse = 0
            self.jamTimer = 0

        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
            and not plus.isDefeated(x.robot)]

        if self.weapons:
            # slight delay between firing
            if self.reloadTime > 0: self.reloadTime -= 1

            if len(targets) > 0 and self.reloadTime <= 0:
                try:
                    trigger = self.triggerIterator.next()
                except StopIteration:
                    self.triggerIterator = iter(self.triggers)
                    trigger = self.triggerIterator.next()

                self.Input(trigger, 0, 1)
                self.reloadTime = self.reloadDelay

        bReturn = AI.SuperAI.Tick(self)

        # call this now so it takes place after other driving commands
        if self.stopFunction: self.stopFunction(len(targets) > 0)

        return bReturn

    def Stop(self, bTarget):
        # stay put if weapon isn't spinning fast
        if self.weapons and not self.bImmobile and (self.RPM < self.targetRPM or (self.motorID2 > 0 and self.RPM2 < self.targetRPM)):
            self.Throttle(0)
        # stay put if the weapon is jammed, to give it a chance to unjam
        if (plus.getTimeElapsed() - self.revolution > self.raspberry or (self.motorID2 > 0 and plus.getTimeElapsed() - self.revolution2 > self.raspberry)) and not self.bImmobile:
            self.Throttle(0)

    def StuckHandler(self):
        "This default generator is called when the bot is almost immobile."
        while 1:
            # back up for 2 seconds (will stop once we're not immobile)
            for i in range(0, 16*self.tickFactor):
                pos = vector3(self.GetLocation())
                dir = vector3(self.GetDirection())
                self.DriveToLocation((pos - dir * 3).asTuple(), True)
                yield 0
            # go forward for 2 seconds
            for i in range(0, 16*self.tickFactor):
                pos = vector3(self.GetLocation())
                dir = vector3(self.GetDirection())
                self.DriveToLocation((pos + dir * 3).asTuple())
                yield 0

    def Think(self):
        self.Evaluate()
        self.countdownToEvaluation = 8*self.tickFactor
        # shut down motors while we think
        self.Throttle(0)
        self.Turn(0)

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)

            for i in range(0, 8*self.tickFactor):
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

AI.register(SpinupOmni2)