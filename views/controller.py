# -*- coding: utf-8 -*-

from flask import Flask, request, abort, Blueprint, jsonify, abort, redirect
import signal
import os
import subprocess
import time
from extensions import redisdb1
#from swiftly.client import DirectClient
#client = DirectClient(swift_proxy_storage_path='/v1/AUTH_test')

ctl = Blueprint('ctl', __name__, url_prefix='/get_file')
@ctl.route('/', defaults={'path': ''},methods=['GET'])
@ctl.route('//<path:object>', methods=['GET'])
@ctl.route('/<path:object>', methods=['GET'])
def get_file(object):
    if not object:
        return 'please insert the file name' 
    else:
        object_name = str(request.path).replace('/get_file','')
    #object_name       = str(request.args.get('name')).strip()
    request_url = 'http://10.20.10.3:8080/v1/AUTH_test/rad_file/' + object_name 
    p = subprocess.Popen(['curl', '--silent', '-k', '-v', request_url, '-X', 'GET'],stdout=subprocess.PIPE, preexec_fn=os.setsid)
    #client.get_object('rad_file',object_name,stream=False)
            
    def retry(max_retry=5):
        retry_count = 0
        result = None
        while retry_count < max_retry:
             result = redisdb1.get(str(object_name).strip())
             if result:
                 os.killpg(p.pid, signal.SIGTERM)
                 break
             time.sleep(0.1)
             retry_count += 1
        return result

    result = retry(max_retry=10)
    if result:
        return redirect(result, code=302)    
    return "404 or failed"


