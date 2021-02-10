import appdaemon.plugins.hass.hassapi as hass

#
# Motion light controller
#
# Args:
#
# Description: 
# - checks if motion is detected 
# - checks if light is manual switched on
# - checks if sun is down
# - if all conditions are satisfied, turn light on
#       and start timer to turn light off after X seconds
# - if motion is detected during timer counting, the timer
#       is restarted 
#
#

class MotionLight(hass.Hass):

  def initialize(self):
    self.log("motion light controller application initialized...")
    self.sensor = self.args["sensors"]
    self.light = self.args["lights"]
    self.light_delay = self.args["configs"] 
    self.log("Sensor: " + self.sensor + '   Light: ' + self.light + '  Delay: ' + str(self.light_delay)) 
    self.listen_state(self.motion, self.sensor, new = "on")
    self.listen_state(self.light_state, self.light, new = "on")
    self.timer = None

  def light_state(self, entity, attribute, old, new, kwargs):
    self.log(" Light state on detected for " + self.light)

  def motion(self, entity, attribute, old, new, kwargs):
    self.log("motion detected for: " + self.sensor)
    if self.sun_down():   # check that it is still dark 
      if (self.get_state(self.light) == "on") and None == self.timer: # check for manual turn on the light
        self.log('motion detected, but light manual turned on')
      else:
        self.turn_on(self.light) # turn on the light
        self.log("light turned on: " + self.light)
        if None != self.timer:  # check if timer is already running, means new motion detected within a timer cycle 
          self.cancel_timer(self.timer) # cancel that timer for restarting
        self.timer = self.run_in(self.light_off, self.light_delay) # start timer to turn of the light with delay

  def light_off(self, kwargs):
    if self.get_state(self.sensor) == "on": # check if sensor is still in motion
      self.timer = self.run_in(self.light_off, self.light_delay) # yes, restart timer
    else:
      self.turn_off(self.light) # turn of light
      self.log("light turned off: " + self.light)
      self.timer = None