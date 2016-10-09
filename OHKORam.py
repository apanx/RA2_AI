from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class OHKORam(Omni):
    "Rammer that waits for all wheels to touch the ground before driving in order to hit the opponent perfectly head-on."
    # Set the start-of-game wait time with 'waittime' in Bindings.  Units are seconds.
    name = "OHKORam"
    #Made by Clickbeetle for R17. Is in fact an OmniRam.py

    def __init__(self, **args):
        Omni.__init__(self, **args)

        self.stopFunction = self.Stop
        self.waittime = 0.5

        if 'waittime' in args:
            self.waittime = args.get('waittime')

        tactic = [x for x in self.tactics if x.name == "Engage"]
        if len(tactic) > 0:
            self.tactics.remove(tactic[0])
        self.tactics.append(Tactics.Ram(self))

    def Activate(self, active):
        bReturn = Omni.Activate(self, active)
        if not active:
            # get rid of reference to self
            self.stopFunction = None

        return bReturn

    def Tick(self):
        # fire srimech here - allows us to be invertible and use srimech at the same time
        if self.IsUpsideDown():
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)

        bReturn = Omni.Tick(self)

        # call this now so it takes place after other driving commands
        if self.stopFunction: self.stopFunction()

        return bReturn

    def Stop(self):
        #wait for the bot to settle before charging
        if plus.getTimeElapsed() < self.waittime:
            self.Throttle(0)

AI.register(OHKORam)