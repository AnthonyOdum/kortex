
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
from kortex_api.autogen.messages.ProductConfiguration_pb2 import ARM_LATERALITY_LEFT
#import pyrealsense2 as rs


from kortex_api.TCPTransport import TCPTransport
from kortex_api.RouterClient import RouterClient
from kortex_api.SessionManager import SessionManager



from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient

from kortex_api.autogen.messages import Session_pb2, Base_pb2

class GripperCommandExample:
    def __init__(self, router, proportional_gain = 2.0):

        self.proportional_gain = proportional_gain
        self.router = router

        # Create base client using TCP router
        self.base = BaseClient(self.router)

# Maximum allowed waiting time during actions (in seconds)
TIMEOUT_DURATION = 20

SPEED = 5.0

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

def populateCartesianCoordinate(x,y,z, bR, tX,tY,tZ):
    waypoint = Base_pb2.CartesianWaypoint() 
    
    waypoint.pose.x = x
    waypoint.pose.y = y
    waypoint.pose.z = z
    waypoint.blending_radius = bR
    waypoint.pose.theta_x = tX
    waypoint.pose.theta_y = tY
    waypoint.pose.theta_z = tZ

    """
    waypoint.pose.x = .5
    waypoint.pose.y = .2
    waypoint.pose.z = .4
    waypoint.blending_radius = 0
    waypoint.pose.theta_x = 89.169
    waypoint.pose.theta_y =1.072
    waypoint.pose.theta_z = 90.428
    """
    waypoint.reference_frame = Base_pb2.CARTESIAN_REFERENCE_FRAME_BASE
    
    
    return waypoint

def example_trajectory(base, x, y, z):

    base_servo_mode = Base_pb2.ServoingModeInformation()
    base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
    base.SetServoingMode(base_servo_mode)
    product = base.GetProductConfiguration()
    waypointsDefinition = tuple(tuple())
    kTheta_x = 89.169
    kTheta_y = 1.072
    kTheta_z = 90.428
    waypointsDefinition = ((x, y, z, 0.0, kTheta_x, kTheta_y, kTheta_z))
    
    waypoints = Base_pb2.WaypointList()
    
    waypoints.duration = 0.0
    
    index = 0
    for waypointDefinition in waypointsDefinition:
        waypoint = waypoints.waypoints.add()
        waypoint.cartesian_waypoint.CopyFrom(populateCartesianCoordinate(*waypointsDefinition))
        index = index + 1 

    # Verify validity of waypoints
    result = base.ValidateWaypointList(waypoints);
    if(len(result.trajectory_error_report.trajectory_error_elements) == 0):
        e = threading.Event()
        notification_handle = base.OnNotificationActionTopic(   check_for_end_or_abort(e),
                                                                Base_pb2.NotificationOptions())


        waypoints.use_optimal_blending = True
        base.ExecuteWaypointTrajectory(waypoints)
        
        print("Waiting for trajectory to finish ...")
        finished_opt = e.wait(TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)

        if(finished_opt):
            print("Cartesian trajectory with optimization completed ")
        else:
            print("Timeout on action notification wait for optimized trajectory")
        

        return finished_opt
        
    else:
        print("Error found in trajectory") 
        result.trajectory_error_report.PrintDebugString();
"""
def initialize():
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

    return gripper,base;

"""

def robot_panning(x:float, y:float, z:float):
    start_y = .189
    start_x = .558
    start_z = .134
    # Import the utilities helper module
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import utilities

    # Parse arguments
    args = utilities.parseConnectionArguments()

    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()
    print('pipeline created')

    # Configure streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    print('config configured')

    # Start streaming
    pipeline.start(config)
    print('streaming started')

    
    command = Base_pb2.TwistCommand()
    twist = command.twist
    
    
    # Create connection to the device and get the router
    with utilities.DeviceConnection.createTcpConnection(args) as router:

        # Create required services
        gripper = GripperCommandExample(router)
        base = BaseClient(router)

        # Example core
        success = True
        success &= example_move_to_home_position(base)
        success &= ExampleSendGripperCommands(gripper, 0)
        if(success):
            print('im home')
            print(base.GetMeasuredCartesianPose())
        success &= example_trajectory(base, start_x, start_y, start_z)
        
        subtraction = True
        minDistance = .5
        objectFacingPose = {
            'x': 0,
            'y': 0,
            'z': 0,
            'theta_x': 0,
            'theta_y': 0,
            'theta_z': 0,
        }
        while(success):

            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            width = int(depth.get_width())
            height = int(depth.get_height())

            distance = depth.get_distance(int(width/2.0), int(height/2.0))

            print('Current Distance: ', distance)
            print('Current Minimum Distance: ', minDistance)

            if distance < minDistance and distance != 0:
                print('New minimum distance')
                minDistance = distance
                objectFacingPose['x'] = base.GetMeasuredCartesianPose().x
                objectFacingPose['y'] = base.GetMeasuredCartesianPose().y
                objectFacingPose['z']= base.GetMeasuredCartesianPose().z
                objectFacingPose['theta_x'] = base.GetMeasuredCartesianPose().theta_x
                objectFacingPose['theta_y'] = base.GetMeasuredCartesianPose().theta_y
                objectFacingPose['theta_z'] = base.GetMeasuredCartesianPose().theta_z

            
            """
            if(y >= .189):
                example_trajectory(base, x, -.208, z)
            else:
                example_trajectory(base, x, .189, z)

            """
            if(start_y <= .189 and subtraction):
                start_y -= .004
                example_trajectory(base, start_x, start_y, start_z)
                #print(base.GetMeasuredCartesianPose())
                #print(y)
                if(start_y <= -.208):
                    print('robot facing object position: ', objectFacingPose)
                    print('minimum distance: ', minDistance)
                    #print('subtraction is now false')
                    subtraction = False
            
            if(minDistance != .5 and start_y <= -.208):
                working = True
                working &= example_trajectory(base, objectFacingPose['x'], objectFacingPose['y'], objectFacingPose['z'])
                working &= example_twist_command(base, .0, 0, .04)

                working &= ExampleSendGripperCommands(gripper, 0.4)
                working &= example_move_to_home_position(base)

                working &= example_trajectory(base, x, y, z)
                working &= ExampleSendGripperCommands(gripper, 0)
                working &= example_move_to_home_position(base)
                minDistance = .5



            if(start_y <= -.208 or not subtraction):
                start_y += .004
                example_trajectory(base, start_x, start_y, start_z)
                #print(base.GetMeasuredCartesianPose())
                if(start_y >= .189):
                    print('robot facing object position: ', objectFacingPose)
                    print('minimum distance: ', minDistance)
                    subtraction = True
                    start_y = .189

            if(minDistance != .5 and start_y >= .189):
                working = True
                working &= example_trajectory(base, objectFacingPose['x'], objectFacingPose['y'], objectFacingPose['z'])
                working &= example_twist_command(base, .0, 0, .04)

                working &= ExampleSendGripperCommands(gripper, 0.4)
                working &= example_move_to_home_position(base)

                working &= example_trajectory(base, x, y, z)
                working &= ExampleSendGripperCommands(gripper, 0)
                working &= example_move_to_home_position(base)
                minDistance = .5
            
            base.SendTwistCommand(command)

    return 0 if success else 1

def robot_demo(x, y, z):
    
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
        if(success):
            print('im home')
        success &= example_trajectory(base, x, y, z)
        if(success):
            print('i am at position 1')
        success &= example_trajectory(base, x, y - .41, z)
        if(success):
            print('i am at position 2')
        """
        success &= example_twist_command(base, .025, -.04, .03)
        success &= ExampleSendGripperCommands(gripper, .4)
        success &= example_twist_command(base, .025, .04, -.03)
        success &= example_trajectory(base, x, y, z)
        """

        return 0 if success else 1

if __name__ == "__robot_demo__":
    exit(robot_demo())
