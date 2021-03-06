
#ifndef TROG_HARDWARE_H
#define TROG_HARDWARE_H

#include "hardware_interface/joint_state_interface.h"
#include "hardware_interface/joint_command_interface.h"
#include "hardware_interface/robot_hw.h"
#include "sensor_msgs/JointState.h"

#include <ros/ros.h>
#include <roboteq_driver/controller.h>
#include <roboteq_msgs/Feedback.h>

namespace trog_control
{
  /**
  * Class representing Trog hardware, allows for ros_control to modify internal state via joint interfaces
  */
  class TrogHardware : public hardware_interface::RobotHW
  {
    public:
      TrogHardware(ros::NodeHandle nh, ros::NodeHandle private_nh);

      // Read data from encoders
      void updateJointsFromHardware(const roboteq_msgs::Feedback& feedback);

      // Send commands to roboteq node
      void writeCommandsToHardware();

    private:    

      bool uncalibrated[2];
      
      void registerControlInterfaces();

      roboteq::Controller controller_;

      //void limitDifferentialSpeed(double &travel_speed_left, double &travel_speed_right);

      ros::NodeHandle nh_, private_nh_;

      // Roboteq motor controller
      ros::Publisher left_motor_pub;
      ros::Publisher right_motor_pub;
      ros::Subscriber left_feedback_sub;
      ros::Subscriber right_feedback_sub;
      
      // Calibrating encoders
      bool reset_encoder_[2]; 

      // ROS Control interfaces
      hardware_interface::JointStateInterface joint_state_interface_;
      hardware_interface::VelocityJointInterface velocity_joint_interface_;


      void limitDifferentialSpeed(double &diff_speed_left, double &diff_speed_right);

      double linearToAngular(const double &travel) const;

      double angularToLinear(const double &angle) const;
      
      double polling_timeout_;

      /**
      * Joint structure that is hooked to ros_control's InterfaceManager, to allow control via diff_drive_controller
      */
      struct Joint
      {
        double position;
        double position_offset;
        double velocity;
        double effort;
        double velocity_command;

        Joint() :
          position(0), velocity(0), effort(0), velocity_command(0)
        { }
      } joints_[2];
    };

}  // namespace trog_base
#endif  // TROG_HARDWARE_H
