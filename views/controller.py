# -*- coding: utf-8 -*-

from flask import Flask, request, abort, Blueprint, jsonify, abort, redirect
import signal
import os
import subprocess
import time
from extensions import redisdb0, redisdb1
cache_server = 'http://cache.rad.fpt.vn/'


ctl = Blueprint('ctl', __name__, url_prefix='/get_file')
@ctl.route('/', defaults={'path': ''},methods=['GET'])
@ctl.route('//<path:object>', methods=['GET'])
@ctl.route('/<path:object>', methods=['GET'])
def get_file(object):
    if not object:
        return 'please insert the file name' 
    else:
        object_name = str(request.path).replace('/get_file/','')
    request_url =  'http://10.20.10.19/v1/AUTH_admin/rad_file/' + object_name
    ##manipulate a download-request to the swift proxy
    p = subprocess.Popen(['curl', '--silent', '-k', '-v','-H', 'X-Auth-Token: AUTH_tkd9290c53a5d4462e808d3b397260f779', request_url, '-X', 'GET'],stdout=subprocess.PIPE, preexec_fn=os.setsid)
    def retry(max_retry=5):
        retry_count = 0
        result = None
        while retry_count < max_retry:
             result = redisdb0.get(str(object_name).strip())
             if result:
                 os.killpg(p.pid, signal.SIGTERM)
                 break
             ##We do not know when the proxy finish saving  the real path to redis. So we have to wait and retry many time until we get the result.
             time.sleep(0.1)
             retry_count += 1
        return result

    result = retry(max_retry=10)
    if result:
        real_path = result.split('/')[3:]
        node_ip = result.split('/')[2]
        real_path_without_node_ip = '/'.join(real_path)
        if redisdb1.get(real_path_without_node_ip):
            num_request = int(redisdb1.get(real_path_without_node_ip))
        else:
            num_request = 0  
             #request/hour < 3, donot cache
        if num_request < 3:
             if num_request == 0:               
                 num_request += 1
                 #we set the expire only on the first time
                 redisdb1.setex(real_path_without_node_ip, num_request, 3600)
             else:
                 redisdb1.incr(real_path_without_node_ip, amount=1)
             return redirect(result, code=302)
             #request/hour >= 3, return the cache path
        elif num_request >= 3:
            num_request += 1
            redisdb1.incr(real_path_without_node_ip, amount=1)
            cache_path = cache_server +  real_path_without_node_ip + '?node_ip=' + node_ip
            return redirect(cache_path, code=302)
        return redirect(result, code=302)    
    return "404 or failed"


