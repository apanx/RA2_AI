from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class RangeOmni(Omni):
    "Omni strategy but with no custom zone"
    name = "RangeOmni"

    def __init__(self, **args):
        Omni.__init__(self, **args)

        self.reloadTime = 0
        self.reloadDelay = 4
        self.mayFire = True
        self.range = 6
        self.delta = 0.5 #tolerance between full Aim

    def Tick(self):
        # fire weapon
        if self.weapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

        if enemy != None :
            # time to move or fire the laser Guided (ser -motor mounted) gun :
            enemyHead = self.GetHeadingToID(enemy, False)
            if self.debug :
                self.DebugString(1, "enemyHead : " + str(enemyHead))
                self.DebugString(2, "range : " + str(range))
            if ( enemyHead >= -self.delta and enemyHead <= self.delta):
                # if range <=  range of the mounted gun
                # LaserGuided gun aim ennemy : par Saint Georges ! Montjoie ! Saint Denis ! pas de quartier !
                if range <= self.range and self.mayFire : self.Input("Fire", 0, 1)

        return AI.SuperAI.Tick(self)

AI.register(RangeOmni)
