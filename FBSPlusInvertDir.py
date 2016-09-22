from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

class FBSPlusInvertDir(AI.SuperAI):
    "Spins!"
    name = "FBSPlusInvertDir"
    #Like FBS, but does not change the direction when inverted.
    #For Melty Brain type SnS that are more efficient when spinning in a certain direction.
    #Brought to you by Naryar and ripped off Apanx's FBS.py
    #Modified by Clickbeetle to reduce lag
    #Modified by 123STW to include spinning weapon.

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)
        self.tactics.append(Tactics.Engage(self))
        self.spin_range = 99.0 #Range value (like spinner)
        self.spinspeed = 6.0 #Turningspeed to achieve before moving
        self.accuracy = 0.01 #Radians
        self.rampupfactor = (math.pi / 2 - self.accuracy) * (math.pi / 2 - (math.pi - self.accuracy) ) * -1
        self.direction = 1 # 1 or -1
        self.tickFactor = 3.75
        
        if 'direction' in args: self.direction = args.get('direction')
        if 'spinspeed' in args: self.spinspeed = args.get('spinspeed')
        if 'accuracy' in args: self.accuracy = args.get('accuracy')
        if 'range' in args: self.spin_range = args.get('range')
        if 'Ticks' in args: self.tickFactor = args.get('Ticks')
        
    def Activate(self, active):
        plus.AI.__setattr__tickInterval__(self, 0.125/self.tickFactor)
        print self.rampupfactor
        
        if active:
            if AI.SuperAI.debugging:
                self.debug = Gooey.Plain("watch", 430, 75, 250, 165)
                tbox = self.debug.addText("line0", 0, 0, 250, 15)
                tbox.setText("Throttle")
                tbox = self.debug.addText("line1", 0, 15, 250, 15)
                tbox.setText("Turning")
                tbox = self.debug.addText("line2", 0, 30, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line3", 0, 45, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line4", 0, 60, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line5", 0, 75, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line6", 0, 90, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line7", 0, 105, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line8", 0, 120, 250, 15)
                tbox.setText("")
                tbox = self.debug.addText("line9", 0, 135, 250, 15)
                tbox.setText("")

        return AI.SuperAI.Activate(self, active)

    def Tick(self):
        if AI.SuperAI.debugging:
            speed = self.GetSpeed()
            self.DebugString(4, "Speed = " + str(speed))

            turning_speed = self.GetTurning()
            self.DebugString(5, "TSpeed = " + str(turning_speed))
        if self.weapons:
            # spin up depending on enemy's range
            enemy, range = self.GetNearestEnemy()
            
            if enemy is not None and range < self.spin_range:
                self.Input("Spin", 0, 1)
            elif self.GetInputStatus("Spin", 0) != 0:
                self.Input("Spin", 0, 0)  
  
        return AI.SuperAI.Tick(self)

        
    def LostComponent(self, id):
        #print "Lost Component!"
        return AI.SuperAI.LostComponent(self, id)
        
    def DebugString(self, id, string):
        if self.debug:
            if id == 0: self.debug.get("line0").setText(string)
            elif id == 1: self.debug.get("line1").setText(string)
            elif id == 2: self.debug.get("line2").setText(string)
            elif id == 3: self.debug.get("line3").setText(string)
            elif id == 4: self.debug.get("line4").setText(string)
            elif id == 5: self.debug.get("line5").setText(string)
            elif id == 6: self.debug.get("line6").setText(string)
            elif id == 7: self.debug.get("line7").setText(string)
            elif id == 8: self.debug.get("line8").setText(string)
            elif id == 9: self.debug.get("line9").setText(string)
            
    def StuckHandler(self):
        "This default generator is called when the bot is almost immobile."
        while 1:
            # back up for 2 seconds (will stop once we're not immobile)
            for i in range(0, 16*self.tickFactor):
                pos = vector3(self.GetLocation())
                dir = vector3(self.GetDirection())
                self.NormalDriveToLocation((pos - dir * 3).asTuple(), True)
                yield 0
            # go forward for 2 seconds
            for i in range(0, 16*self.tickFactor):
                pos = vector3(self.GetLocation())
                dir = vector3(self.GetDirection())
                self.NormalDriveToLocation((pos + dir * 3).asTuple(), True)
                yield 0
                
    def InvertHandler(self):
        # fire SRM once per two seconds (until we're upright!)
        while 1:
            self.Input("SRM", 0, 1)
            
            for i in range(0, 8*self.tickFactor):
                yield 0
                
    def Think(self):
        self.Evaluate()
        self.countdownToEvaluation = 8*self.tickFactor
        
        
    def DriveToWaypoints(self, waypoints, in_reverse = False):
        throttle = 0
        found = False
        
        while len(waypoints) > 0 and not found:
            grid = waypoints[0]
            pos = Arenas.currentArena.FromGrid(grid)
            dist = self.GetDistanceTo(pos)
            
            if dist < 1:
                waypoints.pop(0)
                
            else:
                # drive to this point
                
                h = self.GetHeadingTo(pos, in_reverse)
                  
                self.DebugString(6, str(self.GetHeading(False)))
                self.DebugString(7, str(h))
                
                h -= math.pi / 8 * self.direction
                if h > math.pi: h -= 2 * math.pi
                elif h < -math.pi: h += 2 * math.pi
                h = abs(h)
        
                if abs(self.GetTurning()) > self.spinspeed:               
                
                    turnFactor = ((h - self.accuracy) * (h - (math.pi - self.accuracy) ) / self.rampupfactor)
                
                    if (h>1.57): 
                        TurnInput = int(max(100 * turnFactor, 0) * self.direction)
                        ThrottleInput = int((100 + TurnInput) * -1)
                
                        self.Turn(TurnInput)
                        self.Throttle(ThrottleInput)
                    if (h<1.57): 
                        TurnInput = int(max(100 * turnFactor, 0) * self.direction)
                        ThrottleInput = int((100 + TurnInput))
                
                        self.Turn(TurnInput)
                        self.Throttle(ThrottleInput)
                 

                else:
                    self.Turn(100 * self.direction)
                found = True
        if len(waypoints) == 0:
            self.Turn(100 * self.direction)
            self.Throttle(0)
            
        return found
        
    def NormalDriveToLocation(self, world_location, in_reverse = False, update_path = True, last_path = []):
        if self.GetDistanceTo(world_location) > 1:
            if update_path:
                a = Arenas.currentArena
                a.SetSearchRadius(self.fRadius)
                waypoints = list(a.GetPath(self.GetLocation(), world_location, False))
            else:
                waypoints = last_path
            
            if len(waypoints) > 0:
                return self.NormalDriveToWaypoints(waypoints, in_reverse)
            else:
                return False
        else:
            self.Throttle(0)
            self.Turn(0)
            return False
            
    def NormalDriveToWaypoints(self, waypoints, in_reverse = False):
        throttle = 0
        found = False
        
        while len(waypoints) > 0 and not found:
            grid = waypoints[0]
            pos = Arenas.currentArena.FromGrid(grid)
            dist = self.GetDistanceTo(pos)
            dir = 1
            
            if in_reverse: dir = -1
            
            if dist < 1:
                waypoints.pop(0)
            else:
                # drive to this point
                h = self.GetHeadingTo(pos, in_reverse)
                self.AimToHeading(h, in_reverse)
                speed = self.GetSpeed()

                # slow down if we have to turn sharply
                if dist < abs(speed) and (h > .4 or h < -.4):
                    throttle = 0
                    self.boost_throttle = self.max_throttle
                else:
                    if speed * dir < self.top_speed:
                        h = max(min(h, .4), -.4)
                        # drive slower the more we need to turn our heading
                        mps = dir * (.5 - abs(h)) * self.top_speed

                        # boost throttle if we're not going as fast as we'd like
                        if (dir > 0 and speed < mps) or (dir < 0 and speed > mps):
                            self.boost_throttle += (self.max_throttle * .1)

                        throttle = dir * (.5 - abs(h)) * self.boost_throttle
                    else:
                        throttle = 0
                        self.boost_throttle = self.max_throttle
                        
                found = True
        
        self.Throttle(throttle)
        
        if len(waypoints) == 0:
            self.Turn(0)
            self.Throttle(0)
            
        return found
        
# WIP, convert this into array for support of more wheel sides
        
    def Throttle(self, throttle):
        # if we're car steering and we're not moving much, throttle up
        if self.bCarSteering and self.last_turn_throttle != 0:
            speed = self.GetSpeed()
            if speed > 0 and speed < self.top_speed / 3: throttle = self.last_throttle + 10
            elif speed < 0 and speed > -self.top_speed / 3: throttle = self.last_throttle - 10

        throttle = min(max(throttle, -100), 100)

        if self.bInvertible and self.IsUpsideDown(): throttle = -throttle

        self.set_throttle = throttle
        self.Input('Forward', 0, throttle)
        self.DebugString(0, "Throttle = " + str(int(throttle)))
        
    def Turn(self, turning):
        turning = min(max(turning, -100), 100)
        self.set_turn_throttle = turning
        self.Input('LeftRight', 0, -turning)
        self.Input('LeftRight', 1, turning)
        self.DebugString(1, "Turning = " + str(int(turning)))
            
AI.register(FBSPlusInvertDir)
