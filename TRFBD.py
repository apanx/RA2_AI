from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class TRFBD(Omni):
    "AI for torque reaction full body drums."
    name = "TRFBD"
    # Put 'SpinCycle' in Bindings to make the AI drive back and forth when a bot is in spin range.  It will drive forward for half of the time specified and backwards for the other half.  Measured in ticks (=1/8 seconds).
    # If no SpinCycle is specified, the AI will just spin continuously in one direction when in range.

    def __init__(self, **args):
        Omni.__init__(self, **args)
        if 'SpinCycle' in args: self.spincycle = self.spincycleMax = args['SpinCycle']
        else: self.spincycle = self.spincycleMax = 0

    def Tick(self):
        bReturn = Omni.Tick(self)
        # fire weapon
        if self.weapons:

            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range:
                if self.spincycleMax > 0:
                    self.spincycle -= 1
                    if self.spincycle > self.spincycleMax * 0.5:
                        self.Input("Spin", 0, 100)
                    if self.spincycleMax * 0.5 >= self.spincycle > 0:
                        self.Input("Spin", 0, -100)
                    if self.spincycle <= 0:
                        self.spincycle = self.spincycleMax
                else:
                    self.Input("Spin", 0, 100)
            else:
                self.Input("Spin", 0, 0)

        return bReturn

    def Throttle(self, throttle):
        # if we're car steering and we're not moving much, throttle up
        if self.bCarSteering and self.last_turn_throttle != 0:
            speed = self.GetSpeed()
            if speed > 0 and speed < self.top_speed / 3: throttle = self.last_throttle + 10
            elif speed < 0 and speed > -self.top_speed / 3: throttle = self.last_throttle - 10

        throttle = min(max(throttle, -100), 100)

        self.set_throttle = throttle
        self.Input('Forward', 0, throttle)
        self.DebugString(0, "Throttle = " + str(int(throttle)))

AI.register(TRFBD)
