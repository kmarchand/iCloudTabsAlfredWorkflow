#!/usr/bin/python
#
# Alfred2 workflow for listing iCloud tabs
#

import os
import subprocess
import shutil
from datetime import datetime
import urllib2
import re
import getpass
import sqlite3


local_user = getpass.getuser()
cloudtabs_db = '/Users/%s/Library/Safari/CloudTabs.db' % local_user

conn = sqlite3.connect(cloudtabs_db)
cursor = conn.cursor()

cursor.execute("select device_uuid, device_name from cloud_tab_devices")
cloud_tab_devices = cursor.fetchall()

# Structure of cloud_tab_devices:
#
# [
#     (device1_uuid, device1_name),
#     (device2_uuid, device2_name)
# ]

cloud_tab_devices_lookup = {}

for device in cloud_tab_devices:
        cloud_tab_devices_lookup[device[0]] = device[1]

cloud_tab_devices_uuid_list = []

for device in cloud_tab_devices:
        cloud_tab_devices_uuid_list.append(device[0])

cursor.execute("select device_uuid, title, url from cloud_tabs")
cloud_tabs = cursor.fetchall()

# Structure of cloud_tabs:
#
# [
#     (device_uuid, tab_title, tab_url),
#     (device_uuid, tab_title, tab_url),
# ]

conn.close()


# Structure needed for all_device_tabs:
#
# all_device_tabs = [
#     ['device1_name', [
#         {'Title': 'device1_tab1_title', 'URL': 'device1_tab1_url'},
#         {'Title': 'device1_tab1_title', 'URL': 'device1_tab1_url'}
#     ]
#     ]
#     ['device2_name', [
#         {'Title': 'device2_tab1_title', 'URL': 'device2_tab1_url'},
#         {'Title': 'device2_tab1_title', 'URL': 'device2_tab1_url'}
#     ]
#     ]
# ]

all_device_tabs = []

for device_uuid in cloud_tab_devices_uuid_list:
    lookup_name = cloud_tab_devices_lookup[device_uuid]
    device_tabs = []
    for tab in cloud_tabs:
        if tab[0] == device_uuid:
            tabinfo = {'Title': tab[1], 'URL': tab[2]}
            device_tabs.append(tabinfo)
    all_device_tabs.append([lookup_name, device_tabs])


# Create a Markdown file listing all the tabs from all devices

# Change date format so the resulting filename is compatible with Windows and Dropbox sync
# see https://www.dropbox.com/en/help/145


outfile = os.path.expanduser(
    '~/Desktop/alltabs_%s.md' % datetime.now().strftime('%Y-%m-%d %H.%M.%S'))	


outtext = '''
## iCloud Tab Listing - %s

Links from all devices:

''' % datetime.now().isoformat()[:19]


for device in all_device_tabs:
    outtext += '### %s\n\n' % device[0]
    for tab in device[1]:
        outtext += '* [%s](%s)\n' % (tab['Title'].replace("[", "/[").replace("]", "/]"), tab['URL'])
    outtext += '\n'

with open(outfile, 'w') as f:
    f.write(outtext.encode('utf8'))

# Un-comment this if you want it to auto-open in Marked 2 (http://marked2app.com)
# os.system('open -a "Marked 2" %s' % outfile)