#!/usr/bin/env python

from twitter import twitter_stat
from flask import Flask, jsonify

ts = twitter_stat()
app = Flask('ethostat')

import json
from functools import wraps
from flask import redirect, request, current_app
 
def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args,**kwargs).data) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function
 
@app.route('/query', methods=['GET'])
@support_jsonp
def twitter_term_temperature():
    keyword = request.args.get('keyword', None)
    if keyword is not None:
        temperature = ts.get_temperature(keyword)
        return jsonify({ keyword : temperature })
    else:
        return ''

if __name__ == "__main__":
    app.run(debug=True)