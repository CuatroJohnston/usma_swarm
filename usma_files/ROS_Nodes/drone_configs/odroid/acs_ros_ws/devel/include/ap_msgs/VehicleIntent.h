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
 * Auto-generated by genmsg_cpp from file /home/odroid/acs_ros_ws/src/autonomy-payload/ap_msgs/msg/VehicleIntent.msg
 *
 */


#ifndef AP_MSGS_MESSAGE_VEHICLEINTENT_H
#define AP_MSGS_MESSAGE_VEHICLEINTENT_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <autopilot_bridge/LLA.h>

namespace ap_msgs
{
template <class ContainerAllocator>
struct VehicleIntent_
{
  typedef VehicleIntent_<ContainerAllocator> Type;

  VehicleIntent_()
    : vehicle_id(0)
    , swarm_behavior(0)
    , loc()  {
    }
  VehicleIntent_(const ContainerAllocator& _alloc)
    : vehicle_id(0)
    , swarm_behavior(0)
    , loc(_alloc)  {
    }



   typedef uint8_t _vehicle_id_type;
  _vehicle_id_type vehicle_id;

   typedef uint8_t _swarm_behavior_type;
  _swarm_behavior_type swarm_behavior;

   typedef  ::autopilot_bridge::LLA_<ContainerAllocator>  _loc_type;
  _loc_type loc;




  typedef boost::shared_ptr< ::ap_msgs::VehicleIntent_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ap_msgs::VehicleIntent_<ContainerAllocator> const> ConstPtr;

}; // struct VehicleIntent_

typedef ::ap_msgs::VehicleIntent_<std::allocator<void> > VehicleIntent;

typedef boost::shared_ptr< ::ap_msgs::VehicleIntent > VehicleIntentPtr;
typedef boost::shared_ptr< ::ap_msgs::VehicleIntent const> VehicleIntentConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ap_msgs::VehicleIntent_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ap_msgs::VehicleIntent_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace ap_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'nav_msgs': ['/opt/ros/indigo/share/nav_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/indigo/share/sensor_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/indigo/share/actionlib_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/indigo/share/std_msgs/cmake/../msg'], 'ap_msgs': ['/home/odroid/acs_ros_ws/src/autonomy-payload/ap_msgs/msg'], 'geometry_msgs': ['/opt/ros/indigo/share/geometry_msgs/cmake/../msg'], 'autopilot_bridge': ['/home/odroid/acs_ros_ws/src/autopilot_bridge/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::ap_msgs::VehicleIntent_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ap_msgs::VehicleIntent_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ap_msgs::VehicleIntent_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ap_msgs::VehicleIntent_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ap_msgs::VehicleIntent_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ap_msgs::VehicleIntent_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ap_msgs::VehicleIntent_<ContainerAllocator> >
{
  static const char* value()
  {
    return "1baad67ae12e46c06ebeaa3de44f6e6e";
  }

  static const char* value(const ::ap_msgs::VehicleIntent_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x1baad67ae12e46c0ULL;
  static const uint64_t static_value2 = 0x6ebeaa3de44f6e6eULL;
};

template<class ContainerAllocator>
struct DataType< ::ap_msgs::VehicleIntent_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ap_msgs/VehicleIntent";
  }

  static const char* value(const ::ap_msgs::VehicleIntent_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ap_msgs::VehicleIntent_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8 vehicle_id\n\
uint8 swarm_behavior\n\
autopilot_bridge/LLA loc\n\
\n\
================================================================================\n\
MSG: autopilot_bridge/LLA\n\
float64 lat\n\
float64 lon\n\
float64 alt\n\
";
  }

  static const char* value(const ::ap_msgs::VehicleIntent_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ap_msgs::VehicleIntent_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.vehicle_id);
      stream.next(m.swarm_behavior);
      stream.next(m.loc);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct VehicleIntent_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ap_msgs::VehicleIntent_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ap_msgs::VehicleIntent_<ContainerAllocator>& v)
  {
    s << indent << "vehicle_id: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.vehicle_id);
    s << indent << "swarm_behavior: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.swarm_behavior);
    s << indent << "loc: ";
    s << std::endl;
    Printer< ::autopilot_bridge::LLA_<ContainerAllocator> >::stream(s, indent + "  ", v.loc);
  }
};

} // namespace message_operations
} // namespace ros

#endif // AP_MSGS_MESSAGE_VEHICLEINTENT_H
