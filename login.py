#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Roll my own "template system".
"""
import os
import cgi
import cgitb
from templates import login_page, secret_page
from http.cookies import SimpleCookie

from secret import username, password

COOKIE_KEY_USER = "username"
COOKIE_KEY_PASS = "password"
cgitb.enable()


class AuthError(Exception):
    pass


def endpoint():
    method = get_method()
    if method == "GET":
        handle_get()
    elif method == "POST":
        handle_post()


def handle_get():
    cookie = SimpleCookie()
    cookie_str = os.environ.get("HTTP_COOKIE", "")

    print(f"Content-Type: text/html")
    print()

    cookie.load(cookie_str)
    if cookie.get(COOKIE_KEY_USER) and \
       cookie.get(COOKIE_KEY_USER).value == username and \
       cookie.get(COOKIE_KEY_PASS) and \
       cookie.get(COOKIE_KEY_PASS).value == password:
        print(secret_page(username=username, password=password))
    else:
        print(login_page())


def handle_post():
    print(f"Content-Type: text/html")

    form = cgi.FieldStorage()
    if username != form.getvalue('username') or password != form.getvalue('password'):
        print("Status: 403 Not Authorized")
        print()
        return

    print(f"Set-Cookie:{COOKIE_KEY_USER} = {username};")
    print(f"Set-Cookie:{COOKIE_KEY_PASS} = {password};")

    print()  # ----------- body
    print("<h1>congrats, you logged in</h1>")
    for key in form.keys():
        print(f"<h2>{key}: {form[key].value}</h2>")


def get_method():
    return os.environ.get("REQUEST_METHOD")


endpoint()
