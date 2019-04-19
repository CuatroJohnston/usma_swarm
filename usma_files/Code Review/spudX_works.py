# Performs a sequential greedy waypoint (WP) assignment:
# 1- Determine which UAVs are in your subswarm
# 2- Split up number of wpts to be assigned among subswarm
# 3- Each UAS individually plans for all UAS in the subswarm in sequence follows:
#    - Determine closest point to that UAS, add that point to your bundle
#    - Find next closest point to that point, add to bundle
#    - Repeat until bundle is full.
#    - As waypoints are added to bundle, make them unavailable to others
#    - Repeat this process for each UAS in sequence
# 4- Each UAS then assigns itself its own set of waypoints
# 5- Each UAS is sequenced to navigate through its bundle of waypoints
#
# Ashley Rivera & Conner Russell
# USMA
# Last updated: 15 APR 2019

import numpy as np
import math
import autopilot_bridge.msg as apbrg
import ap_msgs.msg as apmsg
from autopilot_bridge.msg import LLA
import ap_lib.gps_utils as gps
import ap_lib.ap_enumerations as enums
import ap_lib.sasc_scrimmage as ss
import hotspot_grid as usma_enums
import timeit
import socket
import sys
import subprocess
from os.path import expanduser
from geometry_msgs.msg import PointStamped
import rospy
import map_around_central_point as hotspot_grid

DIST2WP_QUAD = 1
DIST2WP_ZEPH = 10
DIST_START_DESCENT = 2
TIME_AT_WP = 1
SAFE_ALT = 100
SURVEY_ALT = 20
BUFFER = 20000
SERVER_FLAG = 1
GROUND_TEST = 1
grid = 0

# If GPS Simulator used, expand distance since quad won't move
if (GROUND_TEST == 1):
    DIST2WP_QUAD = 1000000
    DIST_START_DESCENT = 1000000
    BUFFER = 200000
    TIME_AT_WP = 1

class GreedyGoto(ss.Tactic):

    def init(self, params):
        self._id = int(params['id'])
        self._target_id = -1
        self._wp = np.array([0, 0, 0])
        self._max_range = enums.MAX_RANGE_DEF
        self._fov_width = enums.HFOV_DEF
        self._fov_height = enums.VFOV_DEF
        self._own_pose = apbrg.Geodometry()
        self._blues = dict()
        self._shot = set()
        self._safe_waypoint = np.array([0, 0, 0])
        self._last_ap_wp = np.array([0, 0, 0])
        self._action = ["None", 0]
        self._vehicle_type = int(params['vehicle_type'])
        self._spud = int(params['Survey Number'])
        self.home = expanduser("~")
        self.radeyeDir = self.home + "/scrimmage/usma/plugins/autonomy/python/"
        if (self._spud == 1):
            self._enumList = usma_enums.WP_LOC_RiverCourt
        elif (self._spud == 2):
            self._enumList = usma_enums.WP_LOC_Range11
        self._name = 'GreedyGoto'
        self._radType = 0

        # Initialize Variables for Waypoint Assignment
        self._subswarm_id = 0
        self._id_in_subswarm = []
        self._first_tick = True
        self._subswarm_num_to_assign = []
        self._subswarm_wp_assignment = dict()
        self._wp_assigned = []
        for i in range(0, len(self._enumList)):
            self._wp_assigned.append(False)

        # Initialize Variables for Sequencing between Waypoints
        self._wp_id_list = []   # List of WPs to be assigned to this UAS
        for i in range(0, len(self._enumList)):
            self._wp_id_list.append(i)  # Place holder for other logic
        self._wp_id_list_id = 0     # Index within assigned list of WPs
        self._loc = self._wp_id_list[self._wp_id_list_id]
        self._desired_lat = float(self._enumList[self._loc][0])
        self._desired_lon = float(self._enumList[self._loc][1])
        self._desired_alt = self._last_ap_wp[2]
        self._original_alt = SAFE_ALT
        self._time_at_wp = 0
        self._time_start = 0
        self._at_wp = False
        self._base_alt = int(params['Base Altitude']) 
        self._alt_change = int(params['Altitude Change']) 

        self._altitude = 0.0
        self._radiation = 0.0
        topic='/autopilot/acs_pose'
        outstring = "THIS IS MODIFIED TO FIND error logs"
        print >>sys.stderr, "TESTINGTESTING1 "+ outstring
        rospy.Subscriber('/tactic_interface/altitude', PointStamped, self.altitude_cb)
        rospy.Subscriber('/tactic_interface/radiation', PointStamped, self.radeye_cb)

    def radeye_cb(self, msg):
    	self._radiation = msg.point.x
        self._radType = msg.point.y

    # Sends data to .ros/logs on odroid
    def altitude_cb(self, msg):
        self._altitude = msg.point.x
        self._parent.log_info("The altitude is: %f" %msg.point.x)


    def step_autonomy(self, t, dt):
        # Execute this portion of the code on the loop only
        if self._first_tick == True:
            raddir = self.radeyeDir + 'radeye.py'
            subprocess.Popen(["python", raddir]) # Runs Radeye in the background

            self._first_tick = False
            finishedset = set([])
            #create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #serverflag = 0
            if (SERVER_FLAG == 1):
              server_address = ('192.168.11.202',10000)
            else: 
              server_address = ('127.0.0.1',10000)

            print >>sys.stderr, '---connecting to %s port %s---' % server_address
            sock.connect(server_address)
            try:
                # Initialize data sent to server
                messageArray = [self._id, 100000, 100000, 99999, 100000, self._desired_lat, self._desired_lon, 0, self._desired_alt, "PRDER", 100000, 0, 0] #too long of a list
                message = str(messageArray)
                sock.sendall(message)

                # Look for response from server
                num_symbols = 4096
                delta = 4096
                while delta == num_symbols:
                    data = sock.recv(num_symbols)
                    delta = len(data)
                    print >>sys.stderr,'Received: %s' % data
                temp_finishedset = eval(data)
                finishedset = eval(temp_finishedset[0])
                print "temp finishedset: ", temp_finishedset
                self._enumList = hotspot_grid.createGrid(float(temp_finishedset[1]),float(temp_finishedset[2]))
                print("length of hotspot grid list: ",len(self._enumList))
            finally:
                print >>sys.stderr, '---closing socket---'
                sock.close()


            # Set initial altitude settings
            self._desired_alt = self._last_ap_wp[2]
            self._original_alt = self._last_ap_wp[2]

            # Determine your own subswarm ID
               #key     #value
            for blue_id, blue in self._blues.iteritems():
                if blue.vehicle_id == self._id:
                    self._subswarm_id = blue.subswarm_id
                    break
            print "subswarm_id: ", self._subswarm_id

            # Build a list of all vehicle IDs within your subswarm
            blue_in_subswarm = dict()
            i = 0
            for blue_id, blue in self._blues.iteritems():
                if blue.subswarm_id == self._subswarm_id:
                    self._id_in_subswarm.append(blue.vehicle_id)
                    self._subswarm_num_to_assign.append(0)
                    blue_in_subswarm[i] = blue
                    i = i+1
            print "id_in_subswarm: ", self._id_in_subswarm
            print(self._vehicle_type)

            for n in finishedset:
              self._wp_assigned[n] = True

            # Divide # of waypoints by # of vehicles and create empty bundle of wpts for each
            num_in_subwarm = len(self._id_in_subswarm)
            for i in range(num_in_subwarm):
                self._subswarm_num_to_assign[i] = (len(self._enumList)-len(finishedset))/(num_in_subwarm)
                if i < ((len(self._enumList)-len(finishedset)) % num_in_subwarm):
                    self._subswarm_num_to_assign[i] = self._subswarm_num_to_assign[i] + 1
            print "num_to_assign: ", self._subswarm_num_to_assign


            # Perform sequencial greedy wpt assignment.  Loop over each UAS in subswarm.
            for i in range(num_in_subwarm):
                # Set the start location to current UAS position
                temp_lat = blue_in_subswarm[i].state.pose.pose.position.lat
                temp_lon = blue_in_subswarm[i].state.pose.pose.position.lon
                assignment_list = []
                # Loop over each element of the waypoint bundle
                for j in range(self._subswarm_num_to_assign[i]):
                    min_dist = 99999 #initialize as large number
                    new_wp_assigned = False
                    # Loop over each waypoint defined in the mission
                    for k in range(0, len(self._enumList)):
                        # Skip to next if that waypoint is already assigned
                        if self._wp_assigned[k] == False : #you could use not instead of ==
                            # Set the end location to that waypoint
                            temp2_lat = float(self._enumList[k][0])
                            temp2_lon = float(self._enumList[k][1])
                            # Check if start to end location distance is new minimum, if so mark
                            # if for assignment
                            temp_dist = gps.gps_distance(temp_lat, temp_lon, temp2_lat, temp2_lon)
                            if temp_dist < min_dist:
                                min_dist = temp_dist
                                wp_to_assign = k
                                new_wp_assigned = True
                    # Add the next closest waypoint to the bundle
                    if new_wp_assigned == True:
                        assignment_list.append(wp_to_assign)
                        self._subswarm_wp_assignment[i] = assignment_list
                        # Mark that waypoint as "assigned" so unavailable to others
                        self._wp_assigned[wp_to_assign] = True
                        # Update the start location to that waypoint
                        temp_lat = float(self._enumList[wp_to_assign][0])
                        temp_lon = float(self._enumList[wp_to_assign][1])
                # Assign yourself your own bundle of waypoints
                if blue_in_subswarm[i].vehicle_id == self._id:
                    self._wp_id_list = self._subswarm_wp_assignment[i]
            print "subswarm_wp_assignment: ", self._subswarm_wp_assignment
            # Proceed to the first Waypoint in the bundle
            self._loc = self._wp_id_list[0]
            self._desired_lat = float(self._enumList[self._loc][0])
            self._desired_lon = float(self._enumList[self._loc][1])
            print "Going to WP: ", self._loc


        self._parent.log_info("The altitude global is: %f and radiation is: %f" %(self._altitude,self._radiation))
        # Go to desired latitude, longitude, and maintain altitude
        # deconfliction:
        self._wp = np.array([self._desired_lat, self._desired_lon,
                             self._desired_alt])

        pos = self._own_pose.pose.pose.position
        dist = gps.gps_distance(pos.lat, pos.lon, self._desired_lat, self._desired_lon)

        # Detect whether UAS has arrived at WP (within threshold distance), track time at WP
        # Set threshold distance for Quads (type 1), much smaller

        SURVEY_ALT = self._base_alt + (self._alt_change * self._id_in_subswarm.index(self._id)) 

        if (self._vehicle_type == 1 and dist < DIST2WP_QUAD):
            if self._at_wp == False:
                if (pos.rel_alt > SURVEY_ALT - BUFFER) and (pos.rel_alt < SURVEY_ALT + BUFFER):
                    self._time_start = timeit.default_timer()
            self._at_wp = True
            self._time_at_wp = timeit.default_timer() - self._time_start
        else:
            self._at_wp = False
            self._time_at_wp = 0

        # Detect if Quad is close enough to first WP to descend to survey altitude
        if self._vehicle_type == 1 and dist < DIST_START_DESCENT:
            self._desired_alt = SURVEY_ALT

        # After X time has elapsed at WP, move onto next WP in your bundle
        if self._time_at_wp > TIME_AT_WP:


            lat = pos.lat
            lon = pos.lon
            alt = pos.alt
            if (self._radType == 1): radtype = "PRDER"
            else: radtype = "GN+"

            #create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if (SERVER_FLAG == 1):
              server_address = ('192.168.11.202',10000)
            else: 
              server_address = ('127.0.0.1',10000)
            print >>sys.stderr, '---connecting to %s port %s---' % server_address
            sock.connect(server_address)
            try:

                messageArray = [self._id, len(self._wp_id_list), self._loc, self._wp_id_list.index(self._loc), len(self._enumList), lat, lon, self._radiation, self._altitude, radtype, 0, 0, alt]
                message = str(messageArray)
                print("UAV ID: " + str(self._id))
                print("Sending Message to Base Station...")
                sock.sendall(message)

                #look for response 4194304
                amount_received = 0
                num_symbols = 4096
                delta = 4096
                while delta == num_symbols:
                    data = sock.recv(num_symbols)
                    delta = len(data)

            finally:
                print >>sys.stderr, '---closing socket---'
                sock.close()
            self._wp_id_list_id = self._wp_id_list_id + 1

            # If you get to the end of your bundle, repeat from its beginning
            # and reset to original altitude
            if self._wp_id_list_id > (len(self._wp_id_list)-1):
                self._wp_id_list_id = 0
                self._desired_alt = self._original_alt
            self._loc = self._wp_id_list[self._wp_id_list_id]
            self._desired_lat = float(self._enumList[self._loc][0])
            self._desired_lon = float(self._enumList[self._loc][1])
            # Reset these so that UAV knows it's no longer at its goal WP
            self._at_wp = False
            self._time_at_wp = 0
            print "Going to WP: ", self._loc

        return True
