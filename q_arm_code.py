# !/usr/bin/env python3
# coding: utf-8
# --------------------------------------------------------------------------------

import sys
sys.path.append("../")

from time import sleep
from Common.qarm_interface_wrapper import *

GRIPPER_IMPLEMENTATION = 1
arm = QArmInterface(GRIPPER_IMPLEMENTATION)
scan_barcode = BarcodeScanner.scan_barcode

# ------------------------- GRIPPER CONTROL --------------------------

# rotate_gripper(-80) = open, rotate_gripper(100) = closed.

def open_gripper():
    arm.rotate_gripper(-80)

def close_gripper():
    arm.rotate_gripper(100)

# --------------------------------------------------------------------------------
# STUDENT CODE BEGINS
# ---------------------------------------------------------------------------------

dropbox_position = [0.24088816810517527, -0.30158927247740874, 0.22464027501111783]


# ------------------------------ LEVEL 1 ------------------------------

def lvl_1():

    arm.home()

    # start open
    open_gripper()

 
    arm.rotate_base(18)
    arm.rotate_elbow(-20)
    sleep(1)
    arm.rotate_shoulder(49)
    sleep(1)

    # close to grab
    close_gripper()

    # move to dropbox
    arm.rotate_shoulder(-20)
    arm.set_arm_position(dropbox_position)

    # open to release
    open_gripper()


# ------------------------------ LEVEL 2 ------------------------------

def lvl_2():

    arm.home()

    open_gripper()

    arm.rotate_base(11)
    arm.rotate_elbow(-18)
    sleep(1)
    arm.rotate_shoulder(50)

    close_gripper()

    arm.rotate_shoulder(-20)
    arm.set_arm_position(dropbox_position)
    open_gripper()


# ------------------------------ LEVEL 3 ------------------------------

def lvl_3():

    arm.home()

    open_gripper()

    arm.rotate_base(5)
    arm.rotate_elbow(-15.8)
    sleep(1)
    arm.rotate_shoulder(50)
    sleep(1)

    close_gripper()

    arm.rotate_shoulder(-20)
    arm.set_arm_position(dropbox_position)
    open_gripper()


# ------------------------------ LEVEL 3a ------------------------------

def lvl_3a():

    arm.home()

    open_gripper()

    arm.rotate_base(-5.5)
    arm.rotate_elbow(-20)
    sleep(1)
    arm.rotate_shoulder(70)
    sleep(1)

    close_gripper()

    arm.set_arm_position(dropbox_position)
    open_gripper()


# ---------------------------------------------------------------------------------
# STUDENT CODE ENDS
# ---------------------------------------------------------------------------------

arm.end_arm_connection()
