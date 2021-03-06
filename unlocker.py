#!/usr/bin/env python3
"""

Notes:
    # Device discovery code taken from PyBluez simple example inquiry.py
    https://www.google.com/search?client=safari&rls=en&q=PyBluez+simple+example+inquiry.py&ie=UTF-8&oe=UTF-8

    #?Quartz setup needs a code fix
    #?https://stackoverflow.com/questions/42530309/no-such-file-requirements-txt-error-while-installing-quartz-module

    Objc
    pip install pyobjc

    Recognize if under lock screen
    https://stackoverflow.com/questions/11505255/osx-check-if-the-screen-is-locked


    Lock & Unlock
    https://apple.stackexchange.com/questions/259508/how-to-unlock-my-mac-remotely
 
"""
import json
import os
import sys
import subprocess
import time
import Quartz
import logging
import logging.config
from genkey import decode
from config import allowed_devices,\
                   user_credentials
logging.config.fileConfig('logging.conf')
logger = None


lock_allowed = False

unlock_delay = 3

def get_devices():
    addr = name = None

    logger.debug("Discovering devices ...")
    p = subprocess.Popen("/usr/local/bin/blueutil  --inquiry 1 --format json",
                        shell=True,
                        stdout=subprocess.PIPE, )
    stdout = p.communicate()[0]
    logger.debug("blueutil: %s" % stdout)
    return json.loads(stdout)


def unlock_devices(nearby_devices):
    for nbdev in nearby_devices:
        addr = nbdev.get("address", None)
        name = nbdev.get("name", None)
        logger.debug("   {} - {}".format(addr, name))
        
        for dev in allowed_devices:
            allow_fields = 0
            allow_counter = 0
            allowed_name = dev.get("name", None)
            allowed_addr = dev.get("address", None)
            if allowed_name is None and allowed_addr is None:
                continue
            if allowed_name is not None and name == allowed_name:
                allow_fields += 1
                allow_counter += 1
            if allowed_addr is not None and name == allowed_name:
                allow_fields += 1
                allow_counter += 1
            if allow_counter > 0 and allow_fields == allow_counter:
                if under_lock():
                    unlock(allowed_name, allowed_addr)
                    logger.debug("Waiting {} seconds before return to the loop".format(unlock_delay))
                    time.sleep(unlock_delay)
                    if under_lock():
                        logger.error("It was not possible to unlock the system")
                    else:
                        logger.info("System unlocked successfully")
                else:
                    logger.debug("System already unlocked")
    return

def unlock(name, addr):
    logger.info("Unlocking with device {} - {}".format(name, addr))
    username = user_credentials.get("user","")
    decrypted_password = decode(user_credentials.get("password",""))
    
    subprocess.call("""caffeinate -u -t 1""", shell=True)
    subprocess.call("""osascript -e 'tell application "System Events" to key code 123'""", shell=True)
    subprocess.call("""osascript -e 'tell application "System Events" to keystroke "a" using {command down}'""", shell=True)
    subprocess.call("""osascript -e 'tell application "System Events" to keystroke "%s"'""" % decrypted_password, shell=True)
    subprocess.call("""osascript -e 'tell application "System Events" to keystroke return'""", shell=True)

    logger.debug("Unlock done")


def lock_devices(unlock_dev):
    for dev in allowed_devices:
        allow_counter = 0
        allowed_name = unlock_dev[0]
        allowed_addr = unlock_dev[1]
        if allowed_name is None and allowed_addr is None:
            continue
        if allowed_name is not None and name == allowed_name:
            allow_counter += 1
            break
        if allowed_addr is not None and name == allowed_name:
            allow_counter += 1
            break
    if allow_counter == 0:
        if not under_lock():
            logger.debug("Unlock device no longer in range, locking ...")
            subprocess.call("""pmset displaysleepnow""", shell=True)
            logger.debug("Lock done")
    else:
        logger.debug("Unlock device still in range")

def under_lock():
    session_dict=Quartz.CGSessionCopyCurrentDictionary()
    lock_status = session_dict.get("CGSSessionScreenIsLocked", 0) != 0
    #logger.debug("Lock status: {}".format(lock_status))
    return lock_status


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.debug("Starting unlocker")
    unlock_dev = (None,None)
    while True:
        if under_lock():
            devices = get_devices()
            if devices is not None:
                unlock_dev = unlock_devices(devices)
        else:
            if lock_allowed is True:
                devices = get_devices()
                if devices is not None:
                    lock_devices(unlock_dev)
        time.sleep(.10)
