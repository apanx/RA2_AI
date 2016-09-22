from __future__ import generators
import plus
import AI
from AI import vector3
import Arenas
import Gooey
import math
import Tactics

#NOTES: Bindings' coding for __INIT_ stuff:
    ### 'motor': 5  (5=component number during assembly).
    ### ''
    ### 'altitude': 0.5  (distance above the floor)
    ### ''
    ### 'TimerSpeed3thru4' : 1  (1-5 integer in Bindings line)
    ### 'TimerSpeed5thru8' : 1  (1-5 integer in Bindings line)
    ### 'TimerSpeed1thru7' : 1  (1-5 integer in Bindings line)
    ### ''
    ### 'SRM_TImer' : 1  (1-? integer in Bindings line)


# BINDINGS TEMPLATE (watch indenting):
    # For SkinHead:
        #        list.append(("     SkinHead_HW_2e","Top_Smasher_2R",{'radius':0.1, 'topspeed':130, 'throttle':130, 'turn':20,'turnspeed':1.2, 'TimerSpeed3thru4':5, 'TimerSpeed5thru8':5, 'TimerSpeed1thru7':5, 'SRM_TImer':1,'TS_range': 3, 'motor':12, 'weapons':(10,11)}))

    # For Your Bot:
        #        list.append(("XXXXXXX","Top_Smasher_2R",{'radius':0.1, 'topspeed':130, 'throttle':130, 'turn':20,'turnspeed':1.2, 'TimerSpeed3thru4':5, 'TimerSpeed5thru8':5, 'TimerSpeed1thru7':5, 'SRM_TImer':1,'TS_range': 3, 'motor':12, 'weapons':(10,11)}))



class Top_Smasher_2R(AI.SuperAI):
    "Top_Smasher_2R for For Multi_functioning and sequential bots (with optional turret).   "R" means Range firing option."
    name = "Top_Smasher_2R"

    def __init__(self, **args):
        AI.SuperAI.__init__(self, **args)

        self.OnGoingTimer = 0
        self.LocX_FactorA = 0
        self.LocZ_FactorA = 0
        self.LocX_FactorB = 0
        self.LocZ_FactorB = 0

        self.zone1 = "Zone1"
        self.triggers1 = ["Fire1"]
        self.zone2 = "Zone2"     
        self.triggers2 = ["Fire2"] #  "Number 2 trigger" is actuated/fired via (1) Smartzone ("Zone2" above), or (2) Servo-Aiming (below).
        self.zone3 = "Zone3"
        self.triggers3 = ["Fire3"]
        self.zone4 = "Zone4"
        self.triggers4 = ["Fire4"]
        self.zone5 = "Zone5"
        self.triggers5 = ["Fire5"]
        self.zone6 = "Zone6"
        self.triggers6 = ["Fire6"]
        self.zone7 = "Zone7"
        self.triggers7 = ["Fire7"]
        self.zone8 = "Zone8"
        self.triggers8 = ["Fire8"]

        self.Aim_triggers = ["AimFire"] #@@@@@@@@@@@@@@@@@@@@@

        self.zone9 = "ZoneFire3-4" # This is  2 Sequential triggers.
        self.zone10 = "ZoneFire5-8"#  This is 4 Sequential triggers.                               
        self.zone11 = "ZoneFire1-7"#  This is 7 Sequential triggers.  

        if 'zone' in args: self.zone = args['zone']

        self.tactics.append(Tactics.Engage(self))

        self.weptimerA = 0       ##########################
        self.weptimerB = 0       ##########################
        self.weptimerC = 0       ##########################

        #######AAAAAAAAAAAAAAAAA
#        self.ongoingtimerAA = 0 
#        self.floor = 0  
#        self.altitude = 0 # default (if no Bindings setting)
#        if 'altitude' in args: self.altitude = args.get('altitude') # for Bindings input #
        #######AAAAAAAAAAAAAAAAA

        ########WWWWWWWWWWW
        self.TimerSpeed3thru4 = 1 # default (if no Bindings setting)
        self.ACounter3thru4 = 0
        self.AParameter3thru4 = 0
        if 'TimerSpeed3thru4' in args: self.TimerSpeed3thru4 = args.get('TimerSpeed3thru4')
        if self.TimerSpeed3thru4 ==1:  self.ACounter3thru4 =1; self.AParameter3thru4 =20
        if self.TimerSpeed3thru4 ==2:  self.ACounter3thru4 =1; self.AParameter3thru4 =16
        if self.TimerSpeed3thru4 ==3:  self.ACounter3thru4 =1; self.AParameter3thru4 =12
        if self.TimerSpeed3thru4 ==4:  self.ACounter3thru4 =1; self.AParameter3thru4 =8
        if self.TimerSpeed3thru4 ==5:  self.ACounter3thru4 =1; self.AParameter3thru4 =4
        if self.TimerSpeed3thru4 >5 or self.TimerSpeed3thru4 <1: self.TimerSpeed3thru4 = 1

        self.TimerSpeed5thru8 = 1 # default (if no Bindings setting)
        self.BCounter5thru8 = 0
        self.BParameter5thru8 = 0
        if 'TimerSpeed5thru8' in args: self.TimerSpeed5thru8 = args.get('TimerSpeed5thru8')
        if self.TimerSpeed5thru8 ==1:  self.BCounter5thru8 =1; self.BParameter5thru8 =40
        if self.TimerSpeed5thru8 ==2:  self.BCounter5thru8 =1; self.BParameter5thru8 =32
        if self.TimerSpeed5thru8 ==3:  self.BCounter5thru8 =1; self.BParameter5thru8 =24
        if self.TimerSpeed5thru8 ==4:  self.BCounter5thru8 =1; self.BParameter5thru8 =16
        if self.TimerSpeed5thru8 ==5:  self.BCounter5thru8 =1; self.BParameter5thru8 =8
        if self.TimerSpeed5thru8 >5 or self.TimerSpeed5thru8 <1: self.TimerSpeed5thru8 = 1

        self.TimerSpeed1thru7 = 1 # default (if no Bindings setting)
        self.CCounter1thru7 = 0
        self.CParameter1thru7 = 0
        if 'TimerSpeed1thru7' in args: self.TimerSpeed1thru7 = args.get('TimerSpeed1thru7')
        if self.TimerSpeed1thru7 ==1:  self.CCounter1thru7 =1; self.CParameter1thru7 =40
        if self.TimerSpeed1thru7 ==2:  self.CCounter1thru7 =1; self.CParameter1thru7 =32
        if self.TimerSpeed1thru7 ==3:  self.CCounter1thru7 =1; self.CParameter1thru7 =24
        if self.TimerSpeed1thru7 ==4:  self.CCounter1thru7 =1; self.CParameter1thru7 =16
        if self.TimerSpeed1thru7 ==5:  self.CCounter1thru7 =1; self.CParameter1thru7 =8
#        if self.TimerSpeed1thru7 ==6:  self.CCounter1thru7 =1; self.CParameter1thru7 =8
#        if self.TimerSpeed1thru7 ==7:  self.CCounter1thru7 =1; self.CParameter1thru7 =8
        if self.TimerSpeed1thru7 >5 or self.TimerSpeed1thru7 <1: self.TimerSpeed1thru7 = 1
        ########WWWWWWWWWWW

        self.Motor = 1000 # default (if no Bindings setting) (Can't use '0' here.) @@@@@@@@@@@@@@
        if 'motor' in args: self.Motor = args['motor'] #@@@@@@@@@@@@@@@@@@@

        self.SRM_TImer = 4 # default (if no Bindings setting)
        if 'SRM_TImer' in args: self.SRM_TImer = args['SRM_TImer'] 
        
        self.SRMServoTimer = 0

        self.TS_range = 0 # default (is basically OFF if no Bindings setting)
        if 'TS_range' in args: self.TS_range = args.get('TS_range')
            
        if 'triggers' in args: self.Aim_triggers = args['triggers'] # Range trigger.
        if 'triggers' in args: self.triggers1 = args['triggers']
        if 'triggers' in args: self.triggers2 = args['triggers']
        if 'triggers' in args: self.triggers3 = args['triggers']
        if 'triggers' in args: self.triggers4 = args['triggers']
        if 'triggers' in args: self.triggers5 = args['triggers']
        if 'triggers' in args: self.triggers6 = args['triggers']
        if 'triggers' in args: self.triggers7 = args['triggers']
        if 'triggers' in args: self.triggers8 = args['triggers']



        
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
                tbox = self.debug.addText("line4", 0, 60, 250, 15) #Here to bottom (4-9) is added. @@@@@@
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
                tbox.setText("")                                          #@@@@@@@@@@@@@@@@@@@@@@
            
            self.RegisterSmartZone(self.zone1, 1)
            self.RegisterSmartZone(self.zone2, 2)
            self.RegisterSmartZone(self.zone3, 3)
            self.RegisterSmartZone(self.zone4, 4)
            self.RegisterSmartZone(self.zone5, 5)
            self.RegisterSmartZone(self.zone6, 6)
            self.RegisterSmartZone(self.zone7, 7)
            self.RegisterSmartZone(self.zone8, 8)

            self.RegisterSmartZone(self.zone9, 9)
            self.RegisterSmartZone(self.zone10, 10)
            self.RegisterSmartZone(self.zone11, 11)

        return AI.SuperAI.Activate(self, active)



    def Tick(self):
        #@@@@@@@@@@@@@@@@@@@@@@
        #  Servo Aiming and firing. (Must enter servo's component assembly number in Bindings [see above]).
        if self.Motor < 1000:  # If there IS a Servo motor controlling the direction of the weapon....
            for trigger in self.Aim_triggers: self.Input(trigger, 0, 0)
            Target, range = self.GetNearestEnemy()
            if Target != None:
                Winkel = (self.GetHeadingToID(Target, False) - self.GetMotorAngle(self.Motor))
                self.DebugString(6, str(self.GetHeadingToID(Target, False)))
                self.DebugString(7, str(-self.GetMotorAngle(self.Motor)))
                self.DebugString(8, str(Winkel))
                if self.AimTowards(Winkel) and range < self.TS_range: # Firing is determined by Aiming and Range set in Bindings "TS_range".
                    for trigger in self.Aim_triggers:  self.Input(trigger, 0, 1)
        #@@@@@@@@@@@@@@@@@@@@@@


        ############--TS_range--#############
        if self.Motor == 1000: # If there's NO Servo motor controlling the direction of the weapon, then just use 'Range' to fire weapon(s).
            enemy, TS_range = self.GetNearestEnemy()
            if enemy is not None and range < self.TS_range:
                plus.playSound(self.Alarm)
                for trigger in self.Aim_triggers:  self.Input(trigger, 0, 1)
        ############--TS_range--#############


        ######WWWWWWWWWWW
        # 3 looping timers for sequential weapon activation (with Bindings input) 
        self.weptimerA += self.ACounter3thru4
        if self.weptimerA == self.AParameter3thru4:
            self.weptimerA = 0

        self.weptimerB += self.BCounter5thru8
        if self.weptimerB == self.BParameter5thru8:
            self.weptimerB = 0

        self.weptimerC += self.CCounter1thru7
        if self.weptimerC == self.CParameter1thru7:
            self.weptimerC = 0
        ######WWWWWWWWWWW

        ############--SRM--#############
        self.OnGoingTimer +=1        
        if self.OnGoingTimer == 1:  ##############  Get Location "A"
            self.LocX_FactorA = plus.getLocation(self.GetID())[0]
            self.LocZ_FactorA = plus.getLocation(self.GetID())[2]

        if self.OnGoingTimer == 8:  ##############  Get Location "B"
            self.LocX_FactorB = plus.getLocation(self.GetID())[0]
            self.LocZ_FactorB = plus.getLocation(self.GetID())[2]

        if self.LocX_FactorA > self.LocX_FactorB - 0.05 and self.LocX_FactorA < self.LocX_FactorB + 0.05 and self.LocZ_FactorA > self.LocZ_FactorB - 0.05 and self.LocZ_FactorA < self.LocZ_FactorB + 0.05:
            if self.OnGoingTimer == 8:  
                for trigger in self.Aim_triggers:  self.Input(trigger, 0, 1)

        if self.OnGoingTimer == 8:  self.OnGoingTimer = 0  # Keep Looping this sensor.
        ############--SRM--#############


        ##########AAAAAAAAAAAAAAAAA
#        if self.altitude > 0: # If there's an 'altitude' entry in Bindings...
#            self.ongoingtimerAA += 1   
#
#            if self.ongoingtimerAA <2:  
#                self.floor = self.GetLocation()[1]
#
#            if self.GetLocation()[1] < self.floor + self.altitude: # "self.altitude" added for Bindings input #
#                plus.force(0, 0, 100 * plus.getWeight(0), 0)
        ##########AAAAAAAAAAAAAAAAA


        return AI.SuperAI.Tick(self)
        
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def Aim(self, level):        
        level = min(max(level, -100), 100)
        self.Input('Aim', 0, level)
        self.DebugString(9, "Aim = " + str(int(level)))
        
    def AimTowards(self, heading, in_reverse = False):
        #THRESHOLD = .05
        THRESHOLD = .2
        dreh = 0
        
        if heading > math.pi: heading -= 2 * math.pi
        elif heading < -math.pi: heading += 2 * math.pi
        
        if (heading < -THRESHOLD or heading > THRESHOLD):
            
            dire = -1
            if heading < 0: dire = 1
            
            h = min(abs(heading), 1.75)
            dreh = dire * (int((h / 1.5) * 100)+20)

            self.Aim(dreh)
            return False
        else:
            self.Aim(0)
            return True
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@



    def InvertHandler(self):
        # fire weapon once per second (until we're upright!)
        while 1:
            for trigger in self.Aim_triggers:  self.Input(trigger, 0, 1) # Range/Aim trigger 'Fire'.
            for trigger in self.triggers1: self.Input(trigger, 0, 1)
            for trigger in self.triggers2: self.Input(trigger, 0, 2)
            for trigger in self.triggers3: self.Input(trigger, 0, 3)
            for trigger in self.triggers4: self.Input(trigger, 0, 4)
            for trigger in self.triggers5: self.Input(trigger, 0, 5)
            for trigger in self.triggers6: self.Input(trigger, 0, 6)
            for trigger in self.triggers7: self.Input(trigger, 0, 7)
            for trigger in self.triggers8: self.Input(trigger, 0, 8)
            
            for i in range(0, self.SRM_TImer):
                yield 0

            if self.Motor < 1000:  # If there's a Bindings entry to control a servo motor...
                self.SRMServoTimer += 1
                if self.SRMServoTimer >= 10 and self.SRMServoTimer < 20:      
                    self.Input('Aim', 0, -100)
                if self.SRMServoTimer >= 20 and self.SRMServoTimer < 30:      
                    self.Input('Aim', 0, 100)
                if self.SRMServoTimer == 30:      
                    self.Input('Aim', 0, 0)
                    self.SRMServoTimer = 0


            
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
            elif id == 4: self.debug.get("line4").setText(string) 
            elif id == 5: self.debug.get("line5").setText(string)
            elif id == 6: self.debug.get("line6").setText(string)
            elif id == 7: self.debug.get("line7").setText(string)
            elif id == 8: self.debug.get("line8").setText(string)
            elif id == 9: self.debug.get("line9").setText(string) #@@@@@@@@@@@@@@@@
    


    def SmartZoneEvent(self, direction, id, robot, chassis):
        if id == 1:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers1: self.Input(trigger, 0, 1)
        elif id == 2:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers2: self.Input(trigger, 0, 2)
        elif id == 3:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers3: self.Input(trigger, 0, 3)
        elif id == 4:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers4: self.Input(trigger, 0, 4)
        elif id == 5:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers5: self.Input(trigger, 0, 5)
        elif id == 6:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers6: self.Input(trigger, 0, 6)
        elif id == 7:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers7: self.Input(trigger, 0, 7)
        elif id == 8:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers8: self.Input(trigger, 0, 8)
                   
        ########WWWWWWWWWWWWW --SEQUENTIAL FIRING --
        # Fires multiple triggers(3-4). 
#        elif id == 9 and self.weapons and self.weptimerA == self.ACounter3thru4:  
        elif id == 9 and self.weapons and self.weptimerA == 0:  
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers3: self.Input(trigger, 0, 3)
        elif id == 9 and self.weapons and self.weptimerA == self.AParameter3thru4 *.5:
            if robot > 0:
                if direction == 1:
                   for trigger in self.triggers4: self.Input(trigger, 0, 4)


        # Fires multiple triggers(5-8). 
#        elif id == 10 and self.weapons and self.weptimerB == self.BCounter5thru8:
        elif id == 10 and self.weapons and self.weptimerB == 0:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers5: self.Input(trigger, 0, 5)
        elif id == 10 and self.weapons and self.weptimerB == self.BParameter5thru8 *.25:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers6: self.Input(trigger, 0, 6)
        elif id == 10 and self.weapons and self.weptimerB == self.BParameter5thru8 *.5:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers7: self.Input(trigger, 0, 7)
        elif id == 10 and self.weapons and self.weptimerB == self.BParameter5thru8 *.75:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers8: self.Input(trigger, 0, 8)


        # Fires multiple triggers(1-7). 
#        elif id == 10 and self.weapons and self.weptimerC == self.CCounter1thru7:
        elif id == 11 and self.weapons and self.weptimerC == 0:
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers1: self.Input(trigger, 0, 1)
        elif id == 11 and self.weapons and self.weptimerC == int(self.CParameter1thru7 *.142):
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers2: self.Input(trigger, 0, 2)
        elif id == 11 and self.weapons and self.weptimerC == int(self.CParameter1thru7 *.284):
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers3: self.Input(trigger, 0, 3)
        elif id == 11 and self.weapons and self.weptimerC == int(self.CParameter1thru7 *.426):
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers4: self.Input(trigger, 0, 4)
        elif id == 11 and self.weapons and self.weptimerC == int(self.CParameter1thru7 *.568):
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers5: self.Input(trigger, 0, 5)
        elif id == 11 and self.weapons and self.weptimerC == int(self.CParameter1thru7 *.71):
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers6: self.Input(trigger, 0, 6)
        elif id == 11 and self.weapons and self.weptimerC == int(self.CParameter1thru7 *.852):
            if robot > 0:
                if direction == 1:
                    for trigger in self.triggers7: self.Input(trigger, 0, 7)


        return True





AI.register(Top_Smasher_2R)
