import plus
import AI
from AI import vector3
import Arenas
import math
import string
import random

class Jouster_Attack_1(AI.Tactic):
    name = "Jouster_Attack_1"

    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)

        self.Timer_1 = 0
        self.Timer_2 = 0
        self.Timer_3 = 0
        self.CANCELer = True
        self.bullseye = 0



    def Evaluate(self):
        #self.priority = -1000
        self.priority = 100

        #~ # if we're not in the scoring zone, let's go for it
        #~ a = Arenas.currentArena
        #~ s = a.GetScoringPlayer()
        #~ if s is None or s != self.ai.GetID():

    def Execute(self):
        a = Arenas.currentArena
        self.Timer_1 += 1

        # Works toward enemy bot.
#        id, dist = self.ai.GetNearestEnemy()
#        h = self.ai.GetHeadingToID(id, False)
#        self.ai.AimToHeading(h)
#        self.ai.Throttle(100)
        # -----


        # Works badly (bot just goes a certain angle.)
#        angle = self.ai.GetHeading(False)
#        self.ai.AimToHeading(angle)
#        self.ai.Throttle(100)


        # Works ok (bot just goes straight, in reference to its own heading, not arena location, and thus goes which ever way it is pointed.)
#        self.ai.AimToHeading(0)
#        self.ai.Throttle(100)



#        target = (10,0,10)
#        if self.Timer_1 <= 50:
#            self.ai.DriveToLocation(target, 0)
            #self.ai.DriveToLocation(target, 1)
#        else:
#            self.ai.AimToHeading(self.ai.GetHeadingTo((10,0,10), 0))
#        self.ai.Throttle(100)



#        if self.Timer_1 <= 30:
#            self.ai.AimToHeading(self.ai.GetHeadingTo((10,0,10), 0))
#        if self.Timer_1 >= 30:
#            self.ai.AimToHeading(self.ai.GetHeadingTo((-10,0,-10), 0))
#        self.ai.Throttle(100)



#        id, dist = self.ai.GetNearestEnemy()
#        self.bullseye = self.GetStartPointLocation(id)[0] + 2   #  (x) of enemy's start point.
#        self.ai.AimToHeading(self.bullseye)
#        self.ai.Throttle(100)


 #       if self.Timer_1 == 1:
 #           self.target_id, range = self.ai.GetNearestEnemy()
 #           heading = self.ai.GetHeadingToID(self.target_id, False)
 #       self.ai.AimToHeading(heading)
#        self.ai.Throttle(100)


        # Works ok, but crashes eventually.
#        if self.Timer_1 == 1:
#            enemies = self.ai.GetEnemies()
#            for enemy in enemies:
#                self.target_id = enemy
#            target_loc = plus.getLocation(self.target_id)
#        self.ai.DriveToLocation(target_loc)
#        self.ai.Throttle(100)


        # >>>>>>>>>>>>>>>>>>>>>>>>>>> GOOD >>>>>>>>>>>>>>>>>>>>>
  #      if self.Timer_1 == 1:
  #          self.target_id, range = self.ai.GetNearestEnemy()
  #      self.ai.DriveToLocation(plus.getLocation(self.target_id))
  #      self.ai.Throttle(100)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        # >>>>>>>>>>>>>>>>>>>>>>>>>>> GOOD >>>>>>>>>>>>>>>>>>>>>
        #self.ai.DriveToLocation((0,0,20))
        #self.ai.DriveToLocation((0,0,0))
        #self.ai.Throttle(100)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        # >>>>>>>>>>>>>>>>>>>>>>>>>>> GOOD >>>>>>>>>>>>>>>>>>>>>
        if self.ai.GetID() == 0:
            target_loc_0 = (-2, 0, -24)
            self.ai.DriveToLocation(target_loc_0)

        if self.ai.GetID() ==1:
            target_loc_1 = (2, 0, 24)
            self.ai.DriveToLocation(target_loc_1)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        #loc = ["(0, 0, 0)"]
        #location = ["(-6.73, 12.25, 1.75)", "(6.73, 12.25, 1.75)", "(6.73, -12.25, 1.75)", "(-6.73, -12.25, 1.75)"]
        #loc = a.GetScoringLocation()

#        id, dist = self.ai.GetNearestEnemy()
#        h = self.ai.GetHeadingToID(id, False)

#        reverse = False
        #dist = self.ai.GetDistanceTo(loc)
#        self.ai.AimToHeading(h)
#        h = self.ai.GetHeadingTo(loc, False)
#        if h > math.pi / 2 or h < -math.pi / 2:
#            reverse = True

#        if dist > 0:
#            self.ai.DriveToLocation(loc, reverse)

#        self.ai.Throttle(100)

#        else:
#            # slow down when we get there
#            speed = self.ai.GetSpeed()
#            if speed > 2.0:
#                self.ai.Throttle(-100)
#            elif speed < -2.0:
#                self.ai.Throttle(100)
#            else:
#                # keep facing the nearest enemy & ram him if he gets close enough
#                self.ai.Throttle(0)
#                id, dist = self.ai.GetNearestEnemy()
#                if id is not None:
#                    h = self.ai.GetHeadingToID(id, False)
#                    if abs(h) > push_threshold:
#                        self.ai.AimToHeading(h)
#                    elif dist < 4:
#                        # push him full power
#                        self.ai.Throttle(100)

        return True
########################################################

class Eccentricity_Handler(AI.Tactic):
    name = "Eccentricity_Handler"

    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)

        self.Timer_1 = 0
        self.Timer_2 = 0
        self.Timer_3 = 0
        self.CANCELer = True
        self.bullseye = 0


    def Evaluate(self):
        #self.priority = -1000
        self.priority = 100



    def Execute(self):
        a = Arenas.currentArena

        # >>>>>>>>>>>>>>>>>>>>>>>>>>> GOOD >>>>>>>>>>>>>>>>>>>>>
        self.ai.DriveToLocation((0,0,0))
        self.ai.Throttle(100)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        return True

########################################################

class Evade(AI.Tactic):
    name = "Evade"

    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)

    def Evaluate(self):
        self.priority = 0
        id, range = self.ai.GetNearestEnemy()

    def Execute(self):
        # get information about self and ennemy :
        id, range = self.ai.GetNearestEnemy() # Find Nearest Enemy.

        if id != None:
            a = Arenas.currentArena

        if id is not None:
            h = self.ai.GetHeadingToID(id, False) # Find HEADING to Nearest Enemy.

            if self.ai.GetLocation()[0] <= abs(4) or self.ai.GetLocation()[2] <= abs(4): # If AI is NOT too far from middle of arena..
                if abs(h) >= .4:
                    self.ai.AimToHeading(h) # Point nose toward opponent...
                elif abs(h) < .4  and  range < 4:
                    self.ai.Throttle(-100)       # Then Back up.


            if self.ai.GetLocation()[0] >= abs(4) or self.ai.GetLocation()[2] >= abs(4): # If AI is TOO FAR from middle of arena..
                #self.ai.Turn(20) # TURN AROUND toward center.
                #self.ai.AimToHeading()
                self.ai.DriveToLocation((0,0,0))
                self.ai.Throttle(100)

#        else: #  self.ai.GetLocation() < abs(8):
#            self.ai.Throttle(0)
#            self.ai.Turn(0)



#        if plus.getLocation(self.target_id) > abs(8):

#        if plus.getLocation(self.GetID())[0] > 8 or plus.getLocation(self.GetID())[0] < -8 or plus.getLocation(self.GetID())[2] > 8 or plus.getLocation(self.GetID())[2] < -8:
#            self.ai.Throttle(100)
#            self.ai.DriveToLocation(0, 0, 0)
#            self.ai.AimToHeading(h)

        return True


class DeBaiter(AI.Tactic):
    name = "DeBaiter" # previously "Charge"

    def __init__(self, ai):
        AI.Tactic.__init__(self, ai)

        self.Timer_1 = 0
        self.Timer_2 = 0
        self.Timer_3 = 0
        self.CANCELer = True

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
#        self.Timer_1 += 1
#        if self.Timer_1 >= 10:
#            #angle = self.ai.GetHeading(False)
#            self.ai.AimToHeading(self.target_id)
#            if abs(heading) < .35:
#                self.ai.Throttle(100)

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

            # drive as fast as we can away from the target
            self.ai.AimToHeading(-heading)
            self.ai.Throttle(100)

            return True
        else:
            return False