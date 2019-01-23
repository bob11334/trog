#include <boost/assign/list_of.hpp>
#include <string>
#include <ros/ros.h>

#include "trog_control/trog_hardware.h"
#include "roboteq_msgs/Command.h"
#include "roboteq_msgs/Feedback.h"
#include "roboteq_driver/controller.h"

namespace
{
  const uint8_t LEFT = 0, RIGHT = 1;
  const float WHEEL_DIAMETER = 0.254;
  const double PI  =3.141592653589793238463;
  const float MAX_SPEED = 2.0; // m/s
};

namespace trog_control
{

  /**
  * Initialize Trog hardware
  */
   TrogHardware::TrogHardware(ros::NodeHandle nh, ros::NodeHandle private_nh): nh_(nh), private_nh_(private_nh), controller_("/dev/ttyACM0", 115200)
  {
    left_motor_pub = nh.advertise<roboteq_msgs::Command>("/left/cmd", 50); //TODO: 50?
    right_motor_pub = nh.advertise<roboteq_msgs::Command>("/right/cmd", 50); //TODO: 50?


    left_feedback_sub = nh.subscribe("/left/feedback", 1, &TrogHardware::updateJointsFromHardware, this);
    right_feedback_sub = nh.subscribe("/right/feedback", 1, &TrogHardware::updateJointsFromHardware, this);

    registerControlInterfaces();

    // Set to true to reset position offset
    for(int i = 0; i < 2; i++)
      reset_encoder_[i] = true;
  }

  /**
  * Register interfaces with the RobotHW interface manager, allowing ros_control operation
  */
  void TrogHardware::registerControlInterfaces()
  {
    ros::V_string joint_names = boost::assign::list_of("rear_left_wheel")("rear_right_wheel");
    for (unsigned int i = 0; i < joint_names.size(); i++)
    {
      hardware_interface::JointStateHandle joint_state_handle(joint_names[i],
                                                              &joints_[i].position, 
                                                              &joints_[i].velocity,
                                                              &joints_[i].effort);
      joint_state_interface_.registerHandle(joint_state_handle);

      hardware_interface::JointHandle joint_handle(joint_state_handle, &joints_[i].velocity_command);
      velocity_joint_interface_.registerHandle(joint_handle);
    }
    registerInterface(&joint_state_interface_);
    registerInterface(&velocity_joint_interface_);
  }

  /**
   *  Get latest velocity commands from ros_control via joint structure, and send to MCU
   */
  void TrogHardware::writeCommandsToHardware()
  {
    double diff_speed_left = joints_[LEFT].velocity_command;
    double diff_speed_right = joints_[RIGHT].velocity_command;

    //    limitDifferentialSpeed(diff_speed_left, diff_speed_right);

    // Set up messages
    roboteq_msgs::Command cmd_left;
    cmd_left.setpoint = diff_speed_left;

    roboteq_msgs::Command cmd_right;
    cmd_right.setpoint = diff_speed_right;

    //Publish
    left_motor_pub.publish(cmd_left);
    right_motor_pub.publish(cmd_right);
  }

  
  /**
   *  Process feedback and store in joint structure for ros_control
   */
  void TrogHardware::updateJointsFromHardware(const roboteq_msgs::Feedback& feedback)
  { 
    // Update ROS Control structure
    int ch = feedback.channel - 1;
    
    // Reset Travel Offsets
    if (reset_encoder_[ch])
    {
		joints_[ch].position_offset = feedback.measured_position;
		reset_encoder_[ch] = false;
		joints_[ch].velocity = feedback.measured_velocity;	
		return;
	}
	// Update joint structures
    double delta = feedback.measured_position - joints_[ch].position - joints_[ch].position_offset;
	joints_[ch].position += delta;
    joints_[ch].velocity = feedback.measured_velocity;
  }

  
  void TrogHardware::limitDifferentialSpeed(double &diff_speed_left, double &diff_speed_right)
  {
    double large_speed = std::max(std::abs(diff_speed_left), std::abs(diff_speed_right));

    if (large_speed > MAX_SPEED)
      {
	diff_speed_left *= MAX_SPEED / large_speed;
	diff_speed_right *= MAX_SPEED / large_speed;
      }
  }

  
}  // namespace trog_base
