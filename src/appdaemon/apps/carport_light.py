import appdaemon.plugins.hass.hassapi as hass

#
# Carport light controller
#
# Args:
#
# Description: 
# - checks if motion is detected in two sensors
# - checks if light is manual switched on
# - checks if sun is down
# - if all conditions are satisfied, turn two lights on
#       and start timer to turn lights off after X seconds
# - if motion is detected during timer counting, the timer
#       is restarted 
# entities:
# - binary_sensor.dev03_motion
# - binary_sensor.dev62_motion
# - light.dev03
# - light.dev63

class CarportLight(hass.Hass):


  def initialize(self):
    self.log('carport light controller initialized...')
    self.sensor1 = 'binary_sensor.dev03_motion'
    self.sensor2 = 'binary_sensor.dev62_motion'
    self.light1 = 'light.dev03'
    self.light2 = 'light.dev62'
    self.light_delay = self.args["configs"] 
    self.listen_state(self.motion, self.sensor1, new = 'on')
    self.listen_state(self.motion, self.sensor2, new = 'on')
    self.listen_state(self.light_state, self.light1, new = "on")
    self.listen_state(self.light_state, self.light2, new = "on")
    self.timer = None

  def light_state(self, entity, attribute, old, new, kwargs):
    self.log("light on: " + entity)

  def motion(self, entity, attribute, old, new, kwargs):
    self.log("motion detected: " + entity)
    if self.sun_down():   # check that it is still dark
      if ((self.get_state(self.light1) == "on") or
          (self.get_state(self.light2) == "on")) and (None == self.timer): # check for manual turn on the light
        self.log('motion detected, but light manuel turned on')
      else:
        if self.get_state(self.light1) == "off":
          self.turn_on(self.light1) # turn on the light
          self.log("light1 turned on: " + self.light1)
        if self.get_state(self.light2) == "off":
          self.turn_on(self.light2) # turn on the light
          self.log("light2 turned on: " + self.light2)
        if None != self.timer:  # check if timer is already running, means new motion detected within a timer cycle 
          self.cancel_timer(self.timer) # cancel that timer for restarting
        self.timer = self.run_in(self.light_off, self.light_delay) # start timer to turn of the light with delay

  def light_off(self, kwargs):
    if (self.get_state(self.sensor1) == "on") or (self.get_state(self.sensor2) == "on"): # check if sensor is still in motion
      self.timer = self.run_in(self.light_off, self.light_delay) # yes, restart timer
      self.log('in light off, motion still detected, restart timer...')
    else:
      self.turn_off(self.light1) # turn off the light
      self.log("light1 turned off: " + self.light1)
      self.turn_off(self.light2) # turn off the light
      self.log("light2 turned off: " + self.light2)
      self.timer = None