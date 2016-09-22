from __future__ import generators
from __future__ import division
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math

class DumbCharge(AI.Tactic):
    name = "DumbCharge"
    
    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)
        
        self.regroupPos = None
        self.regroupDir = True
        self.regroupTime = 0
    
    def Evaluate(self):
        self.priority = 0
        self.target_id, range = self.ai.GetNearestEnemy()
        
        if self.target_id != None:
            heading = self.ai.GetHeadingToID(self.target_id, False)
            
            # no turning = more desirable
            self.priority = 100 - (abs(heading) * 20)
                
            # too close to enemy = less desirable
            if range < 3: self.priority -= 75 * (3 - range)
            
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), plus.getLocation(self.target_id))
            if not clear_path: self.priority -= 75
                
    def Execute(self):
        if self.target_id != None:
            self.ai.enemy_id = self.target_id
            
            # default turning & throttle off
            self.ai.Throttle(0)
            self.ai.Turn(0)
            
            heading = self.ai.GetHeadingToID(self.target_id, False)
            target_loc = plus.getLocation(self.target_id)
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), target_loc)

            distance = (vector3(target_loc) - vector3(self.ai.GetLocation())).length()
            speed = self.ai.GetSpeed()
            
            # if we're close but not moving very fast, pick a new location and back toward it
            if (distance < 3 and speed < 2.0) or (distance < 5 and speed < 0):
                if self.regroupPos == None or self.regroupTime <= 0:    
                    self.regroupPos = None
                    # pick a point near us that has a clear shot at the target?
                    for r in (0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6):
                        angle = self.ai.GetHeading(True) + r * (math.pi / 6)
                        new_dir = vector3(math.sin(angle), 0, math.cos(angle))
                        dest = vector3(target_loc) + new_dir * 5
                        
                        clear_path = self.ai.IsStraightPathClear(dest.asTuple(), target_loc)
                        if clear_path:
                            self.regroupPos = dest.asTuple()
                            self.regroupDir = (abs(r) <= 3)
                            self.regroupTime = 16
                            break
                
                # sanity check: if we can't find a valid position, drive forward or backward
                if self.regroupPos == None:
                    self.regroupDir = not self.regroupDir
                    range = 5
                    if self.regroupDir: range = -5
                    self.regroupPos = (vector3(self.ai.GetLocation()) + vector3(self.ai.GetDirection()) * range).asTuple()
                    self.regroupTime = 16
                    
                self.ai.DriveToLocation(self.regroupPos, self.regroupDir)
                self.regroupTime -= 1
            elif distance > 3 and abs(heading) > .35 or not clear_path:
                # if we don't have a clear shot, get closer
                self.ai.DriveToLocation(plus.getLocation(self.target_id))
            else:
                # stop charging if we're near the edge!
                if plus.getGameType() == "TABLETOP":
                    a = Arenas.currentArena
                    loc = vector3(self.ai.GetLocation())
                    
                    # check to see if we're already over
                    dist, over, h = a.DistanceToEdge(loc.asTuple())
                    if over: return False
                    
                    # now check to see if we're heading over
                    angle = self.ai.GetHeading(False)
                    dir = vector3(math.sin(angle), 0, math.cos(angle))
                    speed = self.ai.GetSpeed()
                    
                    look_ahead = .5
                    
                    loc += dir * speed * look_ahead        
                    
                    dist, over, h = a.DistanceToEdge(loc.asTuple())
                    if over: return False
    
                # drive as fast as we can toward the target
                self.ai.AimToHeading(heading)                
                self.ai.Throttle(100)
                self.regroupPos = None
            
            return True
        else:
            return False
            
class Charge(AI.Tactic):
    name = "Charge"
    # This is the same as Ram, but with different default values better suited to slow/more pushy bots.  Charge is added to most bots' tactics when they lose their weapons.
    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)
        
        self.reorient = 0
        self.backuptimer = 0
        # CUSTOMIZABLE SETTINGS
        # 'ThresholdSpeed' is the speed below which the AI will stop pushing the opponent and start backing away.  The default value is 0.1.
        # 'SightRange' is the base distance the AI "sees" for obstacle checking (this is automatically increased with the bot's speed), determining if it is too close to the opponent (base), and the distance at which the AI will stop backing up and charge for another ram (base * 2).  Should be small for slow bots and large for fast bots.  The default value is 3.
        # 'BackUpTime' is an optional feature that will force the AI to stop backing up after a certain time, to prevent certain bots from spinning out in reverse.  The default value is 9999.  To convert to seconds, divide by 8.
        # 'AimError' is the distance to each side of the opponent that the AI will target for a ram.  A low value ensures that the AI will deliver very precise rams to the center of the bot, but too low and the AI may spend too much time aiming.  A high value means less accurate rams, but the AI won't waste any time trying to line up the perfect shot.
        # Default values are good for slow bots.
        list = [x for x in AI.ai_bindings if x[0] == self.ai.botName]
        self.threshold_speed = list[0][2].get('ThresholdSpeed')
        if self.threshold_speed == None: self.threshold_speed = 0.1
        self.sight_range_base = list[0][2].get('SightRange')
        if self.sight_range_base == None: self.sight_range_base = 3
        self.backuptime = list[0][2].get('BackUpTime')
        if self.backuptime == None: self.backuptime = 9999
        self.nosecone = list[0][2].get('AimError')
        if self.nosecone == None: self.nosecone = 0
        #self.tauntbox = Gooey.Plain("taunt", 10, 175, 640, 175)
        #tbox = self.tauntbox.addText("taunt1", 10, 0, 640, 15)
        #tbox.setText("")

    def Evaluate(self):
        self.priority = 0
        self.target_id, range = self.ai.GetNearestEnemy()
        
        if self.target_id != None:
            heading = self.ai.GetHeadingToID(self.target_id, False)
            
            # no turning = more desirable
            self.priority = 100 - (abs(heading) * 20)
                
            # too close to enemy = less desirable
            #if range < 3: self.priority -= 75 * (3 - range)
            
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), plus.getLocation(self.target_id))
            if not clear_path: self.priority -= 75
                
    def Execute(self):
        if self.target_id != None:
            self.ai.enemy_id = self.target_id
            
            # default turning & throttle off
            self.ai.Throttle(0)
            self.ai.Turn(0)
            
            # other info
            heading = self.ai.GetHeadingToID(self.target_id, False)
            target_loc = plus.getLocation(self.target_id)
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), target_loc)
            distance = (vector3(target_loc) - vector3(self.ai.GetLocation())).length()
            speed = self.ai.GetSpeed()
            
            # adjust sight range based on speed so we have time to react to obstacles
            self.sight_range = self.sight_range_base + (0.2 * abs(speed))
            
            # keep track of points in front of and behind us for obstacle detection
            fx = (self.sight_range * math.sin(self.ai.GetHeading(False))) + self.ai.GetLocation()[0]
            fz = (self.sight_range * math.cos(self.ai.GetHeading(False))) + self.ai.GetLocation()[2]
            rx = (-1 * self.sight_range * math.sin(self.ai.GetHeading(False))) + self.ai.GetLocation()[0]
            rz = (-1 * self.sight_range * math.cos(self.ai.GetHeading(False))) + self.ai.GetLocation()[2]
            fry = self.ai.GetLocation()[1]
            forloc = (fx, fry, fz)
            rearloc = (rx, fry, rz)
            
            # markers for detection points
            #plus.emitSmoke(30, (forloc), (0, 2, 0), (3, 3, 3))
            #plus.emitSmoke(30, (rearloc), (0, 2, 0), (3, 3, 3))
            
            # are there obstacles in front of us or behind us
            forclear = self.ai.IsStraightPathClear(self.ai.GetLocation(), forloc)
            rearclear = self.ai.IsStraightPathClear(self.ai.GetLocation(), rearloc)
            
            #self.tauntbox.get("taunt1").setText("fc:" + str(forclear) + " rc:" + str(rearclear) + " reorient:" + str(self.reorient) + " BUtimer:" + str(self.backuptimer))
            
            # if we're close to the enemy and not moving fast, try to get away for another ram
            if (distance < self.sight_range_base and speed < self.threshold_speed and self.backuptimer < self.backuptime) or self.reorient == 1:
                # if the enemy is on our flank, turn to face them a bit better
                if (math.pi/3) < abs(heading) < (2 * math.pi/3):
                    self.ai.AimToHeading(heading)
                # if we're facing the enemy and there's nothing behind us, back up as far as possible
                if abs(heading) <= (math.pi/3):
                    if rearclear:
                        self.reorient = 1
                        self.ai.Turn(0)
                        self.ai.Throttle(-100)
                    else:
                        self.reorient = 0
                        # if we can't get away, push back
                        if abs(heading) > 0.25:
                            self.ai.AimToHeading(heading)
                        else:
                            self.ai.Throttle(100)
                # if we're facing away from the enemy and there's nothing in front of us, drive forward to get away
                if abs(heading) >= (2 * math.pi/3):
                    if forclear:
                        self.reorient = 1
                        self.ai.Turn(0)
                        self.ai.Throttle(100)
                    else:
                        self.reorient = 0
                        # if we can't get away, try to turn around and push back
                        if abs(heading) > 0.25:
                            self.ai.AimToHeading(heading)
                        else:
                            self.ai.Throttle(100)
                # optional timer for bots that go crazy after too long in reverse
                if self.reorient == 1:
                    self.backuptimer += 1
                if self.backuptimer >= self.backuptime:
                    self.reorient = 0
                # 2 times our base sight range is far enough away
                if distance >= (self.sight_range_base * 2):
                    self.backuptimer = 0
                    self.reorient = 0
            elif (distance < self.sight_range_base and speed < self.threshold_speed and self.backuptimer >= self.backuptime):
                if abs(heading) > 0.25:
                    self.ai.AimToHeading(heading)
                else:
                    self.ai.Throttle(100)
                # reset backuptimer when we hit the enemy
                if plus.getTimeElapsed() - self.ai.GetLastDamageDone()[2] <= 0.5:
                    self.backuptimer = 0
            elif not clear_path:
                # if we don't have a clear shot, get closer
                self.ai.DriveToLocation(plus.getLocation(self.target_id))
            else:
                # Ram the opponent
                if self.nosecone > 0:
                    if abs(heading) > abs(math.tan(self.nosecone/distance)):
                        self.ai.AimToHeading(heading)
                    else:
                        self.ai.Throttle(100)
                # stop charging if we're near the edge!
                if plus.getGameType() == "TABLETOP":
                    a = Arenas.currentArena
                    loc = vector3(self.ai.GetLocation())
                    
                    # check to see if we're already over
                    dist, over, h = a.DistanceToEdge(loc.asTuple())
                    if over: return False
                    
                    # now check to see if we're heading over
                    angle = self.ai.GetHeading(False)
                    dir = vector3(math.sin(angle), 0, math.cos(angle))
                    speed = self.ai.GetSpeed()
                    
                    look_ahead = .5
                    
                    loc += dir * speed * look_ahead        
                    
                    dist, over, h = a.DistanceToEdge(loc.asTuple())
                    if over: return False
    
                # drive as fast as we can toward the target
                if abs(heading) > 0.25:
                    self.ai.AimToHeading(heading)
                else:
                    self.ai.Throttle(100)
            return True
        else:
            return False

class Ram(AI.Tactic):
    name = "Ram"

    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)
        
        self.reorient = 0
        self.backuptimer = 0
        # CUSTOMIZABLE SETTINGS
        # 'ThresholdSpeed' is the speed below which the AI will stop pushing the opponent and start backing away.  The default value is 3.
        # 'SightRange' is the base distance the AI "sees" for obstacle checking (this is automatically increased with the bot's speed), determining if it is too close to the opponent (base), and the distance at which the AI will stop backing up and charge for another ram (base * 2).  Should be small for slow bots and large for fast bots.  The default value is 5.
        # 'BackUpTime' is an optional feature that will force the AI to stop backing up after a certain time, to prevent certain bots from spinning out in reverse.  The default value is 9999.  To convert to seconds, divide by 4.
        # 'AimError' is the distance to each side of the opponent that the AI will target for a ram.  A low value ensures that the AI will deliver very precise rams to the center of the bot, but too low and the AI may spend too much time aiming.  A high value means less accurate rams, but the AI won't waste any time trying to line up the perfect shot.
        # Default values are good for fast bots.  They will probably need to be adjusted for slow bots.
        list = [x for x in AI.ai_bindings if x[0] == self.ai.botName]
        self.threshold_speed = list[0][2].get('ThresholdSpeed')
        if self.threshold_speed == None: self.threshold_speed = 3
        self.sight_range_base = list[0][2].get('SightRange')
        if self.sight_range_base == None: self.sight_range_base = 5
        self.backuptime = list[0][2].get('BackUpTime')
        if self.backuptime == None: self.backuptime = 9999
        self.nosecone = list[0][2].get('AimError')
        if self.nosecone == None: self.nosecone = 0
        #self.tauntbox = Gooey.Plain("taunt", 10, 175, 640, 175)
        #tbox = self.tauntbox.addText("taunt1", 10, 0, 640, 15)
        #tbox.setText("")

    def Evaluate(self):
        self.priority = 0
        self.target_id, range = self.ai.GetNearestEnemy()
        
        if self.target_id != None:
            heading = self.ai.GetHeadingToID(self.target_id, False)
            
            # no turning = more desirable
            self.priority = 100 - (abs(heading) * 20)
                
            # too close to enemy = less desirable
            #if range < 3: self.priority -= 75 * (3 - range)
            
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), plus.getLocation(self.target_id))
            if not clear_path: self.priority -= 75
                
    def Execute(self):
        if self.target_id != None:
            self.ai.enemy_id = self.target_id
            
            # default turning & throttle off
            self.ai.Throttle(0)
            self.ai.Turn(0)
            
            # other info
            heading = self.ai.GetHeadingToID(self.target_id, False)
            target_loc = plus.getLocation(self.target_id)
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), target_loc)
            distance = (vector3(target_loc) - vector3(self.ai.GetLocation())).length()
            speed = self.ai.GetSpeed()
            
            # adjust sight range based on speed so we have time to react to obstacles
            self.sight_range = self.sight_range_base + (0.2 * abs(speed))
            
            # keep track of points in front of and behind us for obstacle detection
            fx = (self.sight_range * math.sin(self.ai.GetHeading(False))) + self.ai.GetLocation()[0]
            fz = (self.sight_range * math.cos(self.ai.GetHeading(False))) + self.ai.GetLocation()[2]
            rx = (-1 * self.sight_range * math.sin(self.ai.GetHeading(False))) + self.ai.GetLocation()[0]
            rz = (-1 * self.sight_range * math.cos(self.ai.GetHeading(False))) + self.ai.GetLocation()[2]
            fry = self.ai.GetLocation()[1]
            forloc = (fx, fry, fz)
            rearloc = (rx, fry, rz)
            
            # markers for detection points
            #plus.emitSmoke(30, (forloc), (0, 2, 0), (3, 3, 3))
            #plus.emitSmoke(30, (rearloc), (0, 2, 0), (3, 3, 3))
            
            # are there obstacles in front of us or behind us
            forclear = self.ai.IsStraightPathClear(self.ai.GetLocation(), forloc)
            rearclear = self.ai.IsStraightPathClear(self.ai.GetLocation(), rearloc)
            
            #self.tauntbox.get("taunt1").setText("fc:" + str(forclear) + " rc:" + str(rearclear) + " reorient:" + str(self.reorient) + " BUtimer:" + str(self.backuptimer))
            
            # if we're close to the enemy and not moving fast, try to get away for another ram
            if (distance < self.sight_range_base and speed < self.threshold_speed and self.backuptimer < self.backuptime) or self.reorient == 1:
                # if the enemy is on our flank, turn to face them a bit better
                if (math.pi/3) < abs(heading) < (2 * math.pi/3):
                    self.ai.AimToHeading(heading)
                # if we're facing the enemy and there's nothing behind us, back up as far as possible
                if abs(heading) <= (math.pi/3):
                    if rearclear:
                        self.reorient = 1
                        self.ai.Turn(0)
                        self.ai.Throttle(-100)
                    else:
                        self.reorient = 0
                        # if we can't get away, push back
                        if abs(heading) > 0.25:
                            self.ai.AimToHeading(heading)
                        else:
                            self.ai.Throttle(100)
                # if we're facing away from the enemy and there's nothing in front of us, drive forward to get away
                if abs(heading) >= (2 * math.pi/3):
                    if forclear:
                        self.reorient = 1
                        self.ai.Turn(0)
                        self.ai.Throttle(100)
                    else:
                        self.reorient = 0
                        # if we can't get away, try to turn around and push back
                        if abs(heading) > 0.25:
                            self.ai.AimToHeading(heading)
                        else:
                            self.ai.Throttle(100)
                # optional timer for bots that go crazy after too long in reverse
                if self.reorient == 1:
                    self.backuptimer += 1
                if self.backuptimer >= self.backuptime:
                    self.reorient = 0
                # 2 times our base sight range is far enough away
                if distance >= (self.sight_range_base * 2):
                    self.backuptimer = 0
                    self.reorient = 0
            elif (distance < self.sight_range_base and speed < self.threshold_speed and self.backuptimer >= self.backuptime):
                if abs(heading) > 0.25:
                    self.ai.AimToHeading(heading)
                else:
                    self.ai.Throttle(100)
                # reset backuptimer when we hit the enemy
                if plus.getTimeElapsed() - self.ai.GetLastDamageDone()[2] <= 0.5:
                    self.backuptimer = 0
            elif not clear_path:
                # if we don't have a clear shot, get closer
                self.ai.DriveToLocation(plus.getLocation(self.target_id))
            else:
                # Ram the opponent
                if self.nosecone > 0:
                    if abs(heading) > math.tan(self.nosecone/distance):
                        self.ai.AimToHeading(heading)
                    else:
                        self.ai.Throttle(100)
                # stop charging if we're near the edge!
                if plus.getGameType() == "TABLETOP":
                    a = Arenas.currentArena
                    loc = vector3(self.ai.GetLocation())
                    
                    # check to see if we're already over
                    dist, over, h = a.DistanceToEdge(loc.asTuple())
                    if over: return False
                    
                    # now check to see if we're heading over
                    angle = self.ai.GetHeading(False)
                    dir = vector3(math.sin(angle), 0, math.cos(angle))
                    speed = self.ai.GetSpeed()
                    
                    look_ahead = .5
                    
                    loc += dir * speed * look_ahead        
                    
                    dist, over, h = a.DistanceToEdge(loc.asTuple())
                    if over: return False
    
                # drive as fast as we can toward the target
                if abs(heading) > 0.25:
                    self.ai.AimToHeading(heading)
                else:
                    self.ai.Throttle(100)
            return True
        else:
            return False
            
class ReverseRam(AI.Tactic):
    name = "ReverseRam"
    # AI rams with its back end.  For rammers with weapons both front and back.  Throttle and turning must be inverted to work.

    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)
        
        self.reorient = 0
        self.backuptimer = 0
        # CUSTOMIZABLE SETTINGS
        # 'ThresholdSpeed' is the speed below which the AI will stop pushing the opponent and start backing away.  The default value is 3.
        # 'SightRange' is the base distance the AI "sees" for obstacle checking (this is automatically increased with the bot's speed), determining if it is too close to the opponent (base), and the distance at which the AI will stop backing up and charge for another ram (base * 2).  Should be small for slow bots and large for fast bots.  The default value is 5.
        # 'BackUpTime' is an optional feature that will force the AI to stop backing up after a certain time, to prevent certain bots from spinning out in reverse.  The default value is 9999.  To convert to seconds, divide by 4.
        # 'AimError' is the distance to each side of the opponent that the AI will target for a ram.  A low value ensures that the AI will deliver very precise rams to the center of the bot, but too low and the AI may spend too much time aiming.  A high value means less accurate rams, but the AI won't waste any time trying to line up the perfect shot.
        # Default values are good for fast bots.  They will probably need to be adjusted for slow bots.
        list = [x for x in AI.ai_bindings if x[0] == self.ai.botName]
        self.threshold_speed = list[0][2].get('ThresholdSpeed')
        if self.threshold_speed == None: self.threshold_speed = 3
        self.sight_range_base = list[0][2].get('SightRange')
        if self.sight_range_base == None: self.sight_range_base = 5
        self.backuptime = list[0][2].get('BackUpTime')
        if self.backuptime == None: self.backuptime = 9999
        self.nosecone = list[0][2].get('AimError')
        if self.nosecone == None: self.nosecone = 0
        #self.tauntbox = Gooey.Plain("taunt", 10, 175, 640, 175)
        #tbox = self.tauntbox.addText("taunt1", 10, 0, 640, 15)
        #tbox.setText("")

    def Evaluate(self):
        self.priority = 0
        self.target_id, range = self.ai.GetNearestEnemy()
        
        if self.target_id != None:
            heading = self.ai.GetHeadingToID(self.target_id, False)
            
            # no turning = more desirable
            self.priority = 100 - (abs(heading) * 20)
                
            # too close to enemy = less desirable
            #if range < 3: self.priority -= 75 * (3 - range)
            
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), plus.getLocation(self.target_id))
            if not clear_path: self.priority -= 75
                
    def Execute(self):
        if self.target_id != None:
            self.ai.enemy_id = self.target_id
            
            # default turning & throttle off
            self.ai.Throttle(0)
            self.ai.Turn(0)
            
            # other info
            heading = self.ai.GetHeadingToID(self.target_id, False)
            target_loc = plus.getLocation(self.target_id)
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), target_loc)
            distance = (vector3(target_loc) - vector3(self.ai.GetLocation())).length()
            speed = self.ai.GetSpeed()
            
            # adjust sight range based on speed so we have time to react to obstacles
            self.sight_range = self.sight_range_base + (0.2 * abs(speed))
            
            # keep track of points in front of and behind us for obstacle detection
            fx = (self.sight_range * math.sin(self.ai.GetHeading(False))) + self.ai.GetLocation()[0]
            fz = (self.sight_range * math.cos(self.ai.GetHeading(False))) + self.ai.GetLocation()[2]
            rx = (-1 * self.sight_range * math.sin(self.ai.GetHeading(False))) + self.ai.GetLocation()[0]
            rz = (-1 * self.sight_range * math.cos(self.ai.GetHeading(False))) + self.ai.GetLocation()[2]
            fry = self.ai.GetLocation()[1]
            forloc = (fx, fry, fz)
            rearloc = (rx, fry, rz)
            
            # markers for detection points
            #plus.emitSmoke(30, (forloc), (0, 2, 0), (3, 3, 3))
            #plus.emitSmoke(30, (rearloc), (0, 2, 0), (3, 3, 3))
            
            # are there obstacles in front of us or behind us
            forclear = self.ai.IsStraightPathClear(self.ai.GetLocation(), forloc)
            rearclear = self.ai.IsStraightPathClear(self.ai.GetLocation(), rearloc)
            
            #self.tauntbox.get("taunt1").setText("fc:" + str(forclear) + " rc:" + str(rearclear) + " reorient:" + str(self.reorient) + " BUtimer:" + str(self.backuptimer))
            
            # if we're close to the enemy and not moving fast, try to get away for another ram
            if (distance < self.sight_range_base and speed > -self.threshold_speed and self.backuptimer < self.backuptime) or self.reorient == 1:
                # if the enemy is on our flank, turn to face them a bit better
                if (math.pi/3) < abs(heading) < (2 * math.pi/3):
                    self.ai.AimToHeading(heading)
                # if we're facing the enemy and there's nothing behind us, back up as far as possible
                if abs(heading) <= (math.pi/3):
                    if rearclear:
                        self.reorient = 1
                        self.ai.Turn(0)
                        self.ai.Throttle(100)
                    else:
                        self.reorient = 0
                        # if we can't get away, push back
                        if abs(heading) < (math.pi - 0.25):
                            self.ai.AimToHeading(heading)
                        else:
                            self.ai.Throttle(100)
                # if we're facing away from the enemy and there's nothing in front of us, drive forward to get away
                if abs(heading) >= (2 * math.pi/3):
                    if forclear:
                        self.reorient = 1
                        self.ai.Turn(0)
                        self.ai.Throttle(-100)
                    else:
                        self.reorient = 0
                        # if we can't get away, try to turn around and push back
                        if abs(heading) < (math.pi - 0.25):
                            self.ai.AimToHeading(heading)
                        else:
                            self.ai.Throttle(100)
                # optional timer for bots that go crazy after too long in reverse
                if self.reorient == 1:
                    self.backuptimer += 1
                if self.backuptimer >= self.backuptime:
                    self.reorient = 0
                # 2 times our base sight range is far enough away
                if distance >= (self.sight_range_base * 2):
                    self.backuptimer = 0
                    self.reorient = 0
            elif (distance < self.sight_range_base and speed > -self.threshold_speed and self.backuptimer >= self.backuptime):
                if abs(heading) < (math.pi - 0.25):
                    self.ai.AimToHeading(heading)
                else:
                    self.ai.Throttle(100)
                # reset backuptimer when we hit the enemy
                if plus.getTimeElapsed() - self.ai.GetLastDamageDone()[2] <= 0.5:
                    self.backuptimer = 0
            elif not clear_path:
                # if we don't have a clear shot, get closer
                self.ai.DriveToLocation(plus.getLocation(self.target_id))
            else:
                # Ram the opponent
                if self.nosecone > 0:
                    if abs(heading) < math.pi - math.tan(self.nosecone/distance):
                        self.ai.AimToHeading(heading)
                    else:
                        self.ai.Throttle(100)
                # stop charging if we're near the edge!
                if plus.getGameType() == "TABLETOP":
                    a = Arenas.currentArena
                    loc = vector3(self.ai.GetLocation())
                    
                    # check to see if we're already over
                    dist, over, h = a.DistanceToEdge(loc.asTuple())
                    if over: return False
                    
                    # now check to see if we're heading over
                    angle = self.ai.GetHeading(False)
                    dir = vector3(math.sin(angle), 0, math.cos(angle))
                    speed = self.ai.GetSpeed()
                    
                    look_ahead = .5
                    
                    loc += dir * speed * look_ahead        
                    
                    dist, over, h = a.DistanceToEdge(loc.asTuple())
                    if over: return False
    
                # drive as fast as we can toward the target
                if abs(heading) < (math.pi - 0.25):
                    self.ai.AimToHeading(heading)
                else:
                    self.ai.Throttle(100)
            return True
        else:
            return False
            
class Shove(AI.Tactic):
    name = "Shove"
    
    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)
        self.target_location = None
        
    def Evaluate(self):
        self.priority = 0
        self.target_id, range = self.ai.GetNearestEnemy()
        self.target_location = None
        
        if self.target_id != None:
            # get hazard nearest enemy
            a = Arenas.currentArena
            
            enemy_loc = plus.getLocation(self.target_id)
            
            hazard = a.GetNearestHazard(enemy_loc)
            if hazard != None:
                self.priority = 100
                
                self.target_location = hazard.location
                
                # target too close to hazard = less desirable
                distance = (vector3(self.target_location) - vector3(enemy_loc)).length()
                if distance < 1: self.priority -= 75
                
                clear_path = self.ai.IsStraightPathClear(enemy_loc, self.target_location)
                if not clear_path: self.priority -= 50

                #d1 = vector3(self.ai.GetLocation()) - vector3(enemy_loc)
                d2 = vector3(enemy_loc) - vector3(self.target_location)
                
                # penalties for distance to enemy & distance from enemy to hazard
                self.priority -= (range * 3)
                self.priority -= (d2.length() * 2)
            else:
                self.priority -= 100
        else:
            self.priority -= 100
                
    def Execute(self):
        if self.target_location and self.target_id != None:
            self.ai.enemy_id = self.target_id
            
            e = vector3(plus.getLocation(self.target_id))
            dest = vector3(self.target_location)
            
            dir = dest - e
            dir.y = 0
            
            # default turning & throttle off
            self.ai.Throttle(0)
            self.ai.Turn(0)
            
            # end this action if enemy is close to destination
            if dir.length() < 1: return False
            
            dir.normalize()
            
            a = Arenas.currentArena
            
            # try to line up behind enemy (or to the sides as a last resort)
            target = e - dir * 3
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), target.asTuple())
            if not clear_path:
                dir.x, dir.y, dir.z = dir.z, dir.y, dir.x
                target = e - dir * 3
                clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), target.asTuple())
                if not clear_path:
                    dir.x, dir.z = -dir.x, -dir.z
                    target = e - dir * 3
    
            if not self.ai.DriveToLocation(target.asTuple()):
                # TODO: head toward enemy or target location?!
                #h = self.ai.GetHeadingTo(e.asTuple(), False)
                h = self.ai.GetHeadingTo(self.target_location, False)
                if abs(h) > .25:
                    self.ai.AimToHeading(h)
                else:
                    # shove!
                    self.ai.Throttle(100)
            
            return True
        else:
            return False
                        
class Engage(AI.Tactic):
    name = "Engage"
    
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
            # Commented out original code telling AI not to move if enemy is in their radius.
            ##if self.ai.GetDistanceToID(self.target_id) > self.ai.fRadius \
                ##and not self.ai.RobotInRange(self.target_id)[1]:
            if not self.ai.RobotInRange(self.target_id)[1]:
                self.ai.DriveToLocation(target)
            else:               
                # ... then aim for center of chassis
                h = self.ai.GetHeadingTo(target, False)
                self.ai.AimToHeading(h)
                    
            return True
        else:
            return False
    
class Reorient(AI.Tactic):
    name = "Reorient"
    
    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)
        
        self.target_id = None
        self.destination = None
        self.timeStarted = 0
        self.bInReverse = False
        
    def Evaluate(self):
        current = plus.getTimeElapsed()
        
        # don't reorient if we just did less than 10 seconds ago
        if current - self.timeStarted > 5 and current - self.timeStarted < 10: self.priority = 0
        else: self.priority = min(150, (current - self.ai.timeOfLastGoodHit) * 10)

    def Execute(self):
        "Try to reorient to a new attack position for a few seconds."
        
        if not self.ai.lastTactic or self.ai.lastTactic.name != "Reorient":
            # reorienting anew
            self.target_id, range = self.ai.GetNearestEnemy()
            self.timeStarted = plus.getTimeElapsed()
            self.destination = None
            
            self.bInReverse = False
            
            if self.target_id != None:
                # pick a location to one side of the target bot and drive to it, then attack again
                target = plus.getLocation(self.target_id)
                loc = self.ai.GetLocation()                   
                distance = (-5, 5)
                dir = vector3(target) - vector3(loc)
                dir.normalize()
                dir.x, dir.z = dir.z, dir.x
 
                for d in distance:
                    # drive toward the side of the enemy for about 5 seconds
                    dest = vector3(target) + dir * d
                    
                    if self.ai.IsStraightPathClear(loc, dest.asTuple()):
                        self.destination = dest
                        break
                
                # if the sides are unavailable, try backing up or going forward
                if not self.destination:
                    distance = (-5, 5)
                    dir.x, dir.z = dir.z, dir.x
                    for d in distance:
                        dest = vector3(target) + dir * d
                        if self.ai.IsStraightPathClear(loc, dest.asTuple()):
                            self.destination = dest
                            if d < 0: self.bInReverse = True
                            else: self.bInReverse = False
                            break
                
        if self.destination != None:
            self.ai.DriveToLocation(self.destination.asTuple(), self.bInReverse)
            return True
                
        return False
    
class Invert(AI.Tactic):
    name = "Invert"
    
    def __init__(self, ai, flip_function):
        self.FlipFunction = flip_function
        AI.Tactic.__init__(self, ai)
        
    def Evaluate(self):
        if not self.ai.bInvertible and self.ai.IsUpsideDown(): self.priority = 200
        else: self.priority = -1000
        
    def Execute(self):
        self.ai.Throttle(0)
        self.ai.Turn(0)
        self.FlipFunction.next()
        
        return True

class Unstuck(AI.Tactic):
    name = "Unstuck"
    
    def __init__(self, ai, unstuck_function):
        self.UnstuckFunction = unstuck_function
        AI.Tactic.__init__(self, ai)
        
    def Evaluate(self):
        # try to move if we're immobile and we either have no enemy
        #  or he was pinned after us
        self.priority = 200
        
        ai = self.ai
        
        # move to free ourselves unless our most recent enemy was stuck first
        if not ai.bImmobile: self.priority = -1000
        elif ai.GetID() in ai.immobile_list and \
            ai.enemy_id in ai.immobile_list and \
            ai.immobile_list[ai.GetID()] > ai.immobile_list[ai.enemy_id]:
                self.priority = -1000
        
    def Execute(self):
        self.ai.Throttle(0)
        self.ai.Turn(0)
        self.UnstuckFunction.next()
                
        return True

class AvoidEdges(AI.Tactic):
    name = "AvoidEdges"
    
    def Evaluate(self):
        # if we're near the edge of the arena, drive to the nearest safe point
        self.priority = -1000

        a = Arenas.currentArena
        
        loc = vector3(self.ai.GetLocation())
        
        # check to see if we're already over
        dist, over, h = a.DistanceToEdge(loc.asTuple())
        if over:
            self.priority = 1000
            return

        # now check to see if we're heading over
        angle = self.ai.GetHeading(False)
        dir = vector3(math.sin(angle), 0, math.cos(angle))
        speed = self.ai.GetSpeed()
        
        look_ahead = .5
        
        loc += dir * speed * look_ahead        
       
        dist, over, h = a.DistanceToEdge(loc.asTuple())
        if over:
            self.priority = 1000
            
    def Execute(self):
        a = Arenas.currentArena
        heading = self.ai.GetHeading(False)
        h = a.HeadingAwayFromEdge(self.ai.GetLocation())
        v_us = vector3(heading)
        v_away = vector3(h)
        dir = 1
        if v_us.dot(v_away) < 0:
            h = -h
            dir = -1
        
        self.ai.AimToHeading(-h)
        self.ai.Throttle(100 * dir)
        
        return True
        
class PushOffEdge(AI.Tactic):
    name = "PushOffEdge"
    
    def Evaluate(self):
        # if we have a clean shot at an enemy near an edge, go for it
        self.priority = -1000
        
        enemies = self.ai.GetEnemies()
        a = Arenas.currentArena
        
        threshold = 5
        
        for enemy in enemies:
            self.target_id = enemy
            enemy_loc = plus.getLocation(enemy)
            dist, over, h = a.DistanceToEdge(enemy_loc)
            if dist < threshold:
                # if enemy is close to edge & we're heading toward the edge, push him
                push_loc = vector3(enemy_loc).move(self.ai.GetHeading(False), threshold)
                dist, over, h = a.DistanceToEdge(push_loc.asTuple())
                if over and self.ai.IsStraightPathClear(self.ai.GetLocation(), enemy_loc):
                    priority = 100 - 50 * abs(self.ai.GetHeadingToID(enemy, False))
                    if priority > self.priority:
                        self.priority = priority
    
    def Execute(self):
        # drive as fast as we can toward the target
        heading = self.ai.GetHeadingToID(self.target_id, False)
        self.ai.AimToHeading(heading)                
        self.ai.Throttle(100)
        
        return True
        
class Dethrone(AI.Tactic):
    name = "Dethrone"
    
    def Evaluate(self):
        self.priority = -1000
        
        # if someone else is scoring, push them off
        a = Arenas.currentArena
        s = a.GetScoringPlayer()
        if s is not None and s != self.ai.GetID():
            self.priority = 150
        
    def Execute(self):
        a = Arenas.currentArena
        enemy = a.GetScoringPlayer()
        
        if enemy is None: return False
        
        target_loc = plus.getLocation(enemy)
        clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), target_loc)
        heading = self.ai.GetHeadingToID(enemy, False)

        self.ai.AimToHeading(heading)
        
        if clear_path and abs(heading) < .35:
            self.ai.Throttle(100)
        else:
            self.ai.DriveToLocation(target_loc)
            
        return True
        
class Reign(AI.Tactic):
    name = "Reign"
    
    def Evaluate(self):
        self.priority = -1000
        
        # we always want to be king!
        self.priority = 100
        
        #~ # if we're not in the scoring zone, let's go for it
        #~ a = Arenas.currentArena
        #~ s = a.GetScoringPlayer()
        #~ if s is None or s != self.ai.GetID():
            #~ self.priority = 100
                    
    def Execute(self):
        # occupy the scoring zone (and/or shove close robots out of the way if we're in there)
        a = Arenas.currentArena
        
        loc = a.GetScoringLocation()
        dist_threshold = 2
        push_threshold = .3
        
        reverse = False
        dist = self.ai.GetDistanceTo(loc)
        h = self.ai.GetHeadingTo(loc, False)
        if h > math.pi / 2 or h < -math.pi / 2:
            reverse = True
            
        if dist > dist_threshold:
            self.ai.DriveToLocation(loc, reverse)
        else:
            # slow down when we get there
            speed = self.ai.GetSpeed()
            if speed > 2.0:
                self.ai.Throttle(-100)
            elif speed < -2.0:
                self.ai.Throttle(100)
            else:
                # keep facing the nearest enemy & ram him if he gets close enough
                self.ai.Throttle(0)
                id, dist = self.ai.GetNearestEnemy()
                if id is not None:
                    h = self.ai.GetHeadingToID(id, False)
                    if abs(h) > push_threshold:
                        self.ai.AimToHeading(h)
                    elif dist < 4:
                        # push him full power
                        self.ai.Throttle(100)
        
        return True
        
class MeltyBrain(AI.Tactic):
    name = "MeltyBrain"

    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)

    def Evaluate(self):
        self.priority = 0
        self.target_id, range = self.ai.GetNearestEnemy()
        
        if self.target_id != None:
            heading = self.ai.GetHeadingToID(self.target_id, False)
            
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), plus.getLocation(self.target_id))
            if not clear_path: self.priority -= 75
                
    def Execute(self):
        if self.target_id != None:
            self.ai.enemy_id = self.target_id
            
            # default turning on & throttle off
            self.ai.Throttle(0)
            self.ai.Turn(100)
            
            heading = self.ai.GetHeadingToID(self.target_id, False)
            target_loc = plus.getLocation(self.target_id)
            clear_path = self.ai.IsStraightPathClear(self.ai.GetLocation(), target_loc)

            distance = (vector3(target_loc) - vector3(self.ai.GetLocation())).length()
            speed = self.ai.GetSpeed()
            
            # drive forward when we're aimed at the target
            if abs(heading + 0.5) < 1:
                self.ai.Throttle(100)
            else:
                self.ai.Throttle(0)
            
            return True
        else:
            return False
            