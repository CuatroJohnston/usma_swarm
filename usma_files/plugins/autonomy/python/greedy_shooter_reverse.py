'''
Tactic Name: Greedy Shooter Reverse (GreedyShooterRev)
Description:  This tactic is a variation of the GreedyShooterInt in greedy_shooter_int.py
              The tactic calculates the heading/bearing of the enemy.  If the Blue UAV is on a head-on course, it
              climbs to force the Red UAV to try to catch it.  It then maneuvers around 180 degrees and performs
              a dive attack on the rear of the Red UAV.
Date:		13 Dec 2016
Authors:	USMA SASC Team
'''

import numpy as np
import autopilot_bridge.msg as apbrg
import ap_msgs.msg as apmsg
from autopilot_bridge.msg import LLA
import ap_lib.gps_utils as gps
import ap_lib.ap_enumerations as enums
import math
import ap_lib.sasc_scrimmage as ss

class GreedyShooterRev(ss.Tactic):

    def init(self, params):
        self._id = int(params['id'])
        self._last_lat = None
        self._last_lon = None
        self._speed = None
        self._heading = None
        self._target_id = None
        self._target_count = 0
        self._target_dist = np.inf
        self._target_last_lat = None
        self._target_last_lon = None
        self._target_heading = None
        self._target_speed = None
        self._wp = np.array([0, 0, 0])
        self._max_range = enums.MAX_RANGE_DEF
        self._fov_width = enums.HFOV_DEF
        self._fov_height = enums.VFOV_DEF
        self._own_pose = apbrg.Geodometry()
        self._blues = dict()
        self._reds = dict()
        self._reds_shot = set()
        self._safe_waypoint = np.array([0, 0, 0])
        self._action = ["None", 0]
        self._name = 'GreedyShooterInt'
        self._state = "HUNT"               # states are HUNT, MANEUVER, ATTACK

    def step_autonomy(self, t, dt):

        # Reset the action and target ID every loop
        self._action = ["None", 0]

############################################################
# If self._target_id is not None and in the shot group
# then reset to None, otherwise set to last_target
############################################################

        min_dist = self._target_dist
        for uav in self._reds.values():
            if uav.vehicle_id not in self._reds_shot:
                uav_lat = uav.state.pose.pose.position.lat
                uav_lon = uav.state.pose.pose.position.lon
                d = gps.gps_distance(self._own_pose.pose.pose.position.lat,\
                                     self._own_pose.pose.pose.position.lon,\
                                     uav_lat,\
                                     uav_lon)

                if d < min_dist:
                    min_dist = d
                    self._target_id = uav.vehicle_id


        if self._target_id in self._reds_shot:
            self._target_id = None
            self._target_dist = np.inf
            self._target_count = 0
            self._target_last_lat = None
            self._target_last_lon = None
            self._target_heading = None
            self._target_speed = None

        # If a target has been identified, move towards it
        if self._target_id != None:
            own_lat = self._own_pose.pose.pose.position.lat
            own_lon = self._own_pose.pose.pose.position.lon

            if self._last_lat is not None:
                self._speed = gps.gps_distance(own_lat, own_lon,\
                                     self._last_lat, self._last_lon) / 0.1
                self._heading = gps.gps_bearing(self._last_lat, self._last_lon, own_lat, own_lon)

            self._last_lat = own_lat
            self._last_lon = own_lon

            target_pos = self._reds[self._target_id].state.pose.pose.position
            tgt_lat = target_pos.lat
            tgt_lon = target_pos.lon
            tgt_alt = target_pos.rel_alt

            d = gps.gps_distance(self._own_pose.pose.pose.position.lat,\
                                     self._own_pose.pose.pose.position.lon,\
                                     tgt_lat,\
                                     tgt_lon)

            if self._target_last_lat is not None:
                self._target_speed = gps.gps_distance(tgt_lat, tgt_lon,\
                                     self._target_last_lat, self._target_last_lon) / 0.1
                self._target_heading = gps.gps_bearing(self._target_last_lat, self._target_last_lon, tgt_lat, tgt_lon)
                #print "ID: %d   Target: %d" % (self._id, self._target_id)
                #print "Lat: %f  Lon: %f  Head: %f   T_lat: %f  T_lon %f  T_head: %f" % (own_lat, own_lon, self._heading, \
                    #tgt_lat, tgt_lon, self._target_heading)

            self._target_last_lat = tgt_lat
            self._target_last_lon = tgt_lon

#############################################################################
# Calc intercept point
# Reference:  http://jaran.de/goodbits/2011/07/17/calculating-an-intercept-course-to-a-target-with-constant-direction-and-velocity-in-a-2-dimensional-plane/
# Translated from Java to Python
#############################################################################
            t = None
            if self._target_heading is not None: 
                s = self._speed
                ox = tgt_lat - own_lat
                oy = tgt_lon - own_lon
                vx = self._target_speed * math.cos(self._target_heading) # sin
                vy = self._target_speed * math.sin(self._target_heading) # cos
                h1 = vx**2 + vy**2 - s**2
                h2 = ox*vx + oy*vy

                if h1 == 0:
                    t = -(ox**2 + oy**2)/(2*h2)
                else:
                    minusPHalf = -h2/h1
                    disc = minusPHalf**2 - (ox**2 + oy**2)/h1
                    if disc < 0:
                        t = None
                    else:
                        root = math.sqrt(disc)
                        t1 = minusPHalf + root
                        t2 = minusPHalf - root
                        tmin = t1 if t1 < t2 else t2
                        tmax = t1 if t1 > t2 else t2

                        t = tmin if tmin > 0 else tmax

                        if t < 0:
                            t = None

            if t is not None:
                t_adj = 0 # add extra time for tweaking
                int_lat = tgt_lat + vx * (t+t_adj)
                int_lon = tgt_lon + vy * (t+t_adj)
                int_dist = gps.gps_distance(own_lat, own_lon, int_lat, int_lon)
                bearing = gps.gps_bearing(own_lat, own_lon, int_lat, int_lon)
                
                lat, lon = gps.gps_newpos(own_lat, own_lon, bearing, int_dist+1000)
                #print "Using intercept Lat: %f  Lon: %f   Time: %f" % (lat, lon, t)  #  I_lat: %f  I_lon: %f  t: %f
            else:
                bearing = gps.gps_bearing(own_lat, own_lon, tgt_lat, tgt_lon)  # use standard TutorialGreedyShooter method of new waypoint
                lat, lon = gps.gps_newpos(own_lat, own_lon, bearing, 1000)   # range was 1000
                #print "Using bearing %f to Lat: %f  Lon: %f" % (bearing, lat, lon)

            # Set the waypoint past the current target, so we don't go into a loiter mode

            self._wp = np.array([lat, lon, target_pos.rel_alt])

            # Determine if the target is within firing parameters
            if gps.hitable(self._own_pose.pose.pose.position.lat, \
                           self._own_pose.pose.pose.position.lon, \
                           self._own_pose.pose.pose.position.rel_alt, \
                           (self._own_pose.pose.pose.orientation.x, \
                            self._own_pose.pose.pose.orientation.y, \
                            self._own_pose.pose.pose.orientation.z, \
                            self._own_pose.pose.pose.orientation.w ), \
                           self._max_range, self._fov_width, self._fov_height,\
                           tgt_lat, tgt_lon, tgt_alt):
                self._action = ["Fire", self._target_id]
                #print "GS Int=============================>ID: %d shot at Target %d" % (self._id, self._target_id)

        else:
            # If a target hasn't been identified, return to the safe waypoint
            self._wp = self._safe_waypoint
        return True
