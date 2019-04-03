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
 * Auto-generated by gensrv_cpp from file /home/odroid/acs_ros_ws/src/autopilot_bridge/srv/ParamSetList.srv
 *
 */


#ifndef AUTOPILOT_BRIDGE_MESSAGE_PARAMSETLIST_H
#define AUTOPILOT_BRIDGE_MESSAGE_PARAMSETLIST_H

#include <ros/service_traits.h>


#include <autopilot_bridge/ParamSetListRequest.h>
#include <autopilot_bridge/ParamSetListResponse.h>


namespace autopilot_bridge
{

struct ParamSetList
{

typedef ParamSetListRequest Request;
typedef ParamSetListResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct ParamSetList
} // namespace autopilot_bridge


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::autopilot_bridge::ParamSetList > {
  static const char* value()
  {
    return "7c20195a6434b00060c5d34397ef8702";
  }

  static const char* value(const ::autopilot_bridge::ParamSetList&) { return value(); }
};

template<>
struct DataType< ::autopilot_bridge::ParamSetList > {
  static const char* value()
  {
    return "autopilot_bridge/ParamSetList";
  }

  static const char* value(const ::autopilot_bridge::ParamSetList&) { return value(); }
};


// service_traits::MD5Sum< ::autopilot_bridge::ParamSetListRequest> should match 
// service_traits::MD5Sum< ::autopilot_bridge::ParamSetList > 
template<>
struct MD5Sum< ::autopilot_bridge::ParamSetListRequest>
{
  static const char* value()
  {
    return MD5Sum< ::autopilot_bridge::ParamSetList >::value();
  }
  static const char* value(const ::autopilot_bridge::ParamSetListRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::autopilot_bridge::ParamSetListRequest> should match 
// service_traits::DataType< ::autopilot_bridge::ParamSetList > 
template<>
struct DataType< ::autopilot_bridge::ParamSetListRequest>
{
  static const char* value()
  {
    return DataType< ::autopilot_bridge::ParamSetList >::value();
  }
  static const char* value(const ::autopilot_bridge::ParamSetListRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::autopilot_bridge::ParamSetListResponse> should match 
// service_traits::MD5Sum< ::autopilot_bridge::ParamSetList > 
template<>
struct MD5Sum< ::autopilot_bridge::ParamSetListResponse>
{
  static const char* value()
  {
    return MD5Sum< ::autopilot_bridge::ParamSetList >::value();
  }
  static const char* value(const ::autopilot_bridge::ParamSetListResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::autopilot_bridge::ParamSetListResponse> should match 
// service_traits::DataType< ::autopilot_bridge::ParamSetList > 
template<>
struct DataType< ::autopilot_bridge::ParamSetListResponse>
{
  static const char* value()
  {
    return DataType< ::autopilot_bridge::ParamSetList >::value();
  }
  static const char* value(const ::autopilot_bridge::ParamSetListResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // AUTOPILOT_BRIDGE_MESSAGE_PARAMSETLIST_H
