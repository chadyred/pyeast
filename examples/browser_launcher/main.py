#!/usr/bin/python3

from pyeast import *
from messager import *
from crawler import *

import attr

if __name__ == '__main__':
    # Naviguate().format('google-chrome', '/foo/bar')
    # Naviguate().simple_browser('firefox', 'http://rhcpfrance.com/pwette')
    # Naviguate().simple_browser('firefox', 'http://bit.ly/')
    # Naviguate().simple_browser('firefox', 'http://doodle.com/pwette')
    # Naviguate().browse('google-chrome', 'google.com/foo/bar')
    # Naviguate().browse('google-chrome', 'rhcpfrance.com')
    # Naviguate().browse('google-chrome', 'twitter.com')
    # Naviguate().browse('firefox', 'facebook.com')
    # Naviguate().parse_body('http://google.com')
    Naviguate().crawle_body('http://google.com')
    Naviguate().crawle_body('https://giphy.com')
