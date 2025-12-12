# Command line interface server implementation (stdin for requests, stdout for results)
# Allows accessing gsemgr with an HTTP API

# GSE Proprietary Software License
# Copyright (c) 2025 Global Satellite Engineering, LLC. All rights reserved.
# This software and associated documentation files (the "Software") are the proprietary and confidential information of Global Satellite Engineering, LLC ("GSE"). The Software is provided solely for the purpose of operating applications distributed by GSE and is subject to the following conditions:

# 1. NO RIGHTS GRANTED: This license does not grant any rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell the Software.
# 2. RESTRICTED ACCESS: You may only access the Software as part of a GSE application package and only to the extent necessary for operation of that application package.
# 3. PROHIBITION ON REVERSE ENGINEERING: You may not reverse engineer, decompile, disassemble, or attempt to derive the source code of the Software.
# 4. PROPRIETARY NOTICES: You must retain all copyright, patent, trademark, and attribution notices present in the Software.
# 5. NO WARRANTIES: The Software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement.
# 6. LIMITATION OF LIABILITY: In no event shall GSE be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the Software or the use or other dealings in the Software.
# 7. TERMINATION: This license will terminate automatically if you fail to comply with any of the terms and conditions of this license. Upon termination, you must destroy all copies of the Software in your possession.

# THE SOFTWARE IS PROTECTED BY UNITED STATES COPYRIGHT LAW AND INTERNATIONAL TREATY. UNAUTHORIZED REPRODUCTION OR DISTRIBUTION IS SUBJECT TO CIVIL AND CRIMINAL PENALTIES.

from . import vfs
from . import common
from gse_gsatmicro_utils import utils
from gse_gsatmicro_utils import ser_driver
import json
import sys
import base64
import threading
import queue
import time

#######################################################################################################################
# Local function and data

# httpd logger
logger = utils.Logger("cond")
# Request queue
req_q = queue.Queue()
# stdout/stderr lock
con_lock = threading.Lock()

# Terminal emulator
class TerminalEmulator:
    def __init__(self, kind):
        self.kind = kind # port type (console or logs)
        self.ser = None # serial driver instance (None if the serial emulator is not running)
        self.thread = None # serial reader thread
        self.name = None # emulator port name
        self.sernum = None # device serial number (as given by the user)

    # Set the device serial number
    def set_sernum(self, sernum):
        self.sernum = sernum

    # Detect the terminal serial port
    # Nake sure that all ports can be detected correctly
    def detect_port(self):
        detected = common.get_detected_ports(self.sernum)
        if not detected:
            utils.fatal("Unable to detect serial ports")
        elif len(detected) > 1:
            utils.fatal("Found multiple devices, consider using --sernum")
        else:
            sernum = list(detected.keys())[0]
            detected = detected[sernum]
            if len(detected) != 3:
                utils.fatal("Not all serial ports are available, aborting")
            self.name = detected[self.kind]

    # Serial reader thread function
    def ser_read_thread(self, ser, q):
        tag = "term" if self.kind == "console" else "logs"
        while True:
            try:
                if (d := ser.read_cnt(1024, timeout=0.001)):
                    q.put((tag, d))
            except:
                q.put((tag, None))
                break

    # Start terminal emulator
    # Returns True for success or False for error
    def start(self, fs, req, logger):
        if self.thread == None:
            assert self.ser == None
            try:
                self.detect_port()
                self.ser = ser_driver.SerialHandler(self.name, 115200, echo_rx=False, echo_tx=False)
                self.ser.init()
                self.thread = threading.Thread(target=self.ser_read_thread, args=(self.ser, req_q), daemon=True)
                self.thread.start()
                logger.info(f"Started {self.kind} terminal emulator")
            except:
                logger.error(f"Unable to start {self.kind} terminal emulator")
                if self.ser != None:
                    self.ser.exit()
                    self.ser = None
        return self.thread != None

    # Stop terminal emulator
    # Returns True for success or False for error
    def stop(self, fs, req, logger):
        if self.thread != None:
            assert self.ser != None
            # Close the serial port, this will force the thread to exit
            try:
                self.ser.exit()
                self.ser = None
                wait_cnt = 0
                while self.thread.is_alive():
                    wait_cnt += 1
                    if wait_cnt >= 50: # don't wait mroe than 5 seconds for the thread
                        logger.error(f"Unable to stop {self.kind} terminal emulator thread")
                        break
                    time.sleep(0.1)
                if not self.thread.is_alive():
                    logger.info(f"Stopped {self.kind} terminal emulator")
                self.thread = None
            except:
                logger.error(f"Unable to stop {self.kind} terminal emulator")
                if self.ser != None:
                    self.ser.exit()
                    self.ser = None
        return self.thread == None

    # Called when new data was received
    def new_data(self, data):
        if self.ser != None:
            try:
                self.ser.write(base64.b64decode(data))
                self.ser.flush_output()
            except:
                logger.warning("Error sending data to board")

te_con = TerminalEmulator("console") # console termintal emulator instance
te_logs = TerminalEmulator("logs") # logs terminal emulator instance

# Mapping between the acstion in a request and the correponding handler
act_map = {
    "fs_list": common.fs_list,
    "fs_stat": common.fs_stat,
    "fs_kind": common.fs_kind,
    "fs_get": lambda fs, req, logger: base64.b64encode(common.fs_get(fs, req, logger)).decode("ascii"),
    "fs_create": common.fs_create,
    "fs_remove": common.fs_remove,
    "fs_put": lambda fs, req, logger: common.fs_put(fs, req, logger, b64=True),
    "version": common.cmd_version,
    "reset": common.cmd_reset,
    "run": common.cmd_run_code,
    "term_start": te_con.start,
    "term_stop": te_con.stop,
    "logs_start": te_logs.start,
    "logs_stop": te_logs.stop,
}

# Write the given data to stdout after obtaining the console stdout/stderr lock
def write_locked(*args):
    con_lock.acquire()
    try:
        for a in args:
            sys.stdout.write(a)
        sys.stdout.flush()
    finally:
        con_lock.release()

# Send an "invalid request" response
def invalid(req_id, data="invalid request"):
    write_locked(json.dumps({"id": req_id, "err": data}), "\r\n")

# Call the given function with the given arguments
# If an exception is raised, catch it and return an invalid request rerpose
def req_wrap(req_id, f, *args, **kwargs):
    try:
        if (res := f(*args, **kwargs)) == None:
            res = True
        res = {"id": req_id, "res": res}
    except Exception as e:
        res = {"id": req_id, "err": str(e)}
    return json.dumps(res)

# Console thread: read a line from stdin and save it to the request queue
def stdin_read_thread(q):
    while True:
        try:
            q.put(("stdin", input("")))
        except:
            q.put(("stdin", None))
            break

# Return a request dictionary that is suitable to use for the function in common.py
# In this case, this means that the "act" and "id" keys should be removed, since they are specific to the con server
def fix_req(r):
    return {k: v for k, v in r.items() if not k in ("act", "id")}

#######################################################################################################################
# Commands

# 'cond' command handler
def cmd_cond(ser, args):
    te_con.set_sernum(args.sernum)
    te_logs.set_sernum(args.sernum)
    # Synchronize all stdout/stderr writes
    utils.set_logs_con_lock(con_lock)
    # Get filesystem instance
    fs = vfs.get_vfs()
    # Start console read thread
    threading.Thread(target=stdin_read_thread, args=(req_q, ), daemon=True).start()
    # Start terminal server if needed
    if args.start_term:
        if not te_con.start(fs, None, logger):
            utils.fatal("Unable to start terminal server")
    # Start logs server if needed
    if args.start_logs:
        if not te_logs.start(fs, None, logger):
            utils.fatal("Unable to start logs server")

    # The server loop runs here
    logger.info("Starting console server")
    while True:
        try:
            (src, req) = req_q.get()
            if src == "stdin":
                if req == None: # CTRL+C in stdin thread
                    break
                # Read a single request which should be valid JSON
                try:
                    req = json.loads(req)
                except:
                    logger.error(f"Received invalid reqeust")
                    invalid(-1)
                    continue
                # THe request must be a dictionary
                if not isinstance(req, dict):
                    logger.error("Invalid request type")
                    invalid(-1)
                    continue
                # Terminal data has its own simple format with only "term" expected as a key in the dictionary
                if ("term" in req) and (len(req) == 1):
                    te_con.new_data(req["term"])
                    continue # there is no response for this request
                # The request should have an "act" key (action) and an "id"
                if  (not "act" in req) or (not "id" in req):
                    logger.error("Required key(s) 'act' and/or 'id' not found in request")
                    invalid(-1)
                    continue
                # Check action
                if (act := req["act"]) == "exit": # server must terminate
                    break
                elif not act in act_map: # unknown action
                    logger.error(f"Unknown action {act} in request")
                    invalid(req["id"])
                    continue
                else: # action found, execute its handler
                    res = req_wrap(req["id"], act_map[act], fs, fix_req(req), logger)
                    write_locked(res, "\r\n")
                    if act == "reset": # automatically exit on reset
                        break
            elif src == "term": # terminal data from board
                if req != None:
                    write_locked(json.dumps({"term": base64.b64encode(req).decode("ascii")}), "\r\n")
                else:
                    logger.warning("Console terminal emulator thread error")
                    te_con.stop(fs, req, logger)
            elif src == "logs": # logs data from board
                if req != None:
                    write_locked(json.dumps({"logs": base64.b64encode(req).decode("ascii")}), "\r\n")
                else:
                    logger.warning("Logs terminal emulator thread error")
                    te_logs.stop(fs, req, logger)
        except KeyboardInterrupt:
            break
    logger.info("Server exited")

# 'cond' argument checks
def cond_check_args(args):
    if args.port:
        utils.fatal("The console server can't be used with the --port option")

# 'cond' extra arguments
def cond_args(parser):
    parser.add_argument("--start-term", help="Start terminal server", action="store_true", default=False)
    parser.add_argument("--start-logs", help="Start logs server", action="store_true", default=False)