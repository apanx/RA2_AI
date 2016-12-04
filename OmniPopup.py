from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Popup import Popup

class OmniPopup(Popup):
    "Like Omni, but waits for chassis contact before firing the weapon.  If chassis is not found by a certain time, then fires anyway."
    # Use variable 'NoChassisTime' in Bindings.py to set the amount of time in seconds the AI will wait to find the chassis before giving up and firing, when there are components in the smart zone.
    name = "OmniPopup"
    #It's Popup but with spinning weapon support, oh snap!

    def __init__(self, **args):
        Popup.__init__(self, **args)

        self.spin_range = 40.0

    def Tick(self):
        bReturn = Popup.Tick(self)
        if self.weapons:

            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        return AI.SuperAI.Tick(self)

AI.register(OmniPopup)