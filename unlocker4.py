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

import bluetooth
import os
import sys
import subprocess
import time
import Quartz
import logging
import logging.config
from genkey import decode

logging.config.fileConfig('logging.conf')
logger = None

allowed_devices = [
    {"name": "<your device name>",
     "addr": b"<your device address>"},
]

lock_allowed = False

user_credentials = {
    "user": "<your username (unused)>",
    "password": b"<your encrypted password (see genkey.py code)>",
}

unlock_delay = 10

def get_devices():
    addr = name = None

    logger.debug("Discovering devices ...")
    nearby_devices = bluetooth.discover_devices(duration=1,
                                                lookup_names=True,
                                                flush_cache=True)
    return nearby_devices 


def unlock_devices(nearby_devices):
    if nearby_devices is not None:
        logger.debug("Found {} devices".format(len(nearby_devices)))
        
        for addr, name in nearby_devices:
            try:
                logger.debug("   {} - {}".format(addr, name))
            except UnicodeEncodeError:
                logger.debug("   {} - {}".format(addr, name.encode("utf-8", "replace")))
            
            for dev in allowed_devices:
                allow_fields = 0
                allow_counter = 0
                allowed_name = dev.get("name", None)
                allowed_addr = dev.get("addr", None)
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
                    else:
                        logger.debug("already unlocked")
                    return
    else:
        logger.debug("No devices found")

def unlock(name, addr):
    logger.info("Unlocking with device {} - {}".format(name, addr))
    username = user_credentials.get("user","")
    decrypted_password = decode(user_credentials.get("password",""))
    
    subprocess.call("""caffeinate -u -t 1""", shell=True)
    subprocess.call("""osascript -e 'tell application "System Events" to key code 123'""", shell=True)
    #for i in range(0, 128):
    #    subprocess.call("""osascript -e 'tell application "System Events" to key code 48'""", shell=True)
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
        devices = get_devices()
        if under_lock():
            unlock_dev = unlock_devices(devices)
        else:
            if lock_allowed is True:
                lock_devices(unlock_dev)
        time.sleep(.10)
            


