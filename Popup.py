from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Omni import Omni

class Popup(Omni):
    "Like Omni, but waits for chassis contact before firing the weapon.  If chassis is not found by a certain time, then fires anyway."
    # Use variable 'NoChassisTime' in Bindings.py to set the amount of time in half-seconds the AI will wait to find the chassis before giving up and firing, when there are components in the smart zone.
    # Set variable 'RunUpsideDown' to 1 for bots that flip over at the beginning of the match and fight upside down.  Such bots must be invertible as well.
    # Set srimech component ID's in 'sweapons' to make the bot invertible after the srimech breaks.
    # UPDATE 7/4/11: Added support for upside down bots, conditional invertibility, and made AI fire srimech if the bot is stuck on its rear.
    name = "Popup"

    def __init__(self, **args):
        Omni.__init__(self, **args)

        self.botinzone = 0
        self.compinzone = 0
        self.comptimer = 0
        self.NoChassisTime = 8
        self.RunUpsideDown = 0
        self.InverterTime = 4
        self.maybInvertible = 0

        if 'zone' in args: self.zone = args['zone']

        if 'triggers' in args: self.triggers = args['triggers']
        if 'NoChassisTime' in args: self.NoChassisTime = args['NoChassisTime'] * 4
        if 'RunUpsideDown' in args: self.RunUpsideDown = args['RunUpsideDown']

    def Activate(self, active):
        if len(self.sweapons) > 0:
            self.maybInvertible = 1
        bReturn = Omni.Activate(self, active)

        return bReturn
    def Tick(self):
        # Drive inverted if srimech breaks and srimech ID's have been set in sweapons
        if not self.sweapons and self.maybInvertible == 1:
            self.bInvertible = True

        # fire srimech if we're stuck on our rear
        if list(plus.getDirection(self.GetID(),0))[1]>0.9:
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)

        # Upside-down srimech
        if self.RunUpsideDown == 1 and not self.IsUpsideDown():
            self.InverterTime -= 1
            if self.InverterTime <= 0:
                for trigger in self.trigger2:
                    self.Input(trigger, 0, 1)
                self.InverterTime = 4
        # fire weapon
        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        # if a component is in the smart zone but not the chassis, wait to find chassis before firing weapons
        if self.compinzone == 1 and self.botinzone == 0:
            self.comptimer += 1

        if self.botinzone == 1:
            self.comptimer = 0

        if self.weapons and (self.botinzone == 1 or (self.comptimer >= self.NoChassisTime and self.compinzone == 1)):
            for trigger in self.triggers: self.Input(trigger, 0, 1)

        return AI.SuperAI.Tick(self)

    def LostComponent(self, id):
        if id in self.sweapons: self.sweapons.remove(id)

        return Omni.LostComponent(self, id)

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1 and self.weapons:
            if robot > 0:
                if direction == 1:
                    self.compinzone = 1
                    if chassis:
                        self.botinzone = 1
                if direction == -1:
                    self.compinzone = 0
                    if chassis:
                        self.botinzone = 0
        return True

AI.register(Popup)