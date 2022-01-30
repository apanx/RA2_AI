# Robot Arena 2 AI Python Repository

Contains most of the AI Python files created by the Robot Arena 2 community  
Compiled by apanx  
Version 2016-10-04

# Supporting Files
## ImprovedTactics
Improved Charge and modified Engage Tactic, Includes Ram, ReverseRam and MeltyBrain  
Replace original Tactics.py

# List over AIs, Author, Arguments and short description

## Arrowhead, Madiaba
range, zone1, zone2, srimech  
Spinner AI that backs up if the opponent gets under it.

## Batmobile
Like Popup but tweaked for BatmobileAI.

## Bee
Simply a cross between Whipper and Spinner - for SnS/HS hybrids that use a smartzone.  
Whipper that incorporates Spinner.

### BeeCC
Variant of Bee that spins in opposite direction  

## BiDirRam
"For rammers with weapons in both front and back.  Dynamically switches directions and attacks with whichever side has more weapons."  
Use 'weapons' to indicate weapons in the front, and 'sweapons' to indicate weapons in the back.

## BountyHunter
Special AI for Bounty Hunter.  Drives backwards while self righting.

## Boxrush
Slam em and hold em

## CoreBlow
Spinner with two smartzones and SRM

## D_SMFE_Turret_Machinegun_Spin
"SMFE for Machinegun Vehicle (with optional turret and spinner)"  
NOTES: Bindings' coding  
'motor': 5  (5=component number).  
'altitude': 0.5  (distance above the floor)  
'TimerSpeed3thru4' : 1  (1-5 integer)  
'TimerSpeed5thru8' : 1  (1-5 integer)  
'TimerSpeed1thru7' : 1  (1-5 integer)  
'whip': "around"  (means whip around in circle; else default = back and forth)

## Drum, Naryar 
OBSOLETE - VertSpinner includes this function   
When inverted, changes the spinner's direction  
Intended for invertible bots (notably drums and invertible face spinners) that should still spin their weapon upwards when inverted.
You must use an ANALOG CONTROL to wire your spinner, with Positive axis being the upward spinning direction when your bot isn't inverted.  
The AI will use the Negative axis when inverted, so your spinner will spin upwards, as it should for good gut ripping capability.  
Not intended for hybrids, and there is no srimech command.  
Brought to you by Naryar and ripped off Click's VertSpinner.py.

## Dual, apanx
Fires two independent triggers with own zone and ReloadTime for each

## ElectricHammer
Swings a hammer on a spin motor back and forth.  
Use variable 'NoChassisTime' in Bindings.py to set the amount of time in half-seconds the AI will wait to find the chassis before giving up and firing, when there are components in the smart zone.  
Use variable 'StartAngle' to set the angle the hammer will revert to when not in use.  For best results, this should be a multiple of pi/2.  
Use variable 'SwingTime' to tell the AI how long in ticks it should take to retract the hammer.  A tick is 1/8 second.

## Export, apanx
Requires modification of __init__.py to get BotName  
Saves file with all bot components for current bot.

## FBS, apanx
An AI specially made for SnS that you want to go for the opponent while spinning.  
Actually will move towards the opponent by spinning in small circles while advancing (for the math geeks out there, the path it will follow is an epicycloid)  
Wire your bot normally, and then use the binding entries to customize your FBS. Spinspeed and Direction are the most important.  
'spinspeed' defines how your bot will balance rotational speed and translation speed.  
A low spinspeed will make it faster but it will spin on itself slower, and it will make wider circles while advancing.  
A high spinspeed will make it slower but it will spin faster (=> more damage and knockback in most cases), and will move regularly.  
'direction' will define the direction of your bot's spinning (1 is positive axis, -1 is negative axis on your LeftRight control)  
It will change direction when inverted however - if you want to avoid that (notably if yu have an unidirectional weapon that works better when spinning one way), use FBSInvertDir.py.

### FBSInvertDir
Same as FBS but spins the same direction when inverted.

### FBSPlus
Spinner with FBS movement

### FBSPlusInvertDir
Spinner with FBS movement that spins same direction when inverted.

### FBSTrinityInvertDir
FBS that spins same direction when inverted. Supports pistons for Trinity effect.

### FBSAnalog
Spinner wired to Analog control with FBS movement. Spins same direction when inverted

### FBSFlame
FBS with EternalFlame.py-style flamethrower control.

## FBS_1, Madiaba
"For SnS's, with improved Immobility handling."

## FBS_2, Madiaba
For single-direction full body spinners with active or static weapons, with improved immobility handling.  Also has the optional feature of pulsing the active weapon on and off, for shell spinners that are hard to drive when the weapon is on.

Uses standard 'LeftRight' control for spinning.  'Spin' button for active weapons.  'Trinity' button for activating Trinity glitch pistons.

BINDINGS SETTINGS  
'range' is the range for spinning weapons.  
'fbs_range' is the range for full-body spinning.  
'PreSpinEntrance' is a time at the beginning of the match the AI won't spin, to get further in the arena.  
'clockwise' value of 1 makes the full-body spin direction right/clockwise.  Any other value makes it left/counterclockwise.  
'chase_time' is the time interval in seconds with no hits after which the AI will stop spinning temporarily and chase down the opponent.  
'Pulse' is the number of ticks the active weapon should stay on PLUS the number of ticks it stays off.  A tick is 1/8 second.  
'Coast' is the number of ticks the active weapon should turn off and coast for.  This should be less than the Pulse value.  For equal  times on/off, set Coast equal to half of Pulse.  
'SRcycle' is the number of ticks the weapon should spin in one direction before reversing when attempting to self right.  
NOTE:  You must have the correct ID numbers of the bot's weapons in Bindings.py for the chase_time feature to work!!!  

### Bumblebee, Madiaba
"Same as FBS_2, but needs custom def Turn in order to be invertible."  
Uses standard 'LeftRight' control for spinning.  'Spin' button for active weapons.  
BINDINGS SETTINGS  
'range' is the range for spinning weapons.  
'fbs_range' is the range for full-body spinning.  
'PreSpinEntrance' is a time at the beginning of the match the AI won't spin, to get further in the arena.  
'right' value of 1 makes the full-body spin direction right/clockwise.  Any other value makes it left/counterclockwise.  
'chase_time' is the time interval in seconds with no hits after which the AI will stop spinning temporarily and chase down the opponent.  
NOTE:  You must have the correct ID numbers of the bot's weapons in Bindings.py for the chase_time feature to work!!!  

### SnS_2Invertible, apanx
Based on older version of FBS_2. SnS that spins same direction when inverted.

### Thwack3
"Same as FBS_2 but modified to better suit T-Wrex style thwack/rammer hybrids."  
Uses standard 'LeftRight' control for spinning.  'Spin' button for active weapons.  'Trinity' button for activating Trinity glitch pistons.  
Use 'sweapons' to designate ONLY the thwacking tail weapons--the AI will stop thwacking when these break.  
Use 'weapons' to designate ALL weapons, front and back.

BINDINGS SETTINGS  
'range' is the range for spinning weapons.  
'fbs_range' is the range for full-body spinning.  
'PreSpinEntrance' is a time at the beginning of the match the AI won't spin, to get further in the arena.  
'clockwise' value of 1 makes the full-body spin direction right/clockwise.  Any other value makes it left/counterclockwise.  
'chase_time' is the time interval in seconds with no hits after which the AI will stop spinning temporarily and chase down the opponent.  
'Pulse' is the number of ticks the active weapon should stay on PLUS the number of ticks it stays off.  A tick is 1/8 second.  
'Coast' is the number of ticks the active weapon should turn off and coast for.  This should be less than the Pulse value.  For equal times on/off, set Coast equal to half of Pulse.  
'SRcycle' is the number of ticks the weapon should spin in one direction before reversing when attempting to self right.  
NOTE:  You must have the correct ID numbers of the bot's weapons in Bindings.py for the chase_time feature to work!!!  

## FBSpinner
OBSOLETE - Use FBS.  
Basic Sit and Spin.

## FireDelayStop, ClickBeetle
"Delays initial weapon firing separate from reload and stops while weapon is firing."

## Flipper2, Clickbeetle
Flipper2.py last updated 6/9/14 by Clickbeetle  
This AI will act normally as long as the opponent is moving.  If the opponent stops moving, this AI will also stop and wait for the opponent to be counted out.  If the opponent starts moving again, so will this AI.  In a rumble, this AI will ignore any bots that aren't moving and will only stop if all opponents stop.

Has support for two smart zone-based weapons and one analog-controlled spinner.  Name the smart zones "flip" and "weapon" and the controls "Flip", "Fire", and "Spin".  "Srimech" control for self-righting.  Note you must put 'UseSrimech':1 in Bindings.py to self-right with the Srimech control; otherwise it will use Flip.  You can set component id's in 'sweapons' to become invertible once those components break.  If you use this AI with a vertical spinner, put a smart zone called "flip" or "weapon" in front (doesn't matter which).  This is needed so the AI knows when it hits something.

CUSTOMIZABLE SETTINGS:  
'EnemyMoveRadius' sets how far the enemy must move in order to be considered mobile.  Default is 1.  
'EnemyMoveTime' sets how long (in seconds) the enemy has to move the required distance before being considered immobile.  Default is 3.  
'cooldown' is the time (in seconds) after the AI flips the opponent in which enemy movement won't reset the immobility checker.  Basically this is to let the opponent land and settle down before the AI starts counting movement as "being mobile".  Should be high for powerful flippers and low for weak ones.  Default is 3.  
'PrioritizeFlipper' if set to 1, the AI won't fire the other weapon until the flipper fires.  Useful for bots that use the flipper to get under opponents.  When all of self.weapons are lost, the flipper will stop firing and the other weapon will fire even when the flipper doesn't.  The flipper component id's should therefore be set in self.weapons and no other id's for this to work.  Default is 0.  
'NoChassisTime' sets how long (in half-seconds) the AI will wait to find the chassis before giving up and firing, when there are components in the smart zone.  ONLY WORKS FOR SECONDARY WEAPON, NOT FLIPPER so wire the bot and name the controls like you are using Omni or Popup.py if you use this.  Default is 1.  
'SrimechInterval' sets how often the AI fires the srimech when attempting to self-right.  Srimech will fire once every X seconds.  Default is 1.  

Update 6/9/14: Revamped code to reduce occurrence of "flipper staredowns" in flipper vs. flipper battles.  Added ability to become invertible once 'sweapons' components break.

### NeptuniaSys
Variant of Flipper2 by Bildschirm
Supports more smartzones compared to Flipper2

## Flyer
Spins and fire pistons to fly

## Frenzy
Somehow like Whipper.py but is intended for special use on spin motor hammers (the only legal one being the geared Beta burst)  
Self-rights with the hammer.  
Note: To use only if the hammer uses spin motors, and it is NOT compatible with other weapons.  
Use normal bindings, and wire the hammer with an analog control named "Hammer"  

## FRWL (FromRussiaWithLove)
"The Clamp/Spin AI for From Russia With Love!"  
A Spinner with a smartzone triggering clamping weapon

## Grime
Spinner that pulses spinner when enemy is near. Also fires weapons when enemy in zone.

## HoldPoker, apanx
Waits before triggering when bot is in zone

## HorzSpinner, apanx
Horizontal Spinner that stops disc when inverted for easier deployment of SRM. Also fires trigger for zone.

## InMyArms2, PhiletBabe
"take foe into its arms"

## InvertSwitchWep
VARIANT of SwitchWep
"Switches weapons when one breaks and drives inverted when the srimech breaks."

## Kheper, Clickbeetle
"AI for invertible dustpan-style bots.  Which pretty much just means Kheper."  
Use variable 'NoChassisTime' in Bindings.py to set the amount of time in seconds the AI will wait to find the chassis before giving up and firing, when there are components in the smart zone.

## LaserguidedV2, PhiletBabe
"spinning weapon monted on servo motor tend to aim toward ennemy bot"  
brought to you by PhiletBabe with the help of the incredible Madiaba  
same as laserGuided but use Madiaba SMFE_TurretMachinGun Aiming functions

## LaserGuidedV3, PhiletBabe
"spinning weapon monted on servo motor tend to aim toward ennemy bot"  
brought  to you by PhiletBabe with the help of the incredible Madiaba  
same as laserGuided but use Madiaba SMFE_TurretMachinGun Aiming functions  
binding :  
mayFire :True if piston or burst motor attached to servo  
servonose : angle factor  of attachement of extender to the servo ( typical value 1,-1, 0,25,0.5, -0,25, -0.5)  
list.append(("myBotName","LaserGuidedV3",{ 'servonose':1, 'range':80, 'radius':0.5, 'servospeed':60, 'topspeed':99, 'mayFire':False, 'throttle':130,'weapons':(1,2,3,4,5,6,7,8,9)}))  
name of Servo controler is 'Servo'  
name of Firind controler attached to servo is 'ServoFire'  

## Maatet, PhiletBabe
"Omni strategy with use of 1 servo motor"

class spin servo : like omni AI but allow the monitoring of 1 servo motor.  
the servo motor may be mount to spin horizontaly or verticvaly  
minimum binding.py declaration :    list.append(("mBotName","OmniServo",{'weapons':( 1)}))  
maximum binding.py declaration :   list.append(("myBotName","OmniServo",{'minangle':value, 'maxangle':value, 'servoVS':value, 'delta':value, 'servospeed':value,'weapons':(1)}))

role of arguments and default value  
minangle : angle the servo motor tries to reach when ennemy bot in custom zone named 'zoneservo2'. Default : 0 (radian)  
maxangle : angle the servo motor tries to reach when ennemy bot in custom zone named 'zoneservo1'. Default: math.pi (radian)  
servospeed :  speed of the servo motor.  Default : 30 (hight for a servo !)  
delta :  servo motor is rarely equal to minangle or maxangle, so the servomotor oscillate widly  (like the beautiful music of 'the smiths'.) around theses angles  
the value of delta define the tolerance arounf min/max angle to treat current angle as min/max angle  
servoVS : mostly use if the servo motor spin verticaly : may autorize only positive of negatives angles. Useful for the realistic rules.  
servoVS = 1 : only positives angles / servoVS = -1 : only negatives values / ServoVS = 0 : no control. Default : 0  
TO IMPROVE : problems when the bot is inverted  
bot construction : must have a servo-motor controler  named 'Servo'.  
must have 2 custom zones named 'zoneservo1' and 'zoneservo2'  
must have only 1 servo motor in its components, otherwise only the last one will be controlled.  
note1 :  RA2 angles goes from -math.pi to Math.pi. spinning clockwise (positive servospeed) decrease angle.  
note2:  sometime your bot may fly, lovely but fully useless  
note3: TO IMPROVE :give bad result when others custom zones (ie 'weapon'for piston or 'flip' )  exists  
author : PhiletBabe supported by the irreplaceable Madiaba. 2008

## MadTactics
Set of Tactics used for MultiBotAttacker and MultiBotAttacker. Also contains Tactic adapted for Jousting Arena.

## MultiBotAttacker, MultiBotBaiter, Madiaba
Makes two bots from the same team interleave between baiting and engaging enemy bots. AI one with Attacker and the other with Baiter. Needs MadTactics

## NefariusAI, Trovaner?
"An AI specially designed to complement Trovaner's AW-NefariusBeing."  
A more universally friendly version will be released on a later date.  
I just wanted to get my bot working before the Robo Zone 2 deadline.  

## Octane, JoeBlo
FBS-style AI

## Octane2, JoeBlo
Spinner and fires trigger

## Omni, Starcore, Clickbeetle
Universal AI, uses the Engage tactic. Can spin and trigger and use a SRM. Tactic to use is specifiable.  
Simply put 'tactic':"Ram" (or "Charge") in Bindings to make the AI use rammer/pusher tactics.  No more need for OmniRam.py or any of those!

### EcoOmni
Has the option of using a smart zone for spinner activation.  Name this zone "spin" and then put 'UseSpinZone':1 in Bindings.  Set 'range' to something high like 99.  
'StartSpinup' is the time at the beginning of the match for which the AI should spin its weapons, to get them going.  Measured in seconds.  Default is 2.  Some bots can't move unless this is greater than 0.  
Has the option for pulsing a spinner, rather than running it constantly, if the enemy is outside of a certain range.  Good for shell spinners that can't drive straight when the weapon is running.  
'Pulse' is the number of ticks the active weapon should stay on PLUS the number of ticks it stays off.  A tick is 1/8 second.  
'Coast' is the number of ticks the active weapon should turn off and coast for.  This should be less than the Pulse value.  For equal times on/off, set Coast equal to half of Pulse.  
'PulseRange' is the range within which the weapon should spin constantly.  A 0 value makes it always pulse.

### EternalFlame, ClickBeetle, Naryar
Basically Omni.py with a constantly activated forwards analog control named "Flame", specially for flamethrowers. Brought to you by Clickbeetle, improvement on original FlameOmni.py by Naryar.  
Accepts the same controls as Omni, but you MUST wire your flamethrower to the forward position of an analog named "Flame" to make it work.

### FlameOmni, Naryar
OBSOLETE - Replaced by EternalFlame  
NOTES: This AI is specially designed for flamethrower bots. It will work for all bots that work with Omni, it justs adds special flamethrower lines.  
It uses the flamethrower glitch, aka a flamethrower on an analog control does not weaken as long as you hold the analog control.  
Proper bindings: The flamethrower's activation must be on the positive value of an Analog control that must be named Flame. Also you can add the 'flamerange' value in the bindings.  
That 'flame_range' is the max distance to an opponent the flamethrower will activate, like 'range' on spinners (you still have the range command)  

### OHKORam, Clickbeetle
REQUIRES Ram Tactic by Clickbeetle  
"Rammer that waits for all wheels to touch the ground before driving in order to hit the opponent perfectly head-on."  
Set the start-of-game wait time with 'waittime' in Bindings.  Units are seconds.

### Omnidummy
VARIANT of Omni that spins one control at 80% and one at 100%

### OmniInverted
bot has to be invertible, not mandatory to mention it in your binding, it is force.  
much like omni except that the bot use a button control called 'Inverter' to invert itself if it is not.

### OmniMultiZone
up to 4 zones named weapon1, weapon2, weapon3 and weapon4  
and the associated triggers : Fire1, Fire2, fire3, Fire4  
weaponX is associated with FireX ie : ennemy in customzone weapon3 -> do the action associated with Fire3  
You may also change the default tactics (engage) by specify in the bindings.py 'tactic': XXX  
with XXX = "Charge", "Engage", "Shove", "Ram"  

### OmniRam
Omni using Charge and Shove Tactic  

### OmniRam_EnergyMiser, Madiaba
For Bots with short spin-up time (Face Spinners, Top Spinners, Jugglers,...).  
Saves energy by shutting off weapon motor(s) when NearestEnemy is not near.

### Terraturtle
"Slow OmniRam strategy"  
OmniRam that Inputs Throttle 0.

### OmniServo, PhiletBabe

class omni servo : like omni AI but allow the monitoring of 1 servo motor.  
the servo motor may be mount to spin horizontaly or verticvaly  
minimum binding.py declaration :    list.append(("mBotName","OmniServo",{'weapons':( 1)}))  
maximum binding.py declaration :   list.append(("myBotName","OmniServo",{'minangle':value, 'maxangle':value, 'servoVS':value, 'delta':value, 'servospeed':value,'weapons':(1)}))  
role of arguments and default value  
minangle : angle the servo motor tries to reach when ennemy bot in custom zone named 'zoneservo2'. Default : 0 (radian)  
maxangle : angle the servo motor tries to reach when ennemy bot in custom zone named 'zoneservo1'. Default: math.pi (radian)  
servospeed :  speed of the servo motor.  Default : 30 (hight for a servo !)  
delta :  servo motor is rarely equal to minangle or maxangle, so the servomotor oscillate widly  (like the beautiful music of 'the smiths'.) around theses angles  
the value of delta define how wide the servo motor will oscillate. the higher, the wider. Default : 0.2 (radian)  
servoVS : mostly use if the servo motor spin verticaly : may autorize only positive of negatives angles. Useful for the realistic rules.  
servoVS = 1 : only positives angles / servoVS = -1 : only negatives values / ServoVS = 0 : no control. Default : 0  

bot construction : must have a servo-motor controler  named 'Servo'.  
must have 2 custom zones named 'zoneservo1' and 'zoneservo2'  
must have only 1 servo motor in its components, otherwise only the last one will be controlled.  
note1 :  RA2 angles goes from -math.pi to Math.pi. spinning clockwise (positive servospeed) decrease angle.  
note2:  seems to have problem when stopping servo ( selfinput("Servo",0,0) )   
note3:  sometime your bot may fly, lovely but fully useless  
note4: give bad result when others custom zones (ie 'weapon'for piston or 'flip' )  exists  
author : PhiletBabe supported by the irreplaceable Madiaba. 2008  


### OmniSpin
VARIANT of Omni that uses the Spinner variant of RobotInRange

### OmniSwitch, Philetbabe
Spins and fires weapon when inverted

### OmniTrueRam
"OmniRam strategy with the real Ram and not Push."

### OmniVSpinner
OBSOLETE - Use VertSpinner

### InvertOmni
"Drive inverted when the srimech breaks."

### InvertOmni2
"Omni that can be invertible and fire a srimech at the same time."

### Popup
"Like Omni, but waits for chassis contact before firing the weapon.  If chassis is not found by a certain time, then fires anyway."  
Use variable 'NoChassisTime' in Bindings.py to set the amount of time in half-seconds the AI will wait to find the chassis before giving up and firing, when there are components in the smart zone.  
Set variable 'RunUpsideDown' to 1 for bots that flip over at the beginning of the match and fight upside down.  Such bots must be invertible as well.  
Set srimech component ID's in 'sweapons' to make the bot invertible after the srimech breaks.  
UPDATE 7/4/11: Added support for upside down bots, conditional invertibility, and made AI fire srimech if the bot is stuck on its rear.  

PopupMultiZone, Naryar
"Like Popup strategy, up to 4 zones and the classical Fire/Weapon/Srimech"  
up to 4 zones named weapon1, weapon2, weapon3 and weapon4  
and the associated triggers : Fire1, Fire2, fire3, Fire4  
weaponX is associated with FireX ie : ennemy in customzone weapon3 -> do the action associated with Fire3  
You may also change the default tactics (engage) by specify in the bindings.py 'tactic': XXX  
with XXX = "Charge", "Engage", "Shove", "Ram"  
Ripped off Popup.py and OmniMultiZone.py  

### RangeOmni
Spinner that triggers Fire if enemy is inside certain range

### SpinnerOmni
Special AI for SFTW

### SpinServo, PhiletBabe
"Omni strategy with use of 1 servo motor"

class spin servo : like omni AI but allow the monitoring of 1 servo motor.  
the servo motor may be mount to spin horizontaly or verticvaly  
minimum binding.py declaration :    list.append(("mBotName","OmniServo",{'weapons':( 1)}))  
maximum binding.py declaration :   list.append(("myBotName","OmniServo",{'minangle':value, 'maxangle':value, 'servoVS':value, 'delta':value, 'servospeed':value,'weapons':(1)}))

role of arguments and default value  
minangle : angle the servo motor tries to reach when ennemy bot in custom zone named 'zoneservo2'. Default : 0 (radian)  
maxangle : angle the servo motor tries to reach when ennemy bot in custom zone named 'zoneservo1'. Default: math.pi (radian)  
servospeed :  speed of the servo motor.  Default : 30 (hight for a servo !)  
delta :  servo motor is rarely equal to minangle or maxangle, so the servomotor oscillate widly  (like the beautiful music of 'the smiths'.) around theses angles  
the value of delta define the tolerance arounf min/max angle to treat current angle as min/max angle  
servoVS : mostly use if the servo motor spin verticaly : may autorize only positive of negatives angles. Useful for the realistic rules.  
servoVS = 1 : only positives angles / servoVS = -1 : only negatives values / ServoVS = 0 : no control. Default : 0  
TO IMPROVE : problems when the bot is inverted  
bot construction : must have a servo-motor controler  named 'Servo'.  
must have 2 custom zones named 'zoneservo1' and 'zoneservo2'  
must have only 1 servo motor in its components, otherwise only the last one will be controlled.  
note1 :  RA2 angles goes from -math.pi to Math.pi. spinning clockwise (positive servospeed) decrease angle.  
note2:  sometime your bot may fly, lovely but fully useless  
note3: TO IMPROVE :give bad result when others custom zones (ie 'weapon'for piston or 'flip' )  exists  
author : PhiletBabe supported by the irreplaceable Madiaba. 2008

### SpinupOmni2
"Waits for weapon to spin up before moving.  Also reverses weapon if it gets jammed."  
Update 7/24/12: Fixed AI not moving to avoid immobility when the weapon is jammed.  

***CUSTOMIZABLE SETTINGS***  
'ticks' sets how many times per tick the AI checks its RPM (Revolutions Per Minute) (a tick is 1/8 second).  Needs to be high for accurate measurements on fast spinners, but too high causes lag.  Default is 3.75 (=30 times/second).  
***NOTE*** RA2 can't measure times less than 1/30 second.  Therefore the RPM calculator is only accurate for speeds of 1500, 750, 500, 375, 300, and <250 RPM.  Speeds over 1500 RPM can't be measured, and accuracy decreases with increasing RPM.  
'MotorID' tells the AI which motor to measure RPM on.  
'Motor2ID' (Optional) Set ID for a second motor to measure RPM on.  
'TargetRPM' is the RPM the weapon needs to be spinning at before the AI will move.  (With two motors, only one needs to exceed the target RPM.)  Default is 100.  
'DisplayRPM' Set this to 1 to display current RPM, average RPM, and maximum RPM during battle.  Use this to determine ticks and TargetRPM values.  
'JamTime' Sets the amount of time (in seconds) the weapon should be jammed for, before reversing the direction in an attempt to unjam it.  For unidirectional weapons, just set to 999.  Default is 1.5.  

### SwitchDirEcoOmni
VARIANT of an older version of EcoOmni  
"EcoOmni that turns around and drives backward after the primary weapons break."

### SwitchDirPusher, Naryar
VARIANT of SwitchDirRam  
Slight modification of Click's SwitchDirRam, brought to you by Naryar. Simply changes from Rammer to Pusher.

### SwitchDirRam, Clickbeetle
VARIANT of OmniTrueRam  
"Attacks with the back when the front weapon breaks.  Uses Ram tactic."

### SZSpinner, Naryar
"Like Omni, but does not use a range value for a spinning weapon ; instead uses a smartzone"  
IMPORTANT NOTE: This is a WIP and it might not work properly.  
Just like said, this is an Omni AI that activates it's spinning weapon via a smartzone (that you need to name "spinner") rather than a range value.  
For very short spinup time robots (jugglers, drums, face spinners, etc) that only really need to spin their weapons when the opponent is on them.  
Inspired by Madiaba's Arrowhead.py.

### TopPusher
VARIANT of Omni  
"Uses a smart zone to keep pushing bots even when they are on top of this bot."  
Needs a separate analog control named "Push" wired to the drive, and a smart zone named "Push".  
Put 'tactic':"Ram" (or "Charge") in Bindings to make the AI use rammer/pusher tactics.

### TRFBD
Variant of Omni  
"AI for torque reaction full body drums."  
Put 'SpinCycle' in Bindings to make the AI drive back and forth when a bot is in spin range.  It will drive forward for half of the time specified and backwards for the other half.  Measured in ticks (=1/8 seconds).  
If no SpinCycle is specified, the AI will just spin continuously in one direction when in range.

## Pillar, Beetlebros
"Spins good like a thwackbot should!!!"

## PillarPlus
"Thwackper strategy"  
Spins and turns

## Pinner, Naryar
"Pushes without backing up"  
Designed for true pushers, though does NOT back up repeatedly like Pusher.py does.   
In-built average Throttle, Topspeed, Turn and Turnspeed values for easier AI-ing. Also invertible.

## Plow, Philetbabe
"Plows opponent!"

## PokerPlus, Naryar
"Poker strategy"  
Note: it now fires when being immobilized to try to unstuck, as well as firing when stuck on it's rear end. Also you can select the tactic.

## PSIBot, apanx
Uses plus.damage to destroy all enemies, uses plus.force to levitate

## PusherPiston
"Pushes! with the help of pistons"

## PusherPlus
Pusher with Srimech trigger

## RamSnS
"Initially rams the opponent, then sit-and-spins continuously. No smartzone required"

## RangePoker
Poker that triggers Fire if enemy is inside certain range

## Razorbackv3
"Special AI for Razorback v3.  Drives forwards while self righting."

## ServoClamp, Naryar
"Uses servo motor(s) to clamp enemy bot. Variables are the servo ID and the start/end angles of servo movement. Must also pick up the servo's ID number. Can wait for chassis to be in smartzone like Popup.py"  
Use variable 'NoChassisTime' in Bindings.py to set the amount of time in seconds the AI will wait to find the chassis before giving up and clamping, when there are components in the smart zone.

## ShiftWeapon3, PhiletBabe
"the servo has 2, 3 or 4 'fixed' angle position. It shifts periodically from these"  
otherwise, mount protection (snow plow) and shift them, mount tribar, with a 2 position shifting, weapon may be straight to bot nose or may flank opponent.... etc

## Smashbox
Spinner and triggers weapon

## Snow
"Two wedges slide together or apart, plus some wonky self-righteous coding. Really just special for Seism 13."

## SwitchWep
"Switches weapons when one breaks!"

## SwitchWepPopup, Clickbeetle
"Popup that switches to a secondary weapon after primary weapon breaks."  
Use variable 'NoChassisTime' in Bindings.py to set the amount of time in seconds the AI will wait to find the chassis before giving up and firing, when there are components in the smart zone.

## Tank, apanx
Uses Servomotor to aim turret. Uses Annoy Tactic to avoid enemy.

### FlameTank, apanx
Uses Servomotor to aim turret. Flames forward. Uses Annoy Tactic to avoid enemy.

### MGTank, apanx
Uses Servomotor to aim turret. Cycles through triggers for multiple cannons. Uses Annoy Tactic to avoid enemy.

## TempusFugit
NOTE: You must wire your spinner with an ANALOG CONTROL to work!  
NOTE2: When the 'sweapons' specified in Bindings.py break, the bot will become invertible.  
So if your bot isn't ever invertible, you must add 'sweapons':(0,) to the Bindings.py!  
Spin when enemy is close, Switch Spin2 when wheels are not in contact with ground. Trigger Fire for zone weapon

## THZ, JoeBlo
"Frenzy strategy + FBS immobility management"

## THZPlus, JoeBlo, Naryar
"Frenzy strategy + FBS immobility management. Also backs up weapon when not in use and uses NoChassisTime variable like Popup.py"

## Timber2
"AI that stops moving forward while the weapon is retracting (because Timber II's driving applies force to the chassis which hinders retracting)."  
Set the amount of ticks it takes for the weapon to make one complete downward swing with 'FiringTime'.  The AI will continue driving during this time.  
Set the amount of ticks it takes to retract the weapon with 'RetractingTime'.  This time starts once the FiringTime is over.  The AI will not drive forwards during this time.  

## Topknot
Basically Whipper.py (SnS needing a smartzone), with four other independant hammer/popup controls. Also has a smartzone coded for firing all hammers at once.

## Top_Smasher_2R, Madiaba
"Top_Smasher_2R for For Multi_functioning and sequential bots (with optional turret).   "R" means Range firing option."  
NOTES: Bindings' coding for __INIT_ stuff:  
'motor': 5  (5=component number during assembly).  
'altitude': 0.5  (distance above the floor)  
'TimerSpeed3thru4' : 1  (1-5 integer in Bindings line)  
'TimerSpeed5thru8' : 1  (1-5 integer in Bindings line)  
'TimerSpeed1thru7' : 1  (1-5 integer in Bindings line)  
'SRM_TImer' : 1  (1-? integer in Bindings line)  

## UltraAI, apanx
The Greatest AI

## VertSpinner
"Self-rights by reversing the spinner direction and firing additional optional srimech."  
NOTE: You must wire your spinner with an ANALOG CONTROL to work!  
NOTE2: When the 'sweapons' specified in Bindings.py break, the bot will become invertible.  
So if your bot isn't ever invertible, you must add 'sweapons':(0,) to the Bindings.py!  
Update 5/31/11: added analog control for self righting ("Sriturn")  
Update 6/29/12: added customizable feature 'TrollDanceZone'.  This makes the AI spin weapons in reverse for a longer time when self-righting, to avoid "Troll Dancing".  Set to a number between 0 and 1; lower numbers make the weapons spin in reverse for longer.  Default value is 1.  

## VertSpinner2
"Self-rights by cycling the weapon through forward and reverse, and also with an optional srimech."  
The time the spinner spins in each direction while self-righting can be set with 'SRcycle' in Bindings.  Units are ticks (=1/8 second).  Spins for half this time in reverse and half normally.  Default is 12 (=1.5 seconds, 0.75 per direction).  
NOTE: You must wire your spinner with an ANALOG CONTROL to work!  
NOTE2: When the 'sweapons' specified in Bindings.py break, the bot will become invertible.  
So if your bot isn't ever invertible, you must add 'sweapons':(0,) to the Bindings.py!  

## Volley, apanx
As in cannon volley. Modified Poker that always fires. Used to fire several cannons in sequence

## WhipperPlus
WhipperPlus strategy Whipper + FBS immobility management