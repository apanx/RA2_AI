from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class SwitchDirRam(Omni):
    "Attacks with the back when the front weapon breaks.  Uses Ram tactic."
    name = "SwitchDirRam"

    def __init__(self, **args):
        Omni.__init__(self, **args)

        self.originose = self.fNoseOffset

        tactic = [x for x in self.tactics if x.name == "Engage"]
        if len(tactic) > 0:
            self.tactics.remove(tactic[0])

        self.tactics.append(Tactics.Ram(self))

    def Tick(self):
        #self.tauntbox.get("taunt1").setText("Nose: " + str(self.fNoseOffset))
        # this doesn't seem to do anything, but what the heck, it's not doing any harm either.
        #if plus.getTimeElapsed() > 3 and self.fNoseOffset == self.originose:
        if not self.weapons and self.fNoseOffset == self.originose:
            self.fNoseOffset += math.pi
        bReturn = Omni.Tick(self)
        return bReturn

    def Throttle(self, throttle):
        # if we're car steering and we're not moving much, throttle up
        if self.bCarSteering and self.last_turn_throttle != 0:
            speed = self.GetSpeed()
            if speed > 0 and speed < self.top_speed / 3: throttle = self.last_throttle + 10
            elif speed < 0 and speed > -self.top_speed / 3: throttle = self.last_throttle - 10

        throttle = min(max(throttle, -100), 100)

        if self.bInvertible and self.IsUpsideDown(): throttle = -throttle
        #reverse throttle if weapons break
        if not self.weapons: throttle = -throttle
        #reset throttle if secondary weapons break
        if not self.sweapons: throttle = -throttle

        self.set_throttle = throttle
        self.Input('Forward', 0, throttle)
        self.DebugString(0, "Throttle = " + str(int(throttle)))

    def Turn(self, turning):
        turning = min(max(turning, -100), 100)

        if self.bInvertible and self.IsUpsideDown(): turning = -turning
        #reverse turning if weapons break
        if not self.weapons: turning = -turning
        #reset turning if secondary weapons break
        if not self.sweapons: turning = -turning

        self.set_turn_throttle = turning
        self.Input('LeftRight', 0, -turning)
        self.Input('LeftRight', 1, turning)
        self.DebugString(1, "Turning = " + str(int(turning)))



    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Ram tactic and switch to ReverseRam
        if id in self.weapons: self.weapons.remove(id)
        if id in self.sweapons: self.sweapons.remove(id)

        if not self.weapons and self.sweapons:
            tactic = [x for x in self.tactics if x.name == "Ram"]
            if len(tactic) > 0:
                self.tactics.remove(tactic[0])

                self.tactics.append(Tactics.ReverseRam(self))

        if not self.weapons and not self.sweapons:
            tactic = [x for x in self.tactics if x.name == "ReverseRam"]
            if len(tactic) > 0:
                self.tactics.remove(tactic[0])

                self.tactics.append(Tactics.Shove(self))
                self.tactics.append(Tactics.Charge(self))

        return AI.SuperAI.LostComponent(self, id)

AI.register(SwitchDirRam)