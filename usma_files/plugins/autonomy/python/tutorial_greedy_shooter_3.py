import numpy as np
import autopilot_bridge.msg as apbrg
import ap_msgs.msg as apmsg
from autopilot_bridge.msg import LLA
import ap_lib.gps_utils as gps
import ap_lib.ap_enumerations as enums
import ap_lib.sasc_scrimmage as ss
import random

MIN_DIST = 1000

class TutorialGreedyShooterSingle(ss.Tactic):

    def init(self, params):
        self._id = int(params['id'])
        self._target_id = -1
        self._last_target = None
        self._wp = np.array([0, 0, 0])
        self._max_range = enums.MAX_RANGE_DEF
        self._fov_width = enums.HFOV_DEF
        self._fov_height = enums.VFOV_DEF
        self._own_pose = apbrg.Geodometry()
        self._blues = dict()
        self._reds = dict()
        self._shot = set()
        self._safe_waypoint = np.array([0, 0, 0])
        self._action = ["None", 0]
        self._name = 'TutorialGreedyShooter'
        self._last_update = 0
        self._got_target = False
        self._min_dist = np.inf

    def step_autonomy(self, t, dt):

        # Reset the action and target ID every loop
        self._action = ["None", 0]
        self._target_id = self._last_target

        # Search for the closest target every frame if you don't already have one
        min_dist = np.inf   # self._min_dist
        if self._got_target is False:
            for uav in self._reds.values():
                if uav.vehicle_id not in self._shot:
                    d = gps.gps_distance(self._own_pose.pose.pose.position.lat,\
                                     self._own_pose.pose.pose.position.lon,\
                                     uav.state.pose.pose.position.lat,\
                                     uav.state.pose.pose.position.lon)

                    if d < min_dist:
                        min_dist = d
                        self._target_id = uav.vehicle_id
                        self._last_target = self._target_id
                        
                        if d < MIN_DIST:
                            self._got_target = True
                        else:
                            self._got_target = False

        else:
            self._got_target = False
            self._last_target = None
            for uav in self._reds.values():
                if uav.vehicle_id not in self._shot:
                    if self._target_id == uav.vehicle_id:
                        self._last_target = self._target_id
                        self._got_target = True

                            

        # If a target has been identified, move towards it
        if self._target_id != None:
            target_pos = self._reds[self._target_id].state.pose.pose.position
            # print "*************************************"
            print "ID: %d   Target ID: %d\n" % (self._id, self._target_id)
            
            own_lat = self._own_pose.pose.pose.position.lat
            own_lon = self._own_pose.pose.pose.position.lon
            tgt_lat = target_pos.lat
            tgt_lon = target_pos.lon
            tgt_alt = target_pos.rel_alt

            # Set the waypoint past the current target, so we don't go into a
            # loiter mode
            bearing = gps.gps_bearing(own_lat, own_lon, tgt_lat, tgt_lon)
            lat, lon = gps.gps_newpos(own_lat, own_lon, bearing, 1000)

            self._wp = np.array([lat, lon, tgt_alt])  # np.array([lat, lon, target_pos.rel_alt])

            # Determine if the target is within firing parameters
            if gps.hitable(self._own_pose.pose.pose.position.lat, \
                           self._own_pose.pose.pose.position.lon, \
                           self._own_pose.pose.pose.position.rel_alt, \
                           (self._own_pose.pose.pose.orientation.x, \
                            self._own_pose.pose.pose.orientation.y, \
                            self._own_pose.pose.pose.orientation.z, \
                            self._own_pose.pose.pose.orientation.w ), \
                           self._max_range, self._fov_width, self._fov_height,\
                           target_pos.lat, target_pos.lon, target_pos.rel_alt):
                self._action = ["Fire", self._target_id]
                self._last_target = None
                self._got_target = False

        else:
            # Start at the safe waypoint
            self._wp = self._safe_waypoint

        return True
