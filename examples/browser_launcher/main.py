#!/usr/local/bin/python3

from pyeast import *
from messager import *
from crawler import *

import attr

if __name__ == '__main__':
    # Naviguate().format('google-chrome', '/foo/bar')
    Naviguate().simple_browser('firefox', 'http://rhcpfrance.com')
    # Naviguate().simple_browser('firefox', 'http://bit.ly/')
    # Naviguate().simple_browser('firefox', 'http://doodle.com/pwette')
    # Naviguate().browse('google-chrome', 'google.com/foo/bar')
    # Naviguate().browse('google-chrome', 'rhcpfrance.com')
    # Naviguate().browse('google-chrome', 'twitter.com')
    # Naviguate().browse('firefox', 'facebook.com')
    # Naviguate().parse_body('http://google.com')
    # Naviguate().crawle_body('http://rhcpfrance.com')
    # Naviguate().crawle_body('https://giphy.com')
    # Naviguate().crawle_body_dataframe('https://rhcpfrance.com')
    # Naviguate().crawle_body_dataframe('https://giphy.com')
