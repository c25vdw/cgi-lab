#!/usr/bin/env python3

import os
import cgi
import json

def print_content_type(type="text/html"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Content-Type: {type}")
            print()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@print_content_type("application/json")
def q1():
    print(json.dumps(dict(os.environ), indent=4))

@print_content_type()
def q2():
    print(f"<h2>query strings are: {os.environ.get('QUERY_STRING', {})}</h2>")

@print_content_type()
def q3():
    print(f"<h2>user agent is: {os.environ.get('HTTP_USER_AGENT', {})}</h2>")

q1()