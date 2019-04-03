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
 * Auto-generated by genmsg_cpp from file /home/odroid/acs_ros_ws/src/autonomy-payload/ap_msgs/msg/BehaviorGroupState.msg
 *
 */


#ifndef AP_MSGS_MESSAGE_BEHAVIORGROUPSTATE_H
#define AP_MSGS_MESSAGE_BEHAVIORGROUPSTATE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <ap_msgs/BehaviorState.h>

namespace ap_msgs
{
template <class ContainerAllocator>
struct BehaviorGroupState_
{
  typedef BehaviorGroupState_<ContainerAllocator> Type;

  BehaviorGroupState_()
    : active_behavior(0)
    , behaviors()  {
    }
  BehaviorGroupState_(const ContainerAllocator& _alloc)
    : active_behavior(0)
    , behaviors(_alloc)  {
    }



   typedef uint8_t _active_behavior_type;
  _active_behavior_type active_behavior;

   typedef std::vector< ::ap_msgs::BehaviorState_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::ap_msgs::BehaviorState_<ContainerAllocator> >::other >  _behaviors_type;
  _behaviors_type behaviors;




  typedef boost::shared_ptr< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> const> ConstPtr;

}; // struct BehaviorGroupState_

typedef ::ap_msgs::BehaviorGroupState_<std::allocator<void> > BehaviorGroupState;

typedef boost::shared_ptr< ::ap_msgs::BehaviorGroupState > BehaviorGroupStatePtr;
typedef boost::shared_ptr< ::ap_msgs::BehaviorGroupState const> BehaviorGroupStateConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ap_msgs::BehaviorGroupState_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> >::stream(s, "", v);
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
struct IsFixedSize< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "61c10d40a72ba1aa819a6e0972f5cd9f";
  }

  static const char* value(const ::ap_msgs::BehaviorGroupState_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x61c10d40a72ba1aaULL;
  static const uint64_t static_value2 = 0x819a6e0972f5cd9fULL;
};

template<class ContainerAllocator>
struct DataType< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ap_msgs/BehaviorGroupState";
  }

  static const char* value(const ::ap_msgs::BehaviorGroupState_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8 active_behavior\n\
ap_msgs/BehaviorState[] behaviors\n\
\n\
================================================================================\n\
MSG: ap_msgs/BehaviorState\n\
uint8  behavior_id\n\
uint32 sequence\n\
bool   is_ready\n\
bool   is_active\n\
bool   is_paused\n\
";
  }

  static const char* value(const ::ap_msgs::BehaviorGroupState_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.active_behavior);
      stream.next(m.behaviors);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct BehaviorGroupState_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ap_msgs::BehaviorGroupState_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ap_msgs::BehaviorGroupState_<ContainerAllocator>& v)
  {
    s << indent << "active_behavior: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.active_behavior);
    s << indent << "behaviors[]" << std::endl;
    for (size_t i = 0; i < v.behaviors.size(); ++i)
    {
      s << indent << "  behaviors[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::ap_msgs::BehaviorState_<ContainerAllocator> >::stream(s, indent + "    ", v.behaviors[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // AP_MSGS_MESSAGE_BEHAVIORGROUPSTATE_H
