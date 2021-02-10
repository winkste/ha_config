import appdaemon.plugins.hass.hassapi as hass

#
# Ambient light controller
#
# Args:
#
# Description: 
# - checks if sun is down and time is 19:00
# - if all conditions are satisfied, turn light on
#       and start timer to turn light off at 22:00
#

class OrientLight(hass.Hass):

  def initialize(self):
    pass