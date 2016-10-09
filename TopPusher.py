from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class TopPusher(Omni):
    "Uses a smart zone to keep pushing bots even when they are on top of this bot."
    name = "TopPusher"
    # Needs a separate analog control named "Push" wired to the drive, and a smart zone named "Push".
    # Put 'tactic':"Ram" (or "Charge") in Bindings to make the AI use rammer/pusher tactics.

    def __init__(self, **args):
        Omni.__init__(self, **args)

        self.zone = "Push"
        self.compinzone = 0
    def Tick(self):
        # Push when a bot is in the smart zone
        if self.compinzone == 1 and not self.bImmobile:
            self.Input("Push", 0, 100)
        else:
            self.Input("Push", 0, 0)

        # fire weapon
        if self.weapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        return AI.SuperAI.Tick(self)

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if robot > 0:
                if direction == 1:
                    self.compinzone = 1
                elif direction == -1:
                    self.compinzone = 0

        return True

AI.register(TopPusher)
