from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class Thwack3(AI.SuperAI):
    "Same as FBS_2 but modified to better suit T-Wrex style thwack/rammer hybrids."
    # Uses standard 'LeftRight' control for spinning.  'Spin' button for active weapons.  'Trinity' button for activating Trinity glitch pistons.
    # Use 'sweapons' to designate ONLY the thwacking tail weapons--the AI will stop thwacking when these break.
    # Use 'weapons' to designate ALL weapons, front and back.
    ### BINDINGS SETTINGS ###
    # 'range' is the range for spinning weapons.
    # 'fbs_range' is the range for full-body spinning.
    # 'PreSpinEntrance' is a time at the beginning of the match the AI won't spin, to get further in the arena.
    # 'clockwise' value of 1 makes the full-body spin direction right/clockwise.  Any other value makes it left/counterclockwise.
    # 'chase_time' is the time interval in seconds with no hits after which the AI will stop spinning temporarily and chase down the opponent.
    # 'Pulse' is the number of ticks the active weapon should stay on PLUS the number of ticks it stays off.  A tick is 1/8 second.
    # 'Coast' is the number of ticks the active weapon should turn off and coast for.  This should be less than the Pulse value.  For equal times on/off, set Coast equal to half of Pulse.
    # 'SRcycle' is the number of ticks the weapon should spin in one direction before reversing when attempting to self right.
    # NOTE:  You must have the correct ID numbers of the bot's weapons in Bindings.py for the chase_time feature to work!!!
    name = "Thwack3"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        if 'tactic' in args:
            self.theTactic = args['tactic']
            if   self.theTactic  == "Charge" : self.tactics.append(Tactics.Charge(self))
            elif self.theTactic  == "Ram" : self.tactics.append(Tactics.Ram(self))
            elif self.theTactic  == "Shove" : self.tactics.append(Tactics.Shove(self))
            elif self.theTactic  == "Engage" : self.tactics.append(Tactics.Engage(self))
        else: self.tactics.append(Tactics.Engage(self))

        self.spin_range = 50
        self.turn_range = 3
        self.PreSpinEntrance = 0
        self.turnreset = 0
        if 'PreSpinEntrance' in args: self.PreSpinEntrance = args.get('PreSpinEntrance')
        self.PreSpinEntranceTimer = 0
        self.timeOfLastBadHit = 0
        self.TimeSinceHit = 0
        self.ChaseTime = 60
        self.cycle = 0
        self.cycletime = 16
        if 'chase_time' in args:
            self.ChaseTime = args.get('chase_time')
        if 'range' in args:
            self.spin_range = args.get('range')
        if 'fbs_range' in args:
            self.turn_range = args.get('fbs_range')
        if 'SRcycle' in args:
            self.cycletime = args.get('SRcycle')

        self.thwackFunction = self.ThwackLeft

        if 'clockwise' in args: self.thwackFunction = self.ThwackRight

        self.pulsetime = 0
        if 'Pulse' in args: self.pulsetime = args.get('Pulse')
        self.pulse = self.pulsetime
        if 'Coast' in args: self.pulsetime2 = args.get('Coast')

    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 10, 175, 250, 175)
                tbox = self.debug.addText("line0", 10, 0, 100, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 10, 15, 100, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 10, 30, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 10, 45, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line4", 10, 60, 250, 15)
                tbox.setText("")
        else:
            # get rid of reference to self
            self.thwackFunction = None

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        #self.DebugString(4, "self.TimeSinceHit: "+  str(self.TimeSinceHit))

        # Jut out initially.
        if self.PreSpinEntranceTimer < self.PreSpinEntrance:
            self.PreSpinEntranceTimer += 1

        # Keep track of last time we got hit, ignoring small damage from walls and stuff.
        if self.GetLastDamageReceived()[1] > 100:
            self.timeOfLastBadHit = self.GetLastDamageReceived()[2]

        # Count time since last hit
        self.TimeSinceHit = min((plus.getTimeElapsed() - self.timeOfLastGoodHit), (plus.getTimeElapsed() - self.timeOfLastBadHit))

        #Self right
        if self.IsUpsideDown() and not self.bInvertible:
            self.cycle += 1
            if self.cycle <= self.cycletime/2:
                self.Input("Spin", 0, 100)
            if self.cycle > self.cycletime/2:
                self.Input("Spin", 0, -100)
            if self.cycle >= self.cycletime:
                self.cycle = 0
        else:
            self.cycle = 0

        # define targets
        targets = []

        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
            and not plus.isDefeated(x.robot)]

        bReturn = AI.SuperAI.Tick(self)

        # call this now so it takes place after other driving commands
        if self.thwackFunction: self.thwackFunction(len(targets) > 0)

        return bReturn

    def ThwackLeft(self, bTarget):
        if self.sweapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if not self.bImmobile:
                if self.pulsetime > 0:
                    # Keep spinner on constantly when we're thwacking
                    if enemy is not None and range < self.spin_range and range < self.turn_range and self.TimeSinceHit <= self.ChaseTime:
                        self.Input("Spin", 0, 100)
                        # Reset pulse timer
                        self.pulse = self.pulsetime
                    elif (enemy is not None and range < self.spin_range and range > self.turn_range) or (enemy is not None and range < self.spin_range and range < self.turn_range and self.TimeSinceHit > self.ChaseTime):
                        # Pulse spinner
                        self.pulse -= 1
                        if self.pulsetime2 < self.pulse < self.pulsetime:
                            self.Input("Spin", 0, 100)
                            self.Throttle(0)
                            self.Turn(0)
                        if 0 < self.pulse < self.pulsetime2:
                            self.Input("Spin", 0, 0)
                        if self.pulse <= 0:
                            self.pulse = self.pulsetime
                    elif self.GetInputStatus("Spin", 0) != 0:
                        self.Input("Spin", 0, 0)
                else:
                    if enemy is not None and range < self.spin_range:
                        self.Input("Spin", 0, 100)
                    elif self.GetInputStatus("Spin", 0) != 0:
                        self.Input("Spin", 0, 0)
            else:
                if self.bInvertible or not self.IsUpsideDown():
                    self.Input("Spin", 0, 0)

            # Full body spin if we're in range, not immobile, out of our starting spot, and still hitting stuff.
            if enemy is not None and range < self.turn_range and self.PreSpinEntranceTimer >= self.PreSpinEntrance and self.TimeSinceHit <= self.ChaseTime and not self.bImmobile:
                if self.IsUpsideDown() and self.bInvertible:
                    self.Turn(100)
                else:
                    self.Turn(-100)
                self.Input("Trinity", 0, 1)
                self.turnreset = 0
            else:
                if self.turnreset == 0:
                    self.Turn(0)
                    self.turnreset = 1

    def ThwackRight(self, bTarget):
        if self.sweapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if not self.bImmobile:
                if self.pulsetime > 0:
                    # Keep spinner on constantly when we're thwacking
                    if enemy is not None and range < self.spin_range and range < self.turn_range and self.TimeSinceHit <= self.ChaseTime:
                        self.Input("Spin", 0, 100)
                        # Reset pulse timer
                        self.pulse = self.pulsetime
                    elif (enemy is not None and range < self.spin_range and range > self.turn_range) or (enemy is not None and range < self.spin_range and range < self.turn_range and self.TimeSinceHit > self.ChaseTime):
                        # Pulse spinner
                        self.pulse -= 1
                        if self.pulsetime2 < self.pulse < self.pulsetime:
                            self.Input("Spin", 0, 100)
                            self.Throttle(0)
                            self.Turn(0)
                        if 0 < self.pulse < self.pulsetime2:
                            self.Input("Spin", 0, 0)
                        if self.pulse <= 0:
                            self.pulse = self.pulsetime
                    elif self.GetInputStatus("Spin", 0) != 0:
                        self.Input("Spin", 0, 0)
                else:
                    if enemy is not None and range < self.spin_range:
                        self.Input("Spin", 0, 100)
                    elif self.GetInputStatus("Spin", 0) != 0:
                        self.Input("Spin", 0, 0)
            else:
                if self.bInvertible or not self.IsUpsideDown():
                    self.Input("Spin", 0, 0)

            # Full body spin if we're in range, not immobile, out of our starting spot, and still hitting stuff.
            if enemy is not None and range < self.turn_range and self.PreSpinEntranceTimer >= self.PreSpinEntrance and self.TimeSinceHit <= self.ChaseTime and not self.bImmobile:
                if self.IsUpsideDown() and self.bInvertible:
                    self.Turn(-100)
                else:
                    self.Turn(100)
                self.Input("Trinity", 0, 1)
                self.turnreset = 0
            else:
                if self.turnreset == 0:
                    self.Turn(0)
                    self.turnreset = 1

    def LostComponent(self, id):
        if id in self.weapons: self.weapons.remove(id)
        if id in self.sweapons: self.sweapons.remove(id)

        return AI.SuperAI.LostComponent(self, id)

    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)
            elif id == 4: self.debug.get("line4").setText(string)

AI.register(Thwack3)
