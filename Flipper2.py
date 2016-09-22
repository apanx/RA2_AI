from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
# import Gooey
import math
import Tactics

# Flipper2.py last updated 6/9/14 by Clickbeetle
# Update 6/9/14: Revamped code to reduce occurrence of "flipper staredowns" in flipper vs. flipper battles.  Added ability to become invertible once 'sweapons' components break.
# Update 7/24/12: Renamed this file to Flipper2.py so Flipper.py is not overwritten.  Added customizable srimech firing interval.

# This AI will act normally as long as the opponent is moving.  If the opponent stops moving, this AI will also stop and wait for the opponent to be counted out.  If the opponent starts moving again, so will this AI.  In a rumble, this AI will ignore any bots that aren't moving and will only stop if all opponents stop.
# Has support for two smart zone-based weapons and one analog-controlled spinner.  Name the smart zones "flip" and "weapon" and the controls "Flip", "Fire", and "Spin".  "Srimech" control for self-righting.  Note you must put 'UseSrimech':1 in Bindings.py to self-right with the Srimech control; otherwise it will use Flip.  You can set component id's in 'sweapons' to become invertible once those components break.  If you use this AI with a vertical spinner, put a smart zone called "flip" or "weapon" in front (doesn't matter which).  This is needed so the AI knows when it hits something.
# CUSTOMIZABLE SETTINGS:
# 'EnemyMoveRadius' sets how far the enemy must move in order to be considered mobile.  Default is 1.
# 'EnemyMoveTime' sets how long (in seconds) the enemy has to move the required distance before being considered immobile.  Default is 3.
# 'cooldown' is the time (in seconds) after the AI flips the opponent in which enemy movement won't reset the immobility checker.  Basically this is to let the opponent land and settle down before the AI starts counting movement as "being mobile".  Should be high for powerful flippers and low for weak ones.  Default is 3.
# 'PrioritizeFlipper' if set to 1, the AI won't fire the other weapon until the flipper fires.  Useful for bots that use the flipper to get under opponents.  When all of self.weapons are lost, the flipper will stop firing and the other weapon will fire even when the flipper doesn't.  The flipper component id's should therefore be set in self.weapons and no other id's for this to work.  Default is 0.
# 'NoChassisTime' sets how long (in half-seconds) the AI will wait to find the chassis before giving up and firing, when there are components in the smart zone.  ONLY WORKS FOR SECONDARY WEAPON, NOT FLIPPER so wire the bot and name the controls like you are using Omni or Popup.py if you use this.  Default is 1.
# 'SrimechInterval' sets how often the AI fires the srimech when attempting to self-right.  Srimech will fire once every X seconds.  Default is 1.

class FlipperEngage(AI.Tactic):
    name = "FlipperEngage"
    
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

class UpsideDownTracker:
    def __init__(self):
        self.last_time = 0
        self.last_position = None
        self.contact = 0
        self.stoptime = 0
        
class Flipper2(AI.SuperAI):
    "Flipper strategy"
    name = "Flipper2"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
               
        self.zone = "flip"
        self.zone2 = "weapon"
        self.trigger = "Flip"
        self.upTrack = {}       # for seeing if enemies can drive upside down
        self.move_thresh = 0.5
        if 'EnemyMoveRadius' in args: self.move_thresh = args['EnemyMoveRadius']
        self.move_time = 3
        if 'EnemyMoveTime' in args: self.move_time = args['EnemyMoveTime']
        self.cooldown = 3
        if 'cooldown' in args: self.cooldown = args['cooldown']
        self.spin_range = 50
        if 'range' in args: self.spin_range = args['range']
        self.PrioritizeFlipper = 0
        if 'PrioritizeFlipper' in args: self.PrioritizeFlipper = args['PrioritizeFlipper']
        self.botinzone = 0
        self.compinzone = 0
        self.comptimer = 0
        self.NoChassisTime = 1
        if 'NoChassisTime' in args: self.NoChassisTime = args.get('NoChassisTime') * 4
        self.flip = 0
        self.maybInvertible = 0
        self.UseSrimech = 0
        if 'UseSrimech' in args: self.UseSrimech = args['UseSrimech']
        self.sritime = 8
        if 'SrimechInterval' in args: self.sritime = args.get('SrimechInterval') * 8
        
        self.tactics.append(FlipperEngage(self))
        
    def Activate(self, active):
        if len(self.sweapons) > 0:
            self.maybInvertible = 1
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
            # self.tauntbox = Gooey.Plain("taunt", 10, 175, 640, 175)
            # tbox = self.tauntbox.addText("taunt1", 10, 0, 640, 15)
            # tbox.setText("")
            
            self.RegisterSmartZone(self.zone, 1)
            self.RegisterSmartZone(self.zone2, 2)
            
        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        targets = [x.robot for x in self.sensors.itervalues() if x.contacts > 0 \
                and not plus.isDefeated(x.robot)]
        enemy, range = self.GetNearestEnemy()
        
        # Drive inverted if srimech breaks and srimech ID's have been set in sweapons
        if not self.sweapons and self.maybInvertible == 1:
            self.bInvertible = True
        
        # fire srimech if we're stuck on our rear
        if list(plus.getDirection(self.GetID(),0))[1]>0.9:
            self.Input("Srimech", 0, 1)
                
        if self.compinzone == 1 and self.botinzone == 0:
            self.comptimer += 1
        
        if self.botinzone == 1:
            self.comptimer = 0
                
        if self.weapons:
            fire = False
            self.Input(self.trigger, 0, 0)
            if enemy is not None:
                if self.flip == 1 and self.CanDriveUpsideDown(enemy):
                    fire = True
                
            if fire: self.Input(self.trigger, 0, 1)
            
            if self.PrioritizeFlipper == 0:
                # secondary weapon
                if (self.botinzone == 1 or (self.comptimer >= self.NoChassisTime and self.compinzone == 1)):
                    self.Input("Fire", 0, 1)
                
            # spinner
            # spin up depending on enemy's range
            if enemy is not None and range < self.spin_range and not self.IsUpsideDown():
                self.Input("Spin", 0, 100)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)

            if self.IsUpsideDown():
                self.Input("Spin", 0, -100)
                
        if self.PrioritizeFlipper == 1:
            # if the flipper is still intact, fire it first before firing other weapons
            if self.weapons:
                if self.GetInputStatus(self.trigger, 0) == 1 and (self.botinzone == 1 or (self.comptimer >= self.NoChassisTime and self.compinzone == 1)):
                    self.Input("Fire", 0, 1)
                    
            else:
                if (self.botinzone == 1 or (self.comptimer >= self.NoChassisTime and self.compinzone == 1)):
                    self.Input("Fire", 0, 1)
            
        return AI.SuperAI.Tick(self)

    def CanDriveUpsideDown(self, bot):
        MOVE_THRESHOLD = self.move_thresh
        
        if bot in self.upTrack:
            t = self.upTrack[bot]
            # self.tauntbox.get("taunt1").setText(str(t.contact))
            
            # Check if we've made contact with the enemy
            if (self.flip == 1 or self.compinzone == 1) and t.contact == 0:
                t.contact = 1

            # check to see if he's moved recently
            position = plus.getLocation(bot)
            time = plus.getTimeElapsed()
            if time - t.last_time > self.move_time:
                # this record is too old to be reliable
                t.last_time = time
                t.last_position = position
                #return False
            v0 = vector3(t.last_position)
            v1 = vector3(position)
            # Don't assume the enemy is immobile if we haven't made contact
            if (v1-v0).length() > MOVE_THRESHOLD or t.contact == 0:
                # Reality check: Is the enemy actually still mobile (after a cooldown period to let them settle) - if so, reset contact
                if t.contact == 2 and time - t.stoptime > self.cooldown:
                    t.contact = 0
                    return True
                else:
                    return True
            # Check if we've made contact and the enemy isn't moving
            if (v1-v0).length() <= MOVE_THRESHOLD and t.contact > 0:
                if t.contact == 1:
                    t.contact = 2
                    t.stoptime = plus.getTimeElapsed()
                return False
        else:
            t = UpsideDownTracker()
            t.last_position = plus.getLocation(bot)
            t.last_time = plus.getTimeElapsed()
            t.contact = 0
            t.stoptime = plus.getTimeElapsed()
            self.upTrack[bot] = t
            return False
            
    def GetNearestEnemy(self):
        closest = None
        min_dist = 9999
        min_weighted_dist = 9999

        enemies = self.GetEnemies()

        # ignore bots that aren't moving
        # lol this target human players first code was actually useful.
        for enemy in enemies:
            dist = self.GetDistanceToID(enemy)
            weighted_dist = dist
            if not self.CanDriveUpsideDown(enemy):
                weighted_dist += 30
            else:
                weighted_dist = dist
            if weighted_dist < min_weighted_dist:
                closest = enemy
                min_weighted_dist = weighted_dist
                min_dist = dist

        return closest, min_dist
            
    def InvertHandler(self):
        # fire weapon once per second (until we're upright!)
        while 1:
            if self.UseSrimech == 1:
                self.Input("Srimech", 0, 1)
            else:
                self.Input(self.trigger, 0, 1)
            
            for i in range(0, self.sritime):
                yield 0
                
    def LostComponent(self, id):
        # if we lose all our weapons, stop using the Engage tactic and switch to Shove
        if id in self.weapons: self.weapons.remove(id)
        
        if not self.weapons:
            tactic = [x for x in self.tactics if x.name == "FlipperEngage"]
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
        if id == 1:
            if robot > 0:
                if direction == 1:
                    self.flip = 1
                if direction == -1:
                    self.flip = 0
                    
        if id == 2:
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
    
AI.register(Flipper2)