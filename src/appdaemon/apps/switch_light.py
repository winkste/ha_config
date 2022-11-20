#
# Standard switch - power controller
#
# Refer to the API documentation of Appdaemon:
# https://appdaemon.readthedocs.io/en/latest/HASS_API_REFERENCE.html
#
# Description: 
# App to turn lights on when (sunset - offset * 60sec) and turns off at offTime
# Use with constraints to activate only for the hours of darkness
#
# Signal chart:
#---------------------------------------------------------------------------------------------------
#                Check sunset     Day    sun_set - offset       offTime event
#---------------------------------------------------------------------------------------------------
# swith evt   :____|--|____________|--||--|_________________|--|________________|--||--|____________
# light       :______|------------------|_____________________|----------------------|______________
#
#
# Args:
#
# switch:       switch object that send one or two on/off sequences
# entity_ctrl:  entities to control, can be a light, script, 
#               scene or anything else that can be turned on/off
#
#
# Release Notes
#
# Version 1.0:
#   Initial version of app

import hassapi as hass

class SwitchLight(hass.Hass):
    switch = None
    entity_ctrl = None

    def initialize(self):
        if "switch" not in self.args:
            self.log("switch_light - no switch detected...")
        elif "entity_ctrl" not in self.args:
            self.log("switch_light - no entity control detected...") 
        else:  
            self.switch = self.args["switch"]
            self.entity_ctrl = self.args["entity_ctrl"]
            self.listen_state(self.switch_on_callback, self.switch, new = "on")
            self.listen_state(self.switch_off_callback, self.switch, new = "off")
            self.log("switch_light - controller initialized...")

    def switch_on_callback(self, entity, attribute, old, new, kwargs):
        self.log(f"{self.switch} changed from: {old} to state {new}")
        self._turn_entities_on()

    def switch_off_callback(self, entity, attribute, old, new, kwargs):
        self.log(f"{self.switch} changed from: {old} to state {new}")
        self._turn_entities_off()    
                    
    def _turn_entities_on(self):
        self.log(f"Turn on the entities")
        for entity in self.entity_ctrl:
            self.log("Turn on: " + entity)
            self.turn_on(entity) # turn on the entity
  
    def _turn_entities_off(self):
        self.log(f"Turn off the entities")
        for entity in self.entity_ctrl:
            self.log("Turn off: " + entity)
            self.turn_off(entity) # turn off the entity
    
