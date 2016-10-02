from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class PopupMultiZone(AI.SuperAI):
    "Like Popup strategy, up to 4 zones and the classical Fire/Weapon/Srimech"
    name = "PopupMultiZone"
    # up to 4 zones named weapon1, weapon2, weapon3 and weapon4
    # and the associated triggers : Fire1, Fire2, fire3, Fire4
    # weaponX is associated with FireX ie : ennemy in customzone weapon3 -> do the action associated with Fire3
    # You may also change the default tactics (engage) by specify in the bindings.py 'tactic': XXX
    # with XXX = "Charge", "Engage", "Shove", "Ram"
    # Ripped off Popup.py and OmniMultiZone.py by Naryar
    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.trigger2 = ["Srimech"]
        self.botinzone1 = 0
        self.compinzone1 = 0
        self.botinzone2 = 0
        self.compinzone2 = 0
        self.botinzone3 = 0
        self.compinzone3 = 0
        self.botinzone4 = 0
        self.compinzone4 = 0
        self.comptimer1 = 0
        self.comptimer2 = 0
        self.comptimer3 = 0
        self.comptimer4 = 0
        self.NoChassisTime = 8

        if 'NoChassisTime' in args: self.NoChassisTime = args.get('NoChassisTime') * 4

        if 'tactic' in args:
            self.theTactic = args['tactic']
            if   self.theTactic  == "Charge" : self.tactics.append(Tactics.Charge(self))
            elif self.theTactic  == "Ram" : self.tactics.append(Tactics.Ram(self))
            elif self.theTactic  == "Shove" : self.tactics.append(Tactics.Shove(self))
            elif self.theTactic  == "Engage" : self.tactics.append(Tactics.Engage(self))
            else: self.tactics.append(Tactics.Engage(self))
        else: self.tactics.append(Tactics.Engage(self))


    def Activate(self, active):
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 0, 75, 100, 75)
                tbox = self.debug.addText("line0", 0, 0, 100, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 100, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 0, 30, 100, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 100, 15)
                tbox.setText("")

            self.RegisterSmartZone("weapon1", 1)
            self.RegisterSmartZone("weapon2", 2)
            self.RegisterSmartZone("weapon3", 3)
            self.RegisterSmartZone("weapon4", 4)

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon

        targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]

        # if a component is in the first smart zone but not the chassis, wait to find chassis before firing weapons
        if self.compinzone1 == 1 and self.botinzone1 == 0:
            self.comptimer1 += 1

        if self.botinzone1 == 1:
            self.comptimer1 = 0

        if self.weapons and (self.botinzone1 == 1 or (self.comptimer1 >= self.NoChassisTime and self.compinzone1 == 1)):
            self.Input("Fire1", 0, 1)

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

        return AI.SuperAI.Tick(self)

    def InvertHandler(self):
        # fire all weapons once per second (until we're upright!)
        while 1:
            for trigger in self.trigger2:
                self.Input(trigger, 0, 1)

            for i in range(0, 8):
                yield 0

    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)

        if not self.weapons:
            tactic = [x for x in self.tactics if x.name == "Engage"]
            if len(tactic) > 0:
                self.tactics.remove(tactic[0])

                self.tactics.append(Tactics.Shove(self))
                self.tactics.append(Tactics.Charge(self))

        return AI.SuperAI.LostComponent(self, id)

    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1 and self.weapons:
            if robot > 0:
                if direction == 1:
                    self.compinzone1 = 1
                    if chassis:
                        self.botinzone1 = 1
                if direction == -1:
                    self.compinzone1 = 0
                    if chassis:
                        self.botinzone1 = 0
        elif id == 2 and self.weapons:
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

        return True

AI.register(PopupMultiZone)
