import numpy as np
import math
import autopilot_bridge.msg as apbrg
import ap_msgs.msg as apmsg
from autopilot_bridge.msg import LLA
import ap_lib.gps_utils as gps
import ap_lib.ap_enumerations as enums
import ap_lib.sasc_scrimmage as ss

import goto

class GotoDefend(goto.Goto):

    def init(self, params):
        super(GotoDefend, self).init(params)        
        self._name = 'GotoDefend'                
        
    def step_autonomy(self, t, dt):
        status = super(GotoDefend, self).step_autonomy(t, dt)            
        
        # Fire at any reds that are within firing parameters
        for target_id, red in self._reds.iteritems():
            if gps.hitable(self._own_pose.pose.pose.position.lat, \
                           self._own_pose.pose.pose.position.lon, \
                           self._own_pose.pose.pose.position.rel_alt, \
                           (self._own_pose.pose.pose.orientation.x, \
                            self._own_pose.pose.pose.orientation.y, \
                            self._own_pose.pose.pose.orientation.z, \
                            self._own_pose.pose.pose.orientation.w ), \
                           self._max_range, self._fov_width, self._fov_height,\
                           red.state.pose.pose.position.lat, 
                           red.state.pose.pose.position.lon, 
                           red.state.pose.pose.position.rel_alt):
                self._action = ["Fire", target_id]
                        
        return status
