'''#!/usr/bin/env python

# Implements a proportional navigation control law to guide the UAV
# to an intercept of another UAV.
#
# Duane Davis 2016
'''

# ROS imports
#import rospy
#import std_msgs.msg as stdmsg

# ACS imports
import ap_msgs.msg as apmsg
import autopilot_bridge.msg as brgmsg
import ap_lib.ap_enumerations as enums
import ap_lib.bitmapped_bytes as bytes
import ap_lib.quaternion_math as quat
import ap_lib.gps_utils as gps
#from ap_lib.behavior import *
#from ap_lib.waypoint_behavior import *
import ap_lib.sasc_scrimmage as ss

# Standard Python imports
import math
import numpy


GEO_ORIGIN = ( 35.722267, -120.765808 )

# A few utility functions for dealing with angles

def angle_between(angle, min_angle, max_angle):
    ''' Returns True if min_angle <= angle <= max_angle
    on a normalized range of [0, 2pi)
    '''
    span = gps.normalize(max_angle - min_angle)
    to_test_angle = gps.normalize(angle - min_angle)
    return to_test_angle < span


class USMAInterceptor(ss.Tactic):
    ''' Implements a proportional navigation (PN) control law to guide the
    UAV to intercept another UAV.  The algorithm is currently implemented to
    intercept a specific UAV from the same subswarm as the controlled UAV
    (ID specified in the SwarmBehavior message) for now to facilitate
    implementation.  For now, the interceptor does not actually "shoot"
    at the target, it just maneuvers to intercept from behind.

    TODO: Choose the target from the "red" swarm instead of the UAV's swarm
    TODO: Implement a selection algorithm to choose the target
    TODO: Implement state 6 (reset if the gain is too high in state 5)

    Class-specific member variables:
      _target_id: ID of the UAV that is to be intercepted
      _state: setup, run-in, offset, parallel, intercept, or endgame
      _state_initialized: set to False if the next state has an init step
      _VT_turn_type: type of turn to use to reach the virtual target
      _s_turn_state: states associated with the S-turn to the virtual target
      _t: current time
      _dt: time between execution steps
      _xp: pursuer state (latitude, longitude, heading)
      _vp: pursuer velocity (x_dot, y_dot, psi_dot)
      _xt = target state (latitude, longitude, heading)
      _vt = target velocity (x_dot, y_dot, psi_dot)
      _range: range (m) to the target UAV (or virtual target in offset phase)
      _psi_p3: saved psi used in the s-turn calculation
      _theta: angle (rad) to the target UAV (or virtual target in offset phase)
      _theta2: saved theta value used in the s-turn calculation
      _theta3: computed theta value used in the s-turn calculation
      _theta_dot: rate of change of the theta angle
      _theta_dot_last: previous rate of change of the theta angle
      _s2_check: theta sign-change check for s-turn state turn
      _VT: virtual target position (track to point other than target UAV)
      _theta_VT_init: angle to the virtual target at start of tracking
      _theta_dot_VT_init: anglular rate to the virtual target at start of tracking
      _psi_p_VT_init: pursuer heading at start of tracking the virtual target
      _psi_p_f: targeted pursuer heading at engagement or virtual target
      _gain: N value for use in the PN equation
      _bias: B value for use in the PN equation
      _E: approximated control energy integral
      _E_trend: buffer for last ten E values

    Inherited from WaypointBehavior
      _wpPublisher: publisher object for publishing waypoint commands
      wp_msg: LLA object containing waypoint order
      _last_wp_id: Index (ID) of the last (infinite loiter) waypoint

    Inherited from Behavior
      behaviorID: identifier (int) for this particular behavior
      _subswarm_id: ID of the subswarm to which this UAV is assigned
      _swarm: container for state info for all swarm UAVs
      _swarm_keys: key values (IDs) of all swarm UAVs
      _subswarm_keys: key values (IDs) of all subswarm UAVs
      _ap_intent: most recently ordered autopilot waypoint
      _lock: reentrant lock to enforce thread-safe swarm dictionary access
      is_ready: set to True when the behavior has been initialized
      is_active: set to True when the behavior is running 
      is_paused: set to True when an active behavior is paused
      _activate_time: ROS time that the behavior was activated
      _uses_wp_control: set to True if the behavior drives by waypoint
      _statusPublisher: publisher object for behavior status
      _behaviorDataPublisher: publisher object for behavior data (network) msgs
      _statusStamp: timestamp of the last status message publication
      _sequence: sequence number of the next status message

    Inherited from Nodeable:
      nodeName:  Name of the node to start or node in which the object is
      timer: ROS rate object that controls the timing loop
      DBUG_PRINT: set true to force screen debug messages (default FALSE)
      INFO_PRINT: set true to force screen info messages (default FALSE)
      WARN_PRINT: set false to force screen warning messages (default FALSE)

    Class member functions:
      set_behavior: sets behavior-specific parameters before execution
      run_behavior: implementation of the Behavior virtual function
      set_pause: implementation of the Behavior virtual function
      pause_behavior: overrides the Behavior class method
      _safety_checks: implementation of the Behavior virtual function
      _setup_state: controls the UAV to set up for the intercept
      _runin_state: drives straight towards the target until the offset point
      _offset_state: controls the offset maneuver
      _parallel_state: drives the vehicle parallel to the target before turn-in
      _intercept_state: controls the vehicle during the turn-in maneuver
      _endgame_state: controls the final intercept (taking the shot)
      _calculate_E: calculates the approximated control energy integral (TODO)
      _send_ctrl_wp: runs the PN equation and sends the computed waypoint
    '''

    # Behavior state value enumeration)
    RUN_IN = 0
    OFFSET = 1
    PARALLEL_1 = 2
    PARALLEL_2 = 3
    INTERCEPT = 4
    ENDGAME = 5

    # Types of turns to reach the virtual waypoint
    DIRECT_TURN = 1
    DIRECT_2BIAS = 2
    S_TURN = 3

    # S-Turn states
    S1 = 1
    S2 = 2
    S3 = 3    

    MANEUVER_STATES = { RUN_IN, OFFSET, INTERCEPT, ENDGAME }

    # TODO:  Need values for these
    FIRE_ANGLE = 0.0  # Forward angle to fire from
    R_RUNIN =  2000.0 # Range in front of the target to set up for runin
    R_TH1 = 1400.0    # Range at which to transition from RUN_IN to OFFSET
    R_TH2 = 400.0     # Range at which to transition from OFFSET to PARALLEL
    D1 = 200.0        # Desired separation between target track and pursuer parallel track
    D2 = 1000.0       # Desired distance of VT from target along psi_t
    R_FINAL = 2.0     # Desired distance behind the target
    R_CAP_PARALLEL = 25.0 # Distance from virtual target to shift to parallel
    A_P_MAX = 4.8     # Maximum lateral acceleration of the pursuer
    A_T_MAX = 4.8     # Maximum lateral acceleration of the target

    def init(self, params):
        self._id = int(params['id'])
        #def __init__(self, nodename):
        ''' Class initializer initializes class variables.
        @param nodename: name of the ROS node in which this object exists
        '''
        #WaypointBehavior.__init__(self, nodename, enums.PN_INTERCEPTOR)
        #self._own_uav_id = rospy.get_param("aircraft_id")
        self._target_id = 0
        self._state = USMAInterceptor.RUN_IN
        self._state_initialized = False
        self._t = None
        self._dt = 0.0
        self._xp = (0.0, 0.0, 0.0)
        self._vp = (0.0, 0.0, 0.0)
        self._xt = (0.0, 0.0, 0.0)
        self._vt = (0.0, 0.0, 0.0)
        self._range = 0.0
        self._psi_p3 = 0.0
        self._theta = 0.0
        self._theta2 = 0.0
        self._theta3 = 0.0
        self._theta_dot = 0.0
        self._theta_dot_last = 0.0
        self._VT = (0.0, 0.0)
        self._theta_VT_init = 0.0
        self._theta_dot_VT_init = 0.0
        self._psi_p_VT_init = 0.0
        self._VT_turn_type = USMAInterceptor.DIRECT_TURN
        self._s_turn_state = USMAInterceptor.S1
        self._psi_p_f = 0.0
        self._gain = 0.0
        self._bias = 0.0
        self._E = 1e9
        self._E_trend = [1e9] * 10
        self._bias_initialized = False # to facilitate a log entry
        self._swarm = dict()
        self._blues = dict()
        self._reds = dict()
        self._shot = set()
        self._own_pose = brgmsg.Geodometry()
        self._wp = numpy.array([0, 0, 0])
        # CUT HERE
#        self._outfile = None
#        self._fileNum = 1
        # TO HERE
#        self.DBUG_PRINT = True
#        self.INFO_PRINT = True
#        self.WARN_PRINT = True


    #-------------------------------------------------
    # Implementation of parent class virtual functions
    #-------------------------------------------------

    '''def set_behavior(self, params):
        Sets behavior parameters based on set service parameters
        The params parameter is parsed with a customized ap_lib.BitmappedBytes
        object that is specific to the behavior being implemented.
        @param params: byte array from the set service request
        @return True if set with valid parameters
        
        self.subscribe_to_swarm()
        parser = bytes.UShortParser()
        parser.unpack(params)
        self._target_id = parser.value
        self._state = PNInterceptor.RUN_IN
        self._state_initialized = False
        self._t = rospy.Time.now()
        self._E = 1e9
        self._E_trend = [1e9] * 10
        self._psi_p3 = 0.0
        self._theta2 = 0.0
        self._theta3 = 0.0
        self.wp_msg.alt = self._ap_intent.z
        self._bias_initialized = False # to facilitate a log entry
        self.set_ready_state(True)
        self.log_dbug("PN intercept target ID set to %d" %self._target_id)
        # CUT HERE
#        self._outfile = open('/home/dtdavi1/Desktop/outfile%d.csv'%self._fileNum,'w')
#        self._outfile.write('x_p,\ty_p,\tpsi_p,\txdot_p,\tydot_p,\tx_t,\ty_t,\tpsi_t,\txdot_t,\tydot_t,\tx_vt,\ty_vt,\tpsi_p_0,\tpsi_p_f,\ttheta,\ttheta_dot,\ttheta_vt_0,\ttheta_2,\ttheta_3\n')
#        self._fileNum += 1
        # TO HERE
        return self.is_ready


    # CUT HERE
    '''
#    def set_active(self, activate):
#        ''' Used to activate and deactivate the behavior
#        Will not activate an "unready" behavior or one that is already active
#        @param activate: Boolean value to activate or deactivate the behavior
#        @return active status upon method completion
#        '''
#        if activate and not self.is_ready:
#            self.is_active = False
#            self.log_warn("attempt to activate uninitialized behavior %s"\
#                          %self.nodeName)
#        elif activate and not self.is_active:
#            self.is_active = activate
#            self.log_info("activating behavior %s"%self.nodeName)
#            self._send_status_message()
#        elif not activate and self.is_active:
#            self.log_info("deactivating behavior %s"%self.nodeName)
#            self.set_ready_state(False)
#            self._send_status_message()
#            self._outfile.close()
#        return self.is_active
    # TO HERE


    '''def _safety_checks(self):
        Conducts behavior-specific safety checks
        This method is called automatically every iteration prior to calling
        the _run_behavior method.
        @return True if the behavior passes all safety checks (False otherwise)
        
        if self._target_id not in self._swarm_keys:
            self.log_warn("PN intercept target (%d) not present in swarm"\
                           %self._target_id)
            return False

        if self._target_id == self._own_uav_id:
            self.log_warn("PN intercept target (%d) set to own ID"\
                           %self._target_id)
            return False

        return True  # If it gets here, all safety checks have passed
    '''

    def step_autonomy(self, t, dt):
        #def run_behavior(self):
        ''' Executes one iteration of the behavior
        '''
        # Save last values so we can numerically differentiate the rates
        last_t = self._t
        self._t = t    #rospy.Time.now()
        self._dt = dt    #(float(self._t.secs) + float(self._t.nsecs) / float(1e9)) - \
                         #(float(last_t.secs) + float(last_t.nsecs) / float(1e9))
        (xp_last, vp_last) = (self._xp, self._vp)
        (xt_last, vt_last) = (self._xt, self._vt)

        min_dist = numpy.inf
        for uav in self._reds.values():
            if uav.vehicle_id not in self._shot:
                d = gps.gps_distance(self._own_pose.pose.pose.position.lat,\
                                     self._own_pose.pose.pose.position.lon,\
                                     uav.state.pose.pose.position.lat,\
                                     uav.state.pose.pose.position.lon)

                if d < min_dist:
                    min_dist = d
                    self._target_id = uav.vehicle_id

        # Obtain/compute pursuer position, velocity, and acceleration
        #record_p = self._id    # self._swarm[self.own_uav_id]
        q = self._own_pose.pose.pose.orientation
        _, _, psi_p = quat.quat_to_euler([ q.x, q.y, q.z, q.w ])
        self._xp = ( self._own_pose.pose.pose.position.lat, \
                     self._own_pose.pose.pose.position.lon, \
                     math.atan2(self._vp[1], self._vp[0]) )
        self._vp = ( self._own_pose.twist.twist.linear.x, \
                     self._own_pose.twist.twist.linear.y, \
                     ((self._xp[2] - xp_last[2]) / self._dt) )

        # Obtain/compute target position, velocity, and acceleration
        record_t = self._reds[self._target_id]  # self._swarm[self._target_id]
        self._vt = ( record_t.state.twist.twist.linear.x, \
                     record_t.state.twist.twist.linear.y, \
                     ((self._xt[2] - xt_last[2]) / self._dt) )
        self._xt = ( record_t.state.pose.pose.position.lat, \
                     record_t.state.pose.pose.position.lon, \
                     math.atan2(self._vt[1], self._vt[0]) )

        if self._state == USMAInterceptor.RUN_IN:
            self._runin_state()

        elif self._state == USMAInterceptor.OFFSET:
            self._offset_state()

        elif self._state == USMAInterceptor.PARALLEL_1:
            self._parallel_1_state()

        elif self._state == USMAInterceptor.PARALLEL_2:
            self._parallel_2_state()

        elif self._state == USMAInterceptor.INTERCEPT:
            self._intercept_state()

        elif self._state == USMAInterceptor.ENDGAME:
            self._endgame_state()

        if self._state in USMAInterceptor.MANEUVER_STATES:
            self._send_ctrl_wp()


    '''def set_pause(self, pause):
        Pauses and unpauses the behavior
        Overrides the Behavior class method (which is called from this method)
        @param pause: Boolean determining whether to pause or resume
        @return: the post-execution paused state of the behavior
        
        if not self.is_active: return
        if pause:
            self.wp_msg.lat = \
                self._swarm[self._own_uav_id].state.pose.pose.position.lat
            self.wp_msg.lon = \
                self._swarm[self._own_uav_id].state.pose.pose.position.lon
            self.wp_msg.alt = \
                self._ap_intent.z
            self.publishWaypoint(self.wp_msg)
        return super(PNInterceptor, self).set_pause(pause)
    '''

    #-------------------------------------------------------------
    # Behavior-specific methods
    # Including subscription callbacks and service implementations
    #-------------------------------------------------------------

    def _runin_state(self):
        ''' Performs calculations and operations required for the "runin" state
        '''
        if not self._state_initialized:
            self.log_info("Commence run-in phase")
            self._gain = 2.5
            self._state_initialized = True

        # Compute the control parameters & set a bias value if rqd
        # to force the pursuer towards the target
        self._set_ctrl_params(self._xp, self._vp, self._xt, self._vt)
        theta_diff = gps.normalize_pi(self._theta - self._xp[2])
        self._bias = gps.signum(theta_diff) * \
                     min(2.5, math.fabs(theta_diff) / 10.0)

        # Keep going until the offset range is reached
        if self._range <= USMAInterceptor.R_TH1:
            self._state_initialized = False
            self._state = USMAInterceptor.OFFSET
            self.log_info("Transition to offset phase")


    def _offset_state(self):
        ''' Performs calculations and operations required for the "offset" state
        '''
        if not self._state_initialized:
            # Set the virtual waypoint D2 meters along the target's path and
            # offset by D1 meters to the side that the pursuer is currently on
            theta = gps.gps_bearing(self._xp[0], self._xp[1], \
                                     self._xt[0], self._xt[1])
            offset_dir = \
                gps.signum(gps.normalize_pi(theta + math.pi - self._xt[2]))
            tgt_to_VT = self._xt[2] + math.atan2(USMAInterceptor.D1 * offset_dir, \
                                                 USMAInterceptor.D2)
            self._VT = \
                gps.gps_newpos(self._xt[0], self._xt[1], tgt_to_VT, \
                               math.hypot(USMAInterceptor.D1, USMAInterceptor.D2))
            self._set_ctrl_params(self._xp, self._vp, \
                                  (self._VT[0], self._VT[1], self._xt[2]), \
                                  (0.0, 0.0))
            self._theta_VT_init = self._theta
            self._theta_dot_VT_init = self._theta_dot
            self._psi_p_VT_init = self._xp[2]
            self._psi_p_f = gps.normalize(self._xt[2] + math.pi)
            psi_p_f_rel = gps.normalize(self._psi_p_f - self._theta_VT_init)
            if gps.normalize_pi(self._theta_VT_init - self._psi_p_VT_init) > 0.0:
                psi_p_f_rel = gps.normalize(-psi_p_f_rel)
            if angle_between(psi_p_f_rel, 0.0, math.pi):
                self._VT_turn_type = USMAInterceptor.S_TURN
                self._s_turn_state = USMAInterceptor.S1
            elif angle_between(psi_p_f_rel, (self._theta_VT_init - \
                                             self._psi_p_VT_init), 0.0):
                self._VT_turn_type = USMAInterceptor.DIRECT_TURN
            else:
                self._VT_turn_type = USMAInterceptor.DIRECT_2BIAS
            self._state_initialized = True

        self._set_ctrl_params(self._xp, self._vp, \
                              (self._VT[0], self._VT[1], 0.0), (0.0, 0.0))

        if self._range < USMAInterceptor.R_CAP_PARALLEL:
            self._state_initialized = False
            self._state = USMAInterceptor.PARALLEL_1
            self.log_info("Transition to parallel_1 phase")

        # Determine how to maneuver to the virtual target point
        # Direct turn to the virtual target
        if self._VT_turn_type == USMAInterceptor.DIRECT_TURN:
            self._gain = math.fabs((gps.normalize_pi(self._psi_p_f - \
                                                     self._psi_p_VT_init)) / \
                                   (gps.normalize_pi(self._psi_p_f - \
                                                     self._theta_VT_init)))
            self._bias = 0.0

        # Single turn to virtual target with 2 gains
        elif self._VT_turn_type == USMAInterceptor.DIRECT_2BIAS:
            if math.fabs(gps.normalize_pi(self._psi_p_f - self._xp[2]) / \
                         gps.normalize_pi(self._psi_p_f - self._theta)) < 2.0:
                self._gain = gps.normalize_pi(self._psi_p_VT_init) / \
                             gps.normalize_pi(math.pi/2 + self._theta_VT_init)
                self._bias = 0.0
            else:
                self._gain = 2.0
                self._bias = 0.0


        # S-turn to virtual target
        else:
            self._s_turn()

        # CUT HERE
#        record_t = self._swarm[self._target_id]
#        record_p = self._swarm[self._own_uav_id]
#        xp = gps.cartesian_offset(GEO_ORIGIN[0], GEO_ORIGIN[1], self._xp[0], self._xp[1])
#        xt = gps.cartesian_offset(GEO_ORIGIN[0], GEO_ORIGIN[1], self._xt[0], self._xt[1])
#        vt = gps.cartesian_offset(GEO_ORIGIN[0], GEO_ORIGIN[1], self._VT[0], self._VT[1])
#        xp_dot = (record_p.state.twist.twist.linear.x, record_p.state.twist.twist.linear.y)
#        xt_dot = (record_t.state.twist.twist.linear.x, record_t.state.twist.twist.linear.y)
#        self._outfile.write("%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f,\t%f\n" \
#                            %(xp[0], xp[1], self._xp[2], xp_dot[0], xp_dot[1], \
#                              xt[0], xt[1], self._xt[2], xt_dot[0], xt_dot[1], \
#                              vt[0], vt[1], self._psi_p_VT_init, self._psi_p_f, \
#                              self._theta, self._theta_dot, self._theta_VT_init, \
#                              self._theta2, self._theta3))
        # TO HERE

    def _s_turn(self):
        ''' Calculations associated with the S-turn to the virtual target
        '''
        if self._s_turn_state == self.S1:    # Offset turn
            self._gain = 2.0
            self._bias = 0.5 * gps.signum(self._theta_dot)
            if math.fabs(gps.signum(self._theta_dot) - \
                         gps.signum(self._theta_dot_last)) == 2:
                self._s_turn_state = self.S2
                self._theta2 = self._theta
                self._theta3 = self._theta2 + 0.75 * (self._theta_VT_init - self._theta2)
                self._theta3 = gps.normalize(self._theta3)
                self._s2_check = \
                    gps.signum(gps.normalize_pi(self._theta - self._theta3))
                self.log_info("Shift to S-turn phase S2:\tTheta=%f\tTheta3=%f\tTheta_dot=%f"\
                              %(self._theta, self._theta3, self._theta_dot))

        if self._s_turn_state == self.S2:   # Middle portion of the S
            self._bias = -0.25 * gps.signum(self._theta_dot)
            self._gain = -2.0
            if self._s2_check != \
               gps.signum(gps.normalize_pi(self._theta - self._theta3)):
                self._s_turn_state = self.S3
                self._theta3 = self._theta
                self._psi_p3 = self._xp[2]
                self.log_info("Shift to S-turn phase S3")
                self._bias_initialized = False # to facilitate a log entry

        if self._s_turn_state == self.S3:   # Final turn to VT
            if (self._theta_dot_VT_init < 0.0 and \
                angle_between(self._psi_p_f, self._theta_VT_init, \
                              2.0 * self._theta3 - self._psi_p3)) or \
               (self._theta_dot_VT_init >= 0.0 and \
                angle_between(self._psi_p_f, \
                              2.0 * self._theta3 - self._psi_p3, \
                              self._theta_VT_init)):
                self._gain = math.fabs((gps.normalize_pi(self._psi_p_f - self._psi_p3)) / \
                                       (gps.normalize_pi(self._psi_p_f - self._theta3)))
                self._bias = 0.0
                if not self._bias_initialized:
                    self._bias_initialized = True
                    self.log_info("Phase S3 using 1-bias turn")

            else:
                if math.fabs(gps.normalize_pi(self._psi_p_f - self._xp[2]) / \
                             gps.normalize_pi(self._psi_p_f - self._theta)) < 2.0:
                    self._gain = gps.normalize_pi(self._psi_p3) / \
                                 gps.normalize_pi(math.pi/2.0 + self._theta3)
                    self._bias = 0.0
                else:
                    self._gain = 2.0
                    self._bias = 0.0
                if not self._bias_initialized:
                    self._bias_initialized = True
                    self.log_info("Phase S3 using 2-bias turn")


    def _parallel_1_state(self):
        ''' Performs calculations and operations required for the "parallel 1" state
        '''
        if not self._state_initialized:
            bearing = gps.normalize(self._xt[2] - math.pi)
            self.wp_msg.lat, self.wp_msg.lon = \
                gps.gps_newpos(self._xp[0], self._xp[1], bearing, 10000.0)
            self.publishWaypoint(self.wp_msg)
            self._state_initialized = True
        self._set_ctrl_params(self._xp, self._vp, self._xt, self._vt)

        if self._range <= USMAInterceptor.R_TH2:
            self._state = USMAInterceptor.PARALLEL_2
            self._gain = 0.0
            self._bias = 0.0
            self._state_initialized = False
            self.log_info("Transition to parallel_2 state")


    def _parallel_2_state(self):
        ''' Performs calculations and operations required for the "parallel 2" state
        '''
        if not self._state_initialized:
            self._psi_p_f = gps.normalize(self._xt[2] - USMAInterceptor.FIRE_ANGLE)
            self._bias = 0.0
            self._state_initialized = True
        self._set_ctrl_params(self._xp, self._vp, self._xt, self._vt)
        self._gain = math.fabs(gps.normalize_pi(self._psi_p_f - self._xp[2]) / \
                               gps.normalize_pi(self._psi_p_f - self._theta))
        self._E = self._calculate_E()
        if self._E > min(numpy.mean(self._E_trend), \
                         numpy.median(self._E_trend)):  # reached minimum
            self._state_initialized = False
            self._state = USMAInterceptor.INTERCEPT
            self.log_info("Transition to intercept phase")
        self._E_trend = self._E_trend[1:] + [ self._E ]


    def _intercept_state(self):
        ''' Performs calculations and operations required for the "intercept" state
        '''
        self._set_ctrl_params(self._xp, self._vp, self._xt, self._vt)

    def _engame_state(self):
        ''' Performs calculations and operations required for the "offset" state
        '''
        self._set_ctrl_params(self._xp, self._vp, self._xt, self._vt)
        # TODO:  Still need to add all of this


    def _calculate_E(self):
        ''' Calculates the approximated integral of control energy square (E)
        @return calculated value
        '''
        theta_p = gps.normalize(self._xp[2] - self._theta)
        theta_t = gps.normalize(self._xt[2] - self._theta)
        theta_tr = self._theta
        R = self._range
        delta_theta = 0.0025 * gps.signum(self._theta_dot)
        v_p = math.hypot(self._vp[0], self._vp[1])
        v_t = math.hypot(self._vt[0], self._vt[1])
        v_r = v_t * math.cos(theta_t) - v_p * math.cos(theta_p)
        v_theta = v_t * math.sin(theta_t) - v_p * math.sin(theta_p)
        E = 0.0
        while math.cos(delta_theta) > math.cos(self._psi_p_f - theta_tr):
            E = E + math.pow((self._gain * v_p), 2) * \
                                (v_theta / R) * delta_theta
            R = R * math.exp(v_r / v_theta * delta_theta)
            theta_t = theta_t - delta_theta
            theta_p = theta_p + (self._gain - 1) * delta_theta
            v_r = v_t * math.cos(theta_t) - v_p * math.cos(theta_p)
            v_theta = v_t * math.sin(theta_t) - v_p * math.sin(theta_p)
            theta_tr = theta_tr + delta_theta
        return E


    def _set_ctrl_params(self, own_state, own_vel, tgt_state, tgt_vel):
        ''' Sets the control parameter values based on own and target state
            @param own_state:  pursuer vehicle state (lat, lon, psi)
            @param own_vel:  pursuer velocity (x_dot, y_dot)
            @param tgt_state:  target vehicle state (lat, lon, psi)
            @param tgt_vel:  target velocity (x_dot, y_dot)            
        '''
        self._range = gps.gps_distance(own_state[0], own_state[1], \
                                       tgt_state[0], tgt_state[1])
        self._theta = gps.gps_bearing(own_state[0], own_state[1], \
                                      tgt_state[0], tgt_state[1])
        own_spd = math.hypot(own_vel[0], own_vel[1])
        tgt_spd = math.hypot(tgt_vel[0], tgt_vel[1])
        crossing_spd = own_spd * math.sin(self._theta - own_state[2]) + \
                       tgt_spd * math.sin(self._theta + math.pi - tgt_state[2])
        self._theta_dot_last = self._theta_dot
        self._theta_dot = crossing_spd / self._range


    def _send_ctrl_wp(self):
        ''' Uses the computed gain, bias, and theta_dot to compute a waypoint
        '''
        v_p = math.hypot(self._vp[0], self._vp[1])
        a_p = (self._gain * self._theta_dot + self._bias) * v_p
        if math.fabs(a_p) > USMAInterceptor.A_P_MAX:
            a_p = gps.signum(a_p) * USMAInterceptor.A_P_MAX

        L1 = 150.0 #min((v_p * 5.0 * self._dt), self._range)
        nu = 0
        if v_p != 0:
            nu = math.asin((a_p * L1) / (2.0 * math.pow(v_p, 2.0)))
        self.wp_msg = self._own_pose.pose.pose.position
        self.wp_msg.lat, self.wp_msg.lon = \
            gps.gps_newpos(self._xp[0], self._xp[1], nu + self._xp[2], L1)
        self._wp = numpy.array([self.wp_msg.lat, self.wp_msg.lon, self.wp_msg.rel_alt])   # publishWaypoint(self.wp_msg)
                      

#----------------------------------------------------------------------------
# Node initialization block can be included here or placed in a separate file
#----------------------------------------------------------------------------

'''if __name__ == '__main__':
    rospy.init_node("pn_interceptor")
    behavior = PNInterceptor("pn_interceptor")
    behavior.runAsNode(10.0)
'''

