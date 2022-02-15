#
# Alarm Controller
#
# Refer to the API documentation of Appdaemon:
# https://appdaemon.readthedocs.io/en/latest/HASS_API_REFERENCE.html
#
# Description: 
# Controls the alarm handling and reaction
#
# Signal chart:
#---------------------------------------------------------------------------------------------------
#                                    Alarm                      Home
#---------------------------------------------------------------------------------------------------
# armed_away:_______________|-----------------------------|___|------|______________________________
# disarmed  :---------------|_____________________________|---|______|------------------------------
# any_motion:_________________|-|_________|-|___________________|-|_________________________________
# alarm_tmr :_________________|-----|___________________________|----|______________________________
# scene_plr :_______________________|---------------------|_________________________________________
#
#
#
# Args:
#
# alarm_offset = Timeout after motion detected to start alarm sequence player
# 
# Signals:
# alarm_control_panel.ha_alarm:
#   - disarmed
#   - arming
#   - armed_away
#   - arm_night
#
# Release Notes
#
# Version 1.0:
#   Initial version of app

import hassapi as hass

class AlarmCtrl(hass.Hass):
    alarm_timer = None
    alarm_offset = 30
    alarm_activated = False
    scene_timer_red = None
    scene_timer_blue = None

    def initialize(self):
        '''
            Initialization function of class.
        '''
        # handle arguments
        if "alarm_offset" in self.args:
            self.alarm_offset = self.args["alarm_offset"]
        else:
            self.alarm_offset = 30
        
        # listen to alarm control panel for state changes armed_away and disarmed
        self.listen_state(self._alarm_control, "alarm_control_panel.ha_alarm")

        # listen to all motion and door/window sensors that can trigger the alarm
        self.listen_state(self._motion_detected, "binary_sensor.dev72_motion", new = "on")

        # can we use multiple callbacks for the same entity here? one for night and one for away?

        self.log("alarm controller initialized...")

    def _alarm_control(self, entity, attribute, old, new, kwargs):
        '''
            Callback function for changes of the alarm control panel.
        '''
        self.log(f"alarm controller state changed from: {old} to: {new}")
        if new == "armed_away":
            pass
        if new == "arm_night":
            pass
        elif new == "arming":
            pass
        elif new == "disarmed":
            self._stop_alarm_sequence()
        else:
           self.log(f"alarm controller unexpected state change from: {old} to: {new}") 

    def _stop_alarm_sequence(self):
        '''
            Function that stops all timer and turns light of
        '''
        if None != self.alarm_timer:
            self.cancel_timer(self.alarm_timer)
        self.turn_on("scene.motion_light_blue")
        self.turn_on("scene.motion_light_off")
        if None != self.scene_timer_red:
            self.cancel_timer(self.scene_timer_red)
        if None != self.scene_timer_blue:
            self.cancel_timer(self.scene_timer_blue)
        self.alarm_activated = False
        self.log("alarm controller alarm sequence deactivated")

    def _motion_detected(self, entity, attribute, old, new, kwargs):
        '''
            Callback function for motion, or door/window open detected.
        '''
        if self.get_state("alarm_control_panel.ha_alarm") == "armed_away":
            if False == self.alarm_activated:
                self.log(f"alarm controller motion detected by: binary_sensor.dev72_motion, start alarm sequence")
                self.alarm_activated = True
                self.alarm_timer = self.run_in(self._start_alarm, self.alarm_offset)
    
    def _start_alarm(self, kwargs):
        '''
            Callback function for alarm start timer.
        '''
        if None != self.alarm_timer:
            self.cancel_timer(self.alarm_timer)
        self.log("alarm controller alarm started")
        self.turn_on("scene.motion_light_red")
        self.scene_timer_red = self.run_in(self._activate_scene_red, 2)
        self.scene_timer_blue = self.run_in(self._activate_scene_blue, 1)
    
    def _activate_scene_red(self, kwargs):
        '''
            This function is used to switch the multi color lights to red.
        '''
        if True == self.alarm_activated:
            self.scene_timer_red = self.run_in(self._activate_scene_red, 1)
            self.turn_on("scene.motion_light_red")

    def _activate_scene_blue(self, kwargs):
        '''
            This function is used to switch the multi color lights to blue.
        '''
        if True == self.alarm_activated:
            self.scene_timer_blue = self.run_in(self._activate_scene_blue, 1)
            self.turn_on("scene.motion_light_blue")


