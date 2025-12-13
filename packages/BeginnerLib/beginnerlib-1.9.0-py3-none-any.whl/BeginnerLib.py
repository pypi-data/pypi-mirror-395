# Core utilities
import sys
import os
import pathlib
import time as t
import datetime
import random as r
import math
import functools
import itertools
import pyautogui as pya

# File and data handling
import csv
import json
import pickle
import shutil
import glob

# Networking / web
import socket
import urllib
import http
import ssl
import requests          # External: easy HTTP requests

# Text / parsing
import re
import string
import html

# Debugging / logging
import logging
import traceback
import warnings

# GUI / graphics
import tkinter
import turtle

def prt(msg):
    print(msg)

def inp(inp):
    return input(inp)

def wait(nr):
    t.sleep(nr)

def random(nr1, nr2):
    return r.randint(nr1, nr2)

def click(pos1, pos2):
    pya.moveTo(pos1, pos2)
    pya.click()