from __future__ import generators
import plus
import AI
from AI import vector3
import Tactics
import Flipper2

#Fixed crashing, removed cargo cult programming. Made it a child of Flipper2 /apanx 2021-10-03.

#Yay, its my first AI I did! It's based on the Flipper2 AI but there is pretty much everything modified! xD
#This AI backs up when something gets under it, has a reload function, inverts it's spinner when its upsidedown, stops when it spots immobility... and so on.
#There is some messy leftovers that I didn't cleaned up but whatever, I can't be bothered. xD
#Brought to you by Bildschirm

class NepEngage(Flipper2.FlipperEngage):
    name = "NepEngage"
    def Evaluate(self):
        self.priority = 0
        self.target_id, range = self.ai.GetNearestEnemy()

        # TODO: come up with a priority scale for "engaging"

        if self.target_id != None:
            self.priority = 80
        else:
            self.priority -= 100

    def Execute(self):
        if self.target_id != None:
            self.ai.enemy_id = self.target_id

            # default turning & throttle off
            self.ai.Throttle(0)
            self.ai.Turn(0)

            target = plus.getLocation(self.target_id)

            # slow down if we're coming in too fast
            if self.ai.RobotInRange(self.target_id)[0] and self.ai.GetSpeed() > self.ai.top_speed / 2:
                self.ai.Throttle(-self.ai.max_throttle)

            # try to get within range of chassis...
            if not self.ai.RobotInRange(self.target_id)[1]:
                if self.ai.CanDriveUpsideDown(self.target_id):
                    self.ai.DriveToLocation(target)
                else:
                    self.ai.Throttle(0)
                    h = self.ai.GetHeadingTo(target, False)
                    self.ai.AimToHeading(h)
            else:
                # ... then aim for center of chassis
                h = self.ai.GetHeadingTo(target, False)
                self.ai.AimToHeading(h)

            return True
        else:
            return False

class NeptuniaSys(Flipper2.Flipper2):
    "Flipper strategy"
    name = "NeptuniaSys"

    def __init__(self, **args):
        Flipper2.Flipper2.__init__(self, **args)

        self.zone3 = "Zone1"
        self.zone4 = "Zone2"
        self.triggers = ["Fire"]
        self.botinzone1 = 0
        self.botinzone2 = 0
        self.reloadTime = 0
        self.reloadDelay = 3

        if 'reload' in args: self.reloadDelay = args['reload']
        
        self.triggerIterator = iter(self.triggers)
        tactic = [x for x in self.tactics if x.name == "FlipperEngage"]
        if len(tactic) > 0:
            self.tactics.remove(tactic[0])
        self.tactics.append(NepEngage(self))

    def Activate(self, active):
        Flipper2.Flipper2.Activate(self, active)
        if active:
            self.RegisterSmartZone(self.zone3, 3)
            self.RegisterSmartZone(self.zone4, 4)
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        # fire weapon
        if self.weapons:
            targets = [x for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]
            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()

            if enemy is not None and range < self.spin_range and not self.IsUpsideDown():
                self.Input("Spin", 0, 100)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

            if self.IsUpsideDown():
                self.Input("Spin", 0, -100)

            # slight delay between firing
            if self.reloadTime > 0: self.reloadTime -= 1

            if len(targets) > 0 and self.reloadTime <= 0:
                try:
                    trigger = self.triggerIterator.next()
                except StopIteration:
                    self.triggerIterator = iter(self.triggers)
                    trigger = self.triggerIterator.next()

                self.Input(trigger, 0, 1)
                self.reloadTime = self.reloadDelay

        bReturn = AI.SuperAI.Tick(self)
        
        # call this now so it takes place after other driving commands

        # back up if a bot gets under us
        if self.botinzone1 == 1:
            self.Throttle(0)
            self.Input("Fire1", 0, 100)
        else:
            self.Input("Fire1", 0, 0)
            
        return bReturn

    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)

        if not self.weapons:
            tactic = [x for x in self.tactics if x.name == "NepEngage"]
            if len(tactic) > 0:
                self.tactics.remove(tactic[0])

                self.tactics.append(Tactics.Shove(self))
                self.tactics.append(Tactics.Charge(self))

        return AI.SuperAI.LostComponent(self, id)

    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if robot > 0:
                if direction == 1:
                    self.flip = 1
                if direction == -1:
                    self.flip = 0

        if id == 2:
            if robot > 0:
                r = robot - 1
                if not r in self.sensors:
                    self.sensors[r] = Sensor(r, chassis)
                
                entry = self.sensors[r]
                
                if direction == 1:
                    self.compinzone = 1
                    if chassis:
                        self.botinzone = 1
                    entry.contacts += 1
                    if chassis: entry.chassis = True
                elif direction == -1:
                    entry.contacts -= 1
                    if chassis or entry.contacts == 0: entry.chassis = False
                    self.compinzone = 0
                    if chassis:
                        self.botinzone = 0

        if id == 3:
            if robot > 0:
                if direction == 1:
                    self.botinzone1 = 1
                if direction == -1:
                    self.botinzone1 = 0

        elif id == 4:
            if robot > 0:
                if direction == 1:
                    self.botinzone2 = 1
                if direction == -1:
                    self.botinzone2 = 0
        return True

AI.register(NeptuniaSys)