from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics
from Popup import Popup

class PopupMultiZone(Popup):
    "Like Popup strategy, up to 4 zones and the classical Fire/Weapon/Srimech"
    name = "PopupMultiZone"
    # up to 4 zones named weapon, weapon2, weapon3 and weapon4
    # and the associated triggers : Fire, Fire2, fire3, Fire4
    # weaponX is associated with FireX ie : ennemy in customzone weapon3 -> do the action associated with Fire3
    # You may also change the default tactics (engage) by specify in the bindings.py 'tactic': XXX
    # with XXX = "Charge", "Engage", "Shove", "Ram"
    # Ripped off Popup.py and OmniMultiZone.py by Naryar
    def __init__(self, **args):
        Popup.__init__(self, **args)

        self.botinzone2 = 0
        self.compinzone2 = 0
        self.botinzone3 = 0
        self.compinzone3 = 0
        self.botinzone4 = 0
        self.compinzone4 = 0
        self.comptimer2 = 0
        self.comptimer3 = 0
        self.comptimer4 = 0

    def Activate(self, active):
        if active:
            self.RegisterSmartZone("weapon2", 2)
            self.RegisterSmartZone("weapon3", 3)
            self.RegisterSmartZone("weapon4", 4)

        return Popup.Activate(self, active)

    def Tick(self):
        bReturn = Popup.Tick(self)

        # if a component is in the second smart zone but not the chassis, wait to find chassis before firing weapons
        if self.compinzone2 == 1 and self.botinzone2 == 0:
            self.comptimer2 += 1

        if self.botinzone2 == 1:
            self.comptimer2 = 0

        if self.weapons and (self.botinzone2 == 1 or (self.comptimer2 >= self.NoChassisTime and self.compinzone2 == 1)):
            self.Input("Fire2", 0, 1)

        # if a component is in the third smart zone but not the chassis, wait to find chassis before firing weapons
        if self.compinzone3 == 1 and self.botinzone3 == 0:
            self.comptimer3 += 1

        if self.botinzone3 == 1:
            self.comptimer3 = 0

        if self.weapons and (self.botinzone3 == 1 or (self.comptimer3 >= self.NoChassisTime and self.compinzone3 == 1)):
            self.Input("Fire3", 0, 1)

        # if a component is in the fourth smart zone but not the chassis, wait to find chassis before firing weapons
        if self.compinzone4 == 1 and self.botinzone4 == 0:
            self.comptimer4 += 1

        if self.botinzone4 == 1:
            self.comptimer4 = 0

        if self.weapons and (self.botinzone4 == 1 or (self.comptimer4 >= self.NoChassisTime and self.compinzone4 == 1)):
            self.Input("Fire4", 0, 1)

        return bReturn

    def SmartZoneEvent(self, direction, id, robot, chassis):
        bReturn = Popup.SmartZoneEvent(self, direction, id, robot, chassis)
        if id == 2 and self.weapons:
            if robot > 0:
                if direction == 1:
                    self.compinzone2 = 1
                    if chassis:
                        self.botinzone2 = 1
                if direction == -1:
                    self.compinzone2 = 0
                    if chassis:
                        self.botinzone2 = 0
        elif id == 3 and self.weapons:
            if robot > 0:
                if direction == 1:
                    self.compinzone3 = 1
                    if chassis:
                        self.botinzone3 = 1
                if direction == -1:
                    self.compinzone3 = 0
                    if chassis:
                        self.botinzone3 = 0
        elif id == 4 and self.weapons:
            if robot > 0:
                if direction == 1:
                    self.compinzone4 = 1
                    if chassis:
                        self.botinzone4 = 1
                if direction == -1:
                    self.compinzone4 = 0
                    if chassis:
                        self.botinzone4 = 0

        return bReturn

AI.register(PopupMultiZone)
