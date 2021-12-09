
#! /usr/bin/env python3

###
# KINOVA (R) KORTEX (TM)
#
# Copyright (c) 2018 Kinova inc. All rights reserved.
#
# This software may be modified and distributed
# under the terms of the BSD 3-Clause license.
#
# Refer to the LICENSE file for details.
#
###

import time
import sys
import os
import threading
import pyrealsense2 as rs
from cyberpunk_test import example_trajectory, populateCartesianCoordinate

from kortex_api.TCPTransport import TCPTransport
from kortex_api.RouterClient import RouterClient
from kortex_api.SessionManager import SessionManager



from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient

from kortex_api.autogen.messages import Session_pb2, Base_pb2

class GripperCommandExample:
    def __init__(self, router, proportional_gain = 2.0):

        self.proportional_gain = proportional_gain
        self.router = router

        # Create base client using TCP router
        self.base = BaseClient(self.router)

# Maximum allowed waiting time during actions (in seconds)
TIMEOUT_DURATION = 20

# Create closure to set an event after an END or an ABORT
def check_for_end_or_abort(e):
    """Return a closure checking for END or ABORT notifications

    Arguments:
    e -- event to signal when the action is completed
        (will be set when an END or ABORT occurs)
    """
    def check(notification, e = e):
        print("EVENT : " + \
              Base_pb2.ActionEvent.Name(notification.action_event))
        if notification.action_event == Base_pb2.ACTION_END \
        or notification.action_event == Base_pb2.ACTION_ABORT:
            e.set()
    return check


def example_move_to_home_position(base):
    # Make sure the arm is in Single Level Servoing mode
    base_servo_mode = Base_pb2.ServoingModeInformation()
    base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
    base.SetServoingMode(base_servo_mode)
    
    # Move arm to ready position
    print("Moving the arm to a safe position")
    action_type = Base_pb2.RequestedActionType()
    action_type.action_type = Base_pb2.REACH_JOINT_ANGLES
    action_list = base.ReadAllActions(action_type)
    action_handle = None
    for action in action_list.action_list:
        if action.name == "Home":
            action_handle = action.handle

    if action_handle == None:
        print("Can't reach safe position. Exiting")
        sys.exit(0)

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )
    
    base.ExecuteActionFromReference(action_handle)
    
    # Leave time to action to complete
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Safe position reached")
    else:
        print("Timeout on action notification wait")
    return finished

def example_twist_command(base, lin_x, lin_y, lin_z):

    command = Base_pb2.TwistCommand()

    command.reference_frame = Base_pb2.CARTESIAN_REFERENCE_FRAME_TOOL
    command.duration = 0

    twist = command.twist
    twist.linear_x = lin_x
    twist.linear_y = lin_y
    twist.linear_z = lin_z
    twist.angular_x = 0
    twist.angular_y = 0
    twist.angular_z = 0

    print ("Sending the twist command for 5 seconds...")
    base.SendTwistCommand(command)
    

    print ("Sending the twist command for 5 seconds...")
    base.SendTwistCommand(command)


    # Let time for twist to be executed
    time.sleep(5)

    print ("Stopping the robot...")
    base.Stop()
    time.sleep(1)

 

    return True

def ExampleSendGripperCommands(self, gripPos):

        # Create the GripperCommand we will send
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()

        # Close the gripper with position increments
        print("Performing gripper test in position...")
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        position = 0.00


        finger.finger_identifier = 1
        
        
        position = gripPos
        finger.value = position
        print("Going to position {:0.2f}...".format(finger.value))
        self.base.SendGripperCommand(gripper_command)
        time.sleep(1)

        return True

def main(x,y,z):
    # Import the utilities helper module
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import utilities

    # Parse arguments
    args = utilities.parseConnectionArguments()
    
    # Create connection to the device and get the router
    with utilities.DeviceConnection.createTcpConnection(args) as router:

        # Create required services
        gripper = GripperCommandExample(router)
        base = BaseClient(router)
        

        # Example core
        success = True
        success &= example_move_to_home_position(base)
        success &= example_trajectory(base, .56, .2, .2)

        # Create a context object. This object owns the handles to all connected realsense devices
        pipeline = rs.pipeline()

        # Configure streams
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        # Start streaming
        pipeline.start(config)
        print('streaming started')

        y = .2
        flag = True
        while True:
            # This call waits until a new coherent set of frames is available on a device
            # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            width = int(depth.get_width())
            height = int(depth.get_height())

            distance = depth.get_distance(int(width/2), int(height/2))

            print(width)
            print(height)
            print(distance)
            example_twist_command(base, 0, -.01, .0)
            y -= .01

            if(y < -.2):
                flag = False


            min_distance = 4

        

        """
        success &= example_twist_command(base, .025, -.04, .03)
        success &= ExampleSendGripperCommands(gripper, .4)
        success &= example_twist_command(base, -.025, .04, -.03)
        success &= example_twist_command(base, -.025, -.04, .03)
        success &= ExampleSendGripperCommands(gripper, 0)
        success &= example_move_to_home_position(base)
        success &= example_twist_command(base, .025, -.04, .03)
        success &= ExampleSendGripperCommands(gripper, .4)
        success &= example_twist_command(base, .025, .04, -.03)
        success &= example_twist_command(base, -0.04, -.055, -.02)
        success &= ExampleSendGripperCommands(gripper, 0)
        success &= example_move_to_home_position(base)
        """

        

        #success &= SecondMovement(base)

        return 0 if success else 1

if __name__ == "__main__":
    main(.025, -.05, .03)
    ExampleSendGripperCommands(gripper, 0.4)