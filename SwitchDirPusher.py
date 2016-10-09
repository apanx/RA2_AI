from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from SwitchDirRam import SwitchDirRam

class SwitchDirPusher(SwitchDirRam):
    "Attacks with the back when the front weapon breaks.  Uses Shove tactic."
    name = "SwitchDirPusher"
    #Slight modification of Click's SwitchDirRam, brought to you by Naryar. Simply changes from Rammer to Pusher.

    def __init__(self, **args):
        SwitchDirRam.__init__(self, **args)
        tactic = [x for x in self.tactics if x.name == "Ram"]
        if len(tactic) > 0:
            self.tactics.remove(tactic[0])
        self.tactics.append(Tactics.Charge(self))
        self.tactics.append(Tactics.Shove(self))
    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Shove tactic and switch to ReverseRam
        if id in self.weapons: self.weapons.remove(id)
        if id in self.sweapons: self.sweapons.remove(id)

        if not self.weapons and self.sweapons:
            tactic = [x for x in self.tactics if x.name == "Shove"]
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

AI.register(SwitchDirPusher)