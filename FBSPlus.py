from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from FBS import FBS

class FBSPlus(FBS):
    "Spins!"
    #Same as Apanx's FBS.py but supports a spinning weapon.
    #For spinner/SnS hybrids that you want to go for the opponent.
    #Wire like a normal spinner - it can be used by any horizontal spinner, but will be better with a fast turn speed and an all-encompassing weapon.
    #Use spinspeed to regulate the whole bot's spinning speed - if you increase it, the bot will spin on itself faster but be wary
    #that it will reduce the bot's translational speed as well.
    #Use direction to set the whole bot's spinning direction.
    #Brought to you by Naryar and based on Apanx's awesome work.
    #Modified by Clickbeetle to reduce lag.
    name = "FBSPlus"

    def __init__(self, **args):
        FBS.__init__(self, **args)
        self.spin_range = 40.0 #Range value (like spinner)
        if 'range' in args: self.spin_range = args.get('range')

    def Tick(self):
        FBS.Tick(self)
        if self.weapons:
            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

        return plus.AI.Tick(self)

AI.register(FBSPlus)
