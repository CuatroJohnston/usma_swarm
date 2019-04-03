/* Software License Agreement (BSD License)
 *
 * Copyright (c) 2011, Willow Garage, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above
 *    copyright notice, this list of conditions and the following
 *    disclaimer in the documentation and/or other materials provided
 *    with the distribution.
 *  * Neither the name of Willow Garage, Inc. nor the names of its
 *    contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 * Auto-generated by genmsg_cpp from file /home/odroid/acs_ros_ws/src/autonomy-payload/ap_msgs/msg/SwarmVehicleState.msg
 *
 */


#ifndef AP_MSGS_MESSAGE_SWARMVEHICLESTATE_H
#define AP_MSGS_MESSAGE_SWARMVEHICLESTATE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <autopilot_bridge/Geodometry.h>

namespace ap_msgs
{
template <class ContainerAllocator>
struct SwarmVehicleState_
{
  typedef SwarmVehicleState_<ContainerAllocator> Type;

  SwarmVehicleState_()
    : vehicle_id(0)
    , subswarm_id(0)
    , received_at()
    , swarm_state(0)
    , swarm_behavior(0)
    , vehicle_type(0)
    , state()  {
    }
  SwarmVehicleState_(const ContainerAllocator& _alloc)
    : vehicle_id(0)
    , subswarm_id(0)
    , received_at()
    , swarm_state(0)
    , swarm_behavior(0)
    , vehicle_type(0)
    , state(_alloc)  {
    }



   typedef uint16_t _vehicle_id_type;
  _vehicle_id_type vehicle_id;

   typedef uint16_t _subswarm_id_type;
  _subswarm_id_type subswarm_id;

   typedef ros::Time _received_at_type;
  _received_at_type received_at;

   typedef uint8_t _swarm_state_type;
  _swarm_state_type swarm_state;

   typedef uint8_t _swarm_behavior_type;
  _swarm_behavior_type swarm_behavior;

   typedef uint8_t _vehicle_type_type;
  _vehicle_type_type vehicle_type;

   typedef  ::autopilot_bridge::Geodometry_<ContainerAllocator>  _state_type;
  _state_type state;




  typedef boost::shared_ptr< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> const> ConstPtr;

}; // struct SwarmVehicleState_

typedef ::ap_msgs::SwarmVehicleState_<std::allocator<void> > SwarmVehicleState;

typedef boost::shared_ptr< ::ap_msgs::SwarmVehicleState > SwarmVehicleStatePtr;
typedef boost::shared_ptr< ::ap_msgs::SwarmVehicleState const> SwarmVehicleStateConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ap_msgs::SwarmVehicleState_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace ap_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'nav_msgs': ['/opt/ros/indigo/share/nav_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/indigo/share/sensor_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/indigo/share/actionlib_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/indigo/share/std_msgs/cmake/../msg'], 'ap_msgs': ['/home/odroid/acs_ros_ws/src/autonomy-payload/ap_msgs/msg'], 'geometry_msgs': ['/opt/ros/indigo/share/geometry_msgs/cmake/../msg'], 'autopilot_bridge': ['/home/odroid/acs_ros_ws/src/autopilot_bridge/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "6aa4127caa574d154d4fadf1234e6504";
  }

  static const char* value(const ::ap_msgs::SwarmVehicleState_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x6aa4127caa574d15ULL;
  static const uint64_t static_value2 = 0x4d4fadf1234e6504ULL;
};

template<class ContainerAllocator>
struct DataType< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ap_msgs/SwarmVehicleState";
  }

  static const char* value(const ::ap_msgs::SwarmVehicleState_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint16 vehicle_id\n\
uint16 subswarm_id\n\
time received_at\n\
uint8 swarm_state\n\
uint8 swarm_behavior\n\
uint8 vehicle_type\n\
autopilot_bridge/Geodometry state\n\
\n\
================================================================================\n\
MSG: autopilot_bridge/Geodometry\n\
# Odometry message but with GeoPoseWithCovariance instead\n\
\n\
std_msgs/Header header\n\
string child_frame_id\n\
GeoPoseWithCovariance pose\n\
geometry_msgs/TwistWithCovariance twist\n\
\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n\
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
\n\
================================================================================\n\
MSG: autopilot_bridge/GeoPoseWithCovariance\n\
# Pose using lat/lon/alt in place of x/y/z plus two altitude fields\n\
GeoPose pose\n\
\n\
# Row-major representation of the 6x6 covariance matrix\n\
# The orientation parameters use a fixed-axis representation.\n\
# In order, the parameters are:\n\
# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)\n\
float64[36] covariance\n\
\n\
================================================================================\n\
MSG: autopilot_bridge/GeoPose\n\
# 3-D point using lat/lon/alt, with two altitude options\n\
GeoPoint position\n\
\n\
# Quaternion orientation\n\
geometry_msgs/Quaternion orientation\n\
\n\
================================================================================\n\
MSG: autopilot_bridge/GeoPoint\n\
# WGS84 latitude, longitude, and MSL altitude\n\
float64 lat\n\
float64 lon\n\
float64 alt\n\
\n\
# Relative altitude (custom definable, but generally set w.r.t. some home point)\n\
float64 rel_alt\n\
\n\
# Flag field for which altitudes are valid\n\
bool using_alt\n\
bool using_rel_alt\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Quaternion\n\
# This represents an orientation in free space in quaternion form.\n\
\n\
float64 x\n\
float64 y\n\
float64 z\n\
float64 w\n\
\n\
================================================================================\n\
MSG: geometry_msgs/TwistWithCovariance\n\
# This expresses velocity in free space with uncertainty.\n\
\n\
Twist twist\n\
\n\
# Row-major representation of the 6x6 covariance matrix\n\
# The orientation parameters use a fixed-axis representation.\n\
# In order, the parameters are:\n\
# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)\n\
float64[36] covariance\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Twist\n\
# This expresses velocity in free space broken into its linear and angular parts.\n\
Vector3  linear\n\
Vector3  angular\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Vector3\n\
# This represents a vector in free space. \n\
\n\
float64 x\n\
float64 y\n\
float64 z\n\
";
  }

  static const char* value(const ::ap_msgs::SwarmVehicleState_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.vehicle_id);
      stream.next(m.subswarm_id);
      stream.next(m.received_at);
      stream.next(m.swarm_state);
      stream.next(m.swarm_behavior);
      stream.next(m.vehicle_type);
      stream.next(m.state);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct SwarmVehicleState_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ap_msgs::SwarmVehicleState_<ContainerAllocator>& v)
  {
    s << indent << "vehicle_id: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.vehicle_id);
    s << indent << "subswarm_id: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.subswarm_id);
    s << indent << "received_at: ";
    Printer<ros::Time>::stream(s, indent + "  ", v.received_at);
    s << indent << "swarm_state: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.swarm_state);
    s << indent << "swarm_behavior: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.swarm_behavior);
    s << indent << "vehicle_type: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.vehicle_type);
    s << indent << "state: ";
    s << std::endl;
    Printer< ::autopilot_bridge::Geodometry_<ContainerAllocator> >::stream(s, indent + "  ", v.state);
  }
};

} // namespace message_operations
} // namespace ros

#endif // AP_MSGS_MESSAGE_SWARMVEHICLESTATE_H
