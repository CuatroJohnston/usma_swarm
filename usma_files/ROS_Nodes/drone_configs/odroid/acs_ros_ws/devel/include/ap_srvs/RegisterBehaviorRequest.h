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
 * Auto-generated by genmsg_cpp from file /home/odroid/acs_ros_ws/src/autonomy-payload/ap_srvs/srv/RegisterBehavior.srv
 *
 */


#ifndef AP_SRVS_MESSAGE_REGISTERBEHAVIORREQUEST_H
#define AP_SRVS_MESSAGE_REGISTERBEHAVIORREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace ap_srvs
{
template <class ContainerAllocator>
struct RegisterBehaviorRequest_
{
  typedef RegisterBehaviorRequest_<ContainerAllocator> Type;

  RegisterBehaviorRequest_()
    : id(0)
    , name()
    , wpt_ctrl(false)  {
    }
  RegisterBehaviorRequest_(const ContainerAllocator& _alloc)
    : id(0)
    , name(_alloc)
    , wpt_ctrl(false)  {
    }



   typedef uint8_t _id_type;
  _id_type id;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _name_type;
  _name_type name;

   typedef uint8_t _wpt_ctrl_type;
  _wpt_ctrl_type wpt_ctrl;




  typedef boost::shared_ptr< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> const> ConstPtr;

}; // struct RegisterBehaviorRequest_

typedef ::ap_srvs::RegisterBehaviorRequest_<std::allocator<void> > RegisterBehaviorRequest;

typedef boost::shared_ptr< ::ap_srvs::RegisterBehaviorRequest > RegisterBehaviorRequestPtr;
typedef boost::shared_ptr< ::ap_srvs::RegisterBehaviorRequest const> RegisterBehaviorRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace ap_srvs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'nav_msgs': ['/opt/ros/indigo/share/nav_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/indigo/share/std_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/indigo/share/actionlib_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/indigo/share/sensor_msgs/cmake/../msg'], 'ap_msgs': ['/home/odroid/acs_ros_ws/src/autonomy-payload/ap_msgs/msg'], 'geometry_msgs': ['/opt/ros/indigo/share/geometry_msgs/cmake/../msg'], 'autopilot_bridge': ['/home/odroid/acs_ros_ws/src/autopilot_bridge/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "6d095a0fd7e98d0c701b1f6258043634";
  }

  static const char* value(const ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x6d095a0fd7e98d0cULL;
  static const uint64_t static_value2 = 0x701b1f6258043634ULL;
};

template<class ContainerAllocator>
struct DataType< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ap_srvs/RegisterBehaviorRequest";
  }

  static const char* value(const ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8 id\n\
string name\n\
bool wpt_ctrl\n\
";
  }

  static const char* value(const ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.id);
      stream.next(m.name);
      stream.next(m.wpt_ctrl);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct RegisterBehaviorRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ap_srvs::RegisterBehaviorRequest_<ContainerAllocator>& v)
  {
    s << indent << "id: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.id);
    s << indent << "name: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.name);
    s << indent << "wpt_ctrl: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.wpt_ctrl);
  }
};

} // namespace message_operations
} // namespace ros

#endif // AP_SRVS_MESSAGE_REGISTERBEHAVIORREQUEST_H
