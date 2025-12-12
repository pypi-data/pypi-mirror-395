# HTTP (REST) server implementation
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

from flask import Flask, request, jsonify, abort, send_file
from . import vfs
import traceback
from markupsafe import escape
import io
import os
from gse_gsatmicro_utils import utils
from . import common
import posixpath as pp

#######################################################################################################################
# Local function and data

# Flask app instance
app = Flask("gse_httpd")
# FS instance
fs = None
# API version
api_version = "2.0"
# httpd logger
logger = utils.Logger("httpd")

# Error template to be rendered when an exception occurs
err_template = """
<html>
<head><title>Internal server error</title></head>
<body>
<h1>Internal server error</h1>
<code>
{error}
</code></body></html>
"""

# Bad request template to be rendered when a bad request occurs
bad_request_template = """
<html>
<head><title>Bad request</title></head>
<body>
{error}
</body></html>
"""

# Return the exception information as HTML formatted code
def get_exc_data():
    exc_info = traceback.format_exc()
    return "<br>\n".join([escape(e) for e in exc_info.split("\n")])

# Ensure that the given request has a "json" attribute and return its value if it does
# Raise an "invalid request" error otherwise
def ensure_json(request):
    if (res := getattr(request, "json", None)) == None:
        logger.error("'json' attribute not found in request")
        abort(400, "invalid request")
    return res

# Wrap the function in a try/catch block and check the known exceptions
def exc_check(func):
    def wrapper(*args, **kwargs):
        try:
            # Transform "None" results to True, this lets the called know that the request succeeded, even if it didn't
            # return any data.
            if (res := func(*args, **kwargs)) == None:
                res = True
            return jsonify({"res": res})
        except vfs.VFSError as e: # catch errors from the VFS implementation
            logger.error("VFS error: {}".format(str(e)))
            return jsonify({"err": escape(str(e))})
        except common.InvalidRequest:
            logger.error("Invalid request")
            abort(400, "invalid request")
        except common.PathNotFound as e:
            logger.error(f"Path {e.path} not found")
            abort(404)
        except common.RequestError as e:
            logger.error("Request error: {}".format(str(e)))
            return jsonify({"err": escape(str(e))})
        except Exception: # other exceptions all reported as internal server errors
            ed = get_exc_data()
            logger.error("exc_check exception: {}".format(ed))
            abort(500, ed)
    wrapper.__name__ = func.__name__
    return wrapper

# Same as abovve, but skip the JSON step
def exc_check_no_json(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except common.InvalidRequest:
            logger.error("Invalid request")
            abort(400, "invalid request")
        except common.PathNotFound as e:
            logger.error(f"Path {e.path} not found")
            abort(404)
        except Exception: # all exceptions are reported as internal server errors
            ed = get_exc_data()
            logger.error("exc_check_no_json exception: {}".format(ed))
            abort(500, ed)
    wrapper.__name__ = func.__name__
    return wrapper

# There are probably not needed, so they are commented for now
# Internal err (500) handler
#@app.errorhandler(500)
#def internal_error_handler(error):
#    return err_template.format(error=str(error)), 500

# Bad request (400) handler
#@app.errorhandler(400)
#def bad_request_handler(error):
#    return bad_request_template.format(error=str(error)), 400

######################################################################################################################
# File system requests

# List the content of the directory at "path". If "stat" is True, it also returns data about each item in the directory
# (see /fs/stat below for mode details). If not specified, "stat" defaults to False.
# Returns a dictionary where the keys are directory items and the values are stat data (emtpy if "stat" is False)
@app.route("/fs/list", methods=["POST"])
@exc_check
def fs_list():
    return common.fs_list(fs, ensure_json(request), logger)

# Return information about a file system item (file or directory).
# Returns a {"kind": "file" | "dir", "size": size, "readonly": True|False} dictionary
@app.route("/fs/stat", methods=["POST"])
@exc_check
def fs_stat():
    return common.fs_stat(fs, ensure_json(request), logger)

# Returns the kind of item ("file, "dir" or "none") that the given path points to.
# "none" means that the item does not exist
@app.route("/fs/kind", methods=["POST"])
@exc_check
def fs_kind():
    return common.fs_kind(fs, ensure_json(request), logger)

# Return the content of file at "path"
@app.route("/fs/get", methods=["POST"])
@exc_check_no_json
def fs_get():
    data = common.fs_get(fs, req := ensure_json(request), logger)
    return send_file(io.BytesIO(data), download_name=req["path"])

# Create a file or a directory at "path", depending on "kind" (which must be either "file" or "dir")
# TODO: add "overwrite"
@app.route("/fs/create", methods=["POST"])
@exc_check
def fs_create():
    return common.fs_create(fs, ensure_json(request), logger)

# Remove a file or a directory from "path", depending on "kind" (which must be either "file" or "dir")
@app.route("/fs/remove", methods=["POST"])
@exc_check
def fs_remove():
    return common.fs_remove(fs, ensure_json(request), logger)

# Save data from "file" at "path", which must exist.
# Optionally, "overwrite" can be specified to overwrite existing files (defaults to True if not specified).
# Returns True for success.
@app.route("/fs/put", methods=["POST"])
@exc_check_no_json
def fs_put():
    if not hasattr(request, "form"):
        abort(400, "'form' not found")
    common.fs_put(fs, request.form, logger)
    return jsonify({"res": True})

#######################################################################################################################
# Other endpoints

# Return API version
@app.route("/version", methods=["GET", "POST"])
@exc_check
def version():
    return common.cmd_version(fs, request, logger)

# Reset device
@app.route("/reset", methods=["GET", "POST"])
@exc_check
def reset():
    return common.cmd_reset(fs, request, logger)

# Run the code given in "func". The syntax must be "mod_name.func_name"
@app.route("/run", methods=["POST"])
@exc_check
def run_code():
    return common.cmd_run_code(fs, ensure_json(request), logger)

#######################################################################################################################
# Commands

# 'httpd' command argparse helper
def httpd_args(parser):
    parser.add_argument("--httpd-port", help="HTTP server port", type=int, default=8080)
    parser.add_argument("--httpd-bind", help="HTTP server bind address", type=str, default="127.0.0.1")

# 'httpd' command handler
def cmd_httpd(ser, args):
    global fs
    fs = vfs.get_vfs()
    app.run(host=args.httpd_bind, port=args.httpd_port, debug=args.verbose > 0, use_reloader=False)
