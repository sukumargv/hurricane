#!/usr/bin/python3

import threading
from datetime import datetime
import urllib.request

BASE_PATH = '/Users/sukumargv/bc_ferries/'


def get_page(page_url, local_fname):
    d = datetime.now()
    fname = d.strftime("{}/{}".format(BASE_PATH, local_fname))
    urllib.request.urlretrieve(page_url, fname)

"""
http://orca.bcferries.com:8080/cc/settings/includes/maps/route0.html
http://orca.bcferries.com:8080/cc/settings/includes/maps/route1.html
http://orca.bcferries.com:8080/cc/settings/includes/maps/route2.html
http://orca.bcferries.com:8080/cc/settings/includes/maps/route3.html
http://orca.bcferries.com:8080/cc/settings/includes/maps/route4.html
http://orca.bcferries.com:8080/cc/settings/includes/maps/route5.html
http://orca.bcferries.com:8080/cc/settings/includes/maps/route6.html
http://orca.bcferries.com:8080/cc/settings/includes/maps/route7.html
http://bcferries.applocation.net/routemaps/route13.html
http://bcferries.applocation.net/routemaps/route16.html
http://bcferries.applocation.net/routemaps/route17.html
http://bcferries.applocation.net/routemaps/route18.html
http://bcferries.applocation.net/routemaps/route19.html
http://bcferries.applocation.net/routemaps/route20.html
http://bcferries.applocation.net/routemaps/route21.html
http://bcferries.applocation.net/routemaps/route22.html
http://bcferries.applocation.net/routemaps/route23.html
http://bcferries.applocation.net/routemaps/route24.html
http://bcferries.applocation.net/routemaps/route25.html
http://bcferries.applocation.net/routemaps/route29.html
"""


def get_all():
    base_url = "http://bcferries.applocation.net/routemaps/route{}.html"
    routes = [0,1,2,3,4,5,6,7,13,16,17,18,19,20,21,22,23,24,25,29]

    for route in routes:
        url = base_url.format(route)
        fname = "r{:02d}-%Y-%m-%d_%H-%M-%S.html".format(route)
        thread = threading.Thread(target=get_page, args=(url, fname))
        thread.start()
        # get_page(url, fname)

    thread = threading.Thread(target=get_page, args=("http://orca.bcferries.com:8080/cc/marqui/actualDepartures.asp",
                                                     "s-%Y-%m-%d_%H-%M-%S.html"))
    thread.start()

    thread = threading.Thread(target=get_page, args=("http://orca.bcferries.com:8080/cc/marqui/at-a-glance.asp",
             "i-%Y-%m-%d_%H-%M-%S.html"))
    thread.start()
                            
                
    # get_page("http://orca.bcferries.com:8080/cc/marqui/actualDepartures.asp",
    #          "s-%Y-%m-%d_%H-%M-%S.html")
    # get_page("http://orca.bcferries.com:8080/cc/marqui/at-a-glance.asp",
    #          "i-%Y-%m-%d_%H-%M-%S.html")
        
if __name__ == '__main__':
    get_all()
