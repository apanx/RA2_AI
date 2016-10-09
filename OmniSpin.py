from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class OmniSpin(Omni):
    "Omni that waits to spin back up after hits"
    name = "OmniSpin"

    def __init__(self, **args):
        Omni.__init__(self, **args)

    def RobotInRange(self, robot_id):
        "Return tuple of (part-of-robot-in-range, chassis-in-range)"
        # GetLastDamage returns:  component damaged, amount, at time, by player, by component
        range = self.GetDistanceToID(robot_id)
        if range < self.spin_range:
            damage = self.GetLastDamageReceived()
            if damage[3] == robot_id and (plus.getTimeElapsed() - damage[2] < 1.0):
                return (True, True)

        return (False, False)

AI.register(OmniSpin)
