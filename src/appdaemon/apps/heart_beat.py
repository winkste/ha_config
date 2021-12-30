#
# Heart beat and time controller
#
# Refer to the API documentation of Appdaemon:
# https://appdaemon.readthedocs.io/en/latest/HASS_API_REFERENCE.html 
#
# Description: 
# App to cyclic communicate a heart beat and time information.
#
# Signal chart:
#---------------------------------------------------------------------------------------------------
#                
#---------------------------------------------------------------------------------------------------
# cyclic_event:____|---|_______________|---|__________________|---|__________________|---|__________
# period      :____|-------------------|___|------------------|___|------------------|___|----------
# heart beat  :____|---|_______________|---|__________________|---|__________________|---|__________
# time        :____|---|_______________|---|__________________|---|__________________|---|__________
#
#
# Args:
# period - time period in seconds for heart beat and time distribution
#
# Release Notes
#
# Version 1.0:
#   Initial version of app

import hassapi as hass
#import mqttapi as mqtt

class HeartBeat(hass.Hass):
    period = 30
    timer_handle = None
    heart_beat = 0
    my_mqtt = None

    def initialize(self):
        self.heart_beat = 0
        self.my_mqtt = self.get_plugin_api("MQTT")
        #my_mqtt = MyMqtt()
        if "period" in self.args:
            self.period = self.args["period"]
        else:
            self.period = 30
        
        self.timer_handle = None
        self.timer_handle = self.run_in(self.heart_beat_timer_callback, self.period)

    def heart_beat_timer_callback(self, kwargs):
        self.timer_handle = None
        
        # publish heart beat info
        self.heart_beat += 1
        #self.set_value("sensor.dev300_heart_beat", self.heart_beat)
        #self.set_state("sensor.dev300_heart_beat", state=f"{self.heart_beat}")
        if self.my_mqtt.is_client_connected(namespace = 'mqtt'):
            self.my_mqtt.mqtt_publish("std/dev300/s/hb/heart_beat", f"{self.heart_beat}", name = "mqtt")
            self.log(f"Publish heart beat: {self.heart_beat}")
        else:
            self.log(f"MQTT not connected.")

        
        # publish time info
        now = self.get_now()
        time = now.strftime("%d-%m-%Y, %H:%M:%S")
        time_ts = int(self.get_now_ts())
        #self.set_textvalue("sensor.dev300_time_now", time)
        #self.set_state("sensor.dev300_time_now", state=time)
        if self.my_mqtt.is_client_connected(namespace = 'mqtt'):
            self.my_mqtt.mqtt_publish("std/dev300/s/hb/time_now", time, name = "mqtt")
            self.log(f"Publish time: {time}")
        else:
            self.log(f"MQTT not connected.")
        #self.set_textvalue("sensor.dev300_ts_now", time_ts)
        #self.set_state("sensor.dev300_ts_now", state=time_ts)
        if self.my_mqtt.is_client_connected(namespace = 'mqtt'):
            self.my_mqtt.mqtt_publish("std/dev300/s/hb/ts_now", time_ts, name = "mqtt")
            self.log(f"Publish time: {time_ts}")
        else:
            self.log(f"MQTT not connected.")

        # restart the timer for the next cycle
        self.timer_handle = self.run_in(self.heart_beat_timer_callback, self.period)
