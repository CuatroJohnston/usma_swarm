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
 * Auto-generated by genmsg_cpp from file /home/odroid/acs_ros_ws/src/autonomy-payload/ap_msgs/msg/SwarmStateStamped.msg
 *
 */


#ifndef AP_MSGS_MESSAGE_SWARMSTATESTAMPED_H
#define AP_MSGS_MESSAGE_SWARMSTATESTAMPED_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>
#include <ap_msgs/SwarmVehicleState.h>

namespace ap_msgs
{
template <class ContainerAllocator>
struct SwarmStateStamped_
{
  typedef SwarmStateStamped_<ContainerAllocator> Type;

  SwarmStateStamped_()
    : header()
    , crashed_list()
    , swarm()  {
    }
  SwarmStateStamped_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , crashed_list(_alloc)
    , swarm(_alloc)  {
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef std::vector<uint16_t, typename ContainerAllocator::template rebind<uint16_t>::other >  _crashed_list_type;
  _crashed_list_type crashed_list;

   typedef std::vector< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >::other >  _swarm_type;
  _swarm_type swarm;




  typedef boost::shared_ptr< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> const> ConstPtr;

}; // struct SwarmStateStamped_

typedef ::ap_msgs::SwarmStateStamped_<std::allocator<void> > SwarmStateStamped;

typedef boost::shared_ptr< ::ap_msgs::SwarmStateStamped > SwarmStateStampedPtr;
typedef boost::shared_ptr< ::ap_msgs::SwarmStateStamped const> SwarmStateStampedConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ap_msgs::SwarmStateStamped_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace ap_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': True}
// {'nav_msgs': ['/opt/ros/indigo/share/nav_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/indigo/share/sensor_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/indigo/share/actionlib_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/indigo/share/std_msgs/cmake/../msg'], 'ap_msgs': ['/home/odroid/acs_ros_ws/src/autonomy-payload/ap_msgs/msg'], 'geometry_msgs': ['/opt/ros/indigo/share/geometry_msgs/cmake/../msg'], 'autopilot_bridge': ['/home/odroid/acs_ros_ws/src/autopilot_bridge/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> >
{
  static const char* value()
  {
    return "557f14204e6d11be03676b20f863ebda";
  }

  static const char* value(const ::ap_msgs::SwarmStateStamped_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x557f14204e6d11beULL;
  static const uint64_t static_value2 = 0x03676b20f863ebdaULL;
};

template<class ContainerAllocator>
struct DataType< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ap_msgs/SwarmStateStamped";
  }

  static const char* value(const ::ap_msgs::SwarmStateStamped_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> >
{
  static const char* value()
  {
    return "std_msgs/Header header\n\
uint16[] crashed_list\n\
ap_msgs/SwarmVehicleState[] swarm\n\
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
MSG: ap_msgs/SwarmVehicleState\n\
uint16 vehicle_id\n\
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

  static const char* value(const ::ap_msgs::SwarmStateStamped_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.crashed_list);
      stream.next(m.swarm);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct SwarmStateStamped_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ap_msgs::SwarmStateStamped_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ap_msgs::SwarmStateStamped_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "crashed_list[]" << std::endl;
    for (size_t i = 0; i < v.crashed_list.size(); ++i)
    {
      s << indent << "  crashed_list[" << i << "]: ";
      Printer<uint16_t>::stream(s, indent + "  ", v.crashed_list[i]);
    }
    s << indent << "swarm[]" << std::endl;
    for (size_t i = 0; i < v.swarm.size(); ++i)
    {
      s << indent << "  swarm[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::ap_msgs::SwarmVehicleState_<ContainerAllocator> >::stream(s, indent + "    ", v.swarm[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // AP_MSGS_MESSAGE_SWARMSTATESTAMPED_H
