import appdaemon.plugins.hass.hassapi as hass

#
# Sun state controller
#
# Args:
#
# Description: 
# - Runs every sunset and sunrise and logs this event
#
#

class SunChecker(hass.Hass):

  def initialize(self):
    self.log("sun state controller application initialized...")
    self.run_at_sunrise(self.sunrise_callback)
    self.run_at_sunset(self.sunset_callback)


  def sunrise_callback(self, kwargs):
    self.log(" --------- SUNRISE -------------")

  def sunset_callback(self, kwargs):
    self.log(" --------- SUNSET --------------")

