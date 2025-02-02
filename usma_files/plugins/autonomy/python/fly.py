# Performs a sequencial greedy waypoint (WP) assignment: 
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
# Andrew Kopeikin
# USMA
# 27 Jan 2018

import numpy as np
import math
import autopilot_bridge.msg as apbrg
import ap_msgs.msg as apmsg
from autopilot_bridge.msg import LLA
import ap_lib.gps_utils as gps
import ap_lib.ap_enumerations as enums
import ap_lib.sasc_scrimmage as ss
import usma_enumerations as usma_enums
import timeit
import rospy

finishedList = []

class Fly(ss.Tactic):

    #Creates a dictionary of waypoints depending on the Lat/Lon given as the
    #Starting point, Ending Point, Num of Waypoints to be in the dictionary
    #Tuple           Tuple         Int
    global separatePoints
    global finishedList 
    def separatePoints(starting, ending, num_of_points):
        #print(starting)
        #print(ending)
        #print(num_of_points)
        iterable_wp = [starting]
        inc_lon = (ending[0] - starting[0])/(num_of_points-1)
        inc_lat = (ending[1] - starting[1])/(num_of_points-1)
        stored_pt = (starting[0]+inc_lon,starting[1]+inc_lat)
        for i in range(1,num_of_points):
            iterable_wp.append(stored_pt)
            stored_pt = (stored_pt[0]+inc_lon, stored_pt[1]+inc_lat)
        return (iterable_wp)

    def init(self, params):
        self._id = int(params['id'])
        self._file_id = params['id']
        self._target_id = -1
        self._wp = np.array([0, 0, 0])
        self._max_range = enums.MAX_RANGE_DEF
        self._fov_width = enums.HFOV_DEF
        self._fov_height = enums.VFOV_DEF
        self._own_pose = apbrg.Geodometry()
        self._blues = dict()
        #self._reds = dict()
        self._shot = set()
        self._safe_waypoint = np.array([0, 0, 0])
        self._last_ap_wp = np.array([0, 0, 0])
        self._action = ["None", 0]
        self._vehicle_type = int(params['vehicle_type'])
        self._name = 'Fly'
        #self._location = int(params['location'])
        #self._desired_lat = float(usma_enums.WP_LOC[self._location][0])
        #self._desired_lon = float(usma_enums.WP_LOC[self._location][1])

        # Initialize Variables for Waypoint Assignment
        self._subswarm_id = 0
        self._id_in_subswarm = []
        self._first_tick = True
        self._subswarm_num_to_assign = []c
        self._subswarm_wp_assignment = dict()
        self._wp_assigned = []
        for i in range(0, len(usma_enums.WP_LOC)):
            self._wp_assigned.append(False)  

        # Initialize Variables for Sequencing between Waypoints
        self._wp_id_list = []   # List of WPs to be assigned to this UAS
        for i in range(0, len(usma_enums.WP_LOC)):
            self._wp_id_list.append(i)  # Place holder for other logic
        self._wp_id_list_id = 0     # Index within assigned list of WPs
        self._loc = self._wp_id_list[self._wp_id_list_id]
        self._desired_lat = float(usma_enums.WP_LOC[self._loc][0])
        self._desired_lon = float(usma_enums.WP_LOC[self._loc][1])
        self._finished_list = []
        self._time_at_wp = 0
        self._time_start = 0
        self._at_wp = False

        ######## this is the new messaging logic
        self.pubs['wp_tracker'] = \
            self.createPublisher('wp_tracker', apmsg.WPTracker, 1)
        self.subs['wp_tracker'] = \
            self.createSubscriber('wp_tracker', apmsg.WPTracker, \
                                  self.receive_msg_stat)

        msg = apmsg.SwarmSearchWaypointList()
        msg.header = std_msg.msg.Header()
        msg.header.seq = 5
        msg.header.stamp = rospy.Time.now
        msg.header.frame_id = "Peter"

        msg.waypoints = self._finished_list
        self.pubs['wp_tracker'].publish(msg)

        print '{} sending message' \
              .format(self._finished_list)

    def receive_msg_stat(self, msg):
        print 'Received message {}'.format(self._finished_list)

        
        
    def step_autonomy(self, t, dt):
        # Go to desired latitude, longitude, and maintain altitude
        # deconfliction:
        self._wp = np.array([self._desired_lat, self._desired_lon, 
                             self._last_ap_wp[2]])

        pos = self._own_pose.pose.pose.position
        dist = gps.gps_distance(pos.lat, pos.lon, self._desired_lat, self._desired_lon)

        # Execute this portion of the code on the loop only
        if self._first_tick == True:
            self._first_tick = False

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

            # Divide # of waypoints by # of vehicles and create empty bundle of wpts for each 
            num_in_subwarm = len(self._id_in_subswarm)
            for i in range(0, num_in_subwarm):
                self._subswarm_num_to_assign[i] = int(math.floor(len(usma_enums.WP_LOC)/num_in_subwarm))
                if i < (len(usma_enums.WP_LOC) % num_in_subwarm):
                    self._subswarm_num_to_assign[i] = self._subswarm_num_to_assign[i] + 1
            print "num_to_assign: ", self._subswarm_num_to_assign

            # Perform sequencial greedy wpt assignment.  Loop over each UAS in subswarm.
            for i in range(0, num_in_subwarm):
                # Set the start location to current UAS position
                temp_lat = blue_in_subswarm[i].state.pose.pose.position.lat
                temp_lon = blue_in_subswarm[i].state.pose.pose.position.lon
                assignment_list = []
                # Loop over each element of the waypoint bundle 
                for j in range(0, self._subswarm_num_to_assign[i]):
                    min_dist = 99999 #initialize as large number
                    new_wp_assigned = False
                    # Loop over each waypoint defined in the mission  
                    for k in range(0, len(usma_enums.WP_LOC)):
                        # Skip to next if that waypoint is already assigned
                        if self._wp_assigned[k] == False:
                            # Set the end location to that waypoint
                            temp2_lat = float(usma_enums.WP_LOC[k][0])
                            temp2_lon = float(usma_enums.WP_LOC[k][1])
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
                        temp_lat = float(usma_enums.WP_LOC[wp_to_assign][0])
                        temp_lon = float(usma_enums.WP_LOC[wp_to_assign][1])
                # Assign yourself your own bundle of waypoints
                if blue_in_subswarm[i].vehicle_id == self._id:
                    self._wp_id_list = self._subswarm_wp_assignment[i]
            print "subswarm_wp_assignment: ", self._subswarm_wp_assignment
            # Proceed to the first Waypoint in the bundle
            self._loc = self._wp_id_list[0]
            self._desired_lat = float(usma_enums.WP_LOC[self._loc][0])
            self._desired_lon = float(usma_enums.WP_LOC[self._loc][1]) 
            print "Going to wp1: ", self._loc
            print "Finished list: ", self._finished_list
            finishedList = self._finished_list # ADDED BY PENG PONG

        # Detect whether UAS has arrived at WP (within threshold distance), track time at WP
        # Zephyrs (type 2) loiter around point, so set threshold distance > loiter radius
        # Set threshold distance for Quads (type 1), much smaller
        if (self._vehicle_type == 2 and dist < 75) or (self._vehicle_type == 1 and dist < 10):
            if self._at_wp == False:
                self._time_start = timeit.default_timer()
            self._at_wp = True
            self._time_at_wp = timeit.default_timer() - self._time_start
        else:
            self._at_wp = False
            self._time_at_wp = 0
        
        # After X time has elapsed at WP, move onto next WP in your bundle
        if self._time_at_wp > 10:
            self._finished_list.append([1,2,3])
            receive_msg_stat(self, self.msg)
            self._wp_id_list_id = self._wp_id_list_id + 1
            # If you get to the end of your bundle, repeat from its beginning
            if self._wp_id_list_id > (len(self._wp_id_list)-1): 
                self._wp_id_list_id = 0
            self._loc = self._wp_id_list[self._wp_id_list_id]
            self._desired_lat = float(usma_enums.WP_LOC[self._loc][0])
            self._desired_lon = float(usma_enums.WP_LOC[self._loc][1]) 
            # Reset these so that UAV knows it's no longer at its goal WP
            self._at_wp = False
            self._time_at_wp = 0
        
        return True

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
