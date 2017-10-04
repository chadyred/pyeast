#!/usr/bin/python3

from pyeast import *

import attr

if __name__ == '__main__':
    Naviguate().format('google-chrome', '/foo/bar')
    Naviguate().simple_browser('firefox', 'http://rhcpfrance.com/pwette')
    Naviguate().browse('google-chrome', 'google.com/foo/bar')
    Naviguate().browse('google-chrome', 'rhcpfrance.com')
    Naviguate().browse('google-chrome', 'twitter.com')
    Naviguate().browse('firefox', 'facebook.com')
