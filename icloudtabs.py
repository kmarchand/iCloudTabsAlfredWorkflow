#!/usr/bin/python
#
# Alfred2 workflow for listing iCloud tabs
#

import os
import subprocess
import shutil
import tempfile
import plistlib
import xml.etree.ElementTree as ET


def create_temporary_copy(path):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'safari_sync_plist_copy.plist')
    shutil.copy2(os.path.expanduser(path), temp_path)
    return temp_path


# make a temp copy of the plist file

temp_plist = create_temporary_copy(
    '~/Library/SyncedPreferences/com.apple.Safari.plist')

# Use plutil to convert binary plist to xml

os.system('plutil -convert xml1 %s' % temp_plist)


# Use plistlib to convert plist XML to a dictionary

info = plistlib.readPlist(temp_plist)

# Clean up (delete) temp file

os.remove(temp_plist)

# Pull out the device elements from the info dict for easier parsing later

devicetabs = []

for uid in info['values'].values():
    try:
        devicetabs.append([uid['value']['DeviceName'], uid['value']['Tabs']])
    except:
        pass

# Get local machine's host and computer names to exclude both from the list

hostname_proc = subprocess.Popen(['scutil --get LocalHostName'], stdout=subprocess.PIPE, shell=True)
(hostname_out, hostname_err) = hostname_proc.communicate()
hostname = hostname_out.strip()

computername_proc = subprocess.Popen(['scutil --get ComputerName'], stdout=subprocess.PIPE, shell=True)
(computername_out, computername_err) = computername_proc.communicate()
computername = computername_out.strip()

# Generate Alfred's XML

root = ET.Element('items')

for device in devicetabs:

    device_name = device[0]

    if device_name not in [hostname, computername.decode("utf-8")]:

        for tab in device[1]:

            item = ET.SubElement(root, 'item')
            item.set('uid', tab['URL'])
            item.set('arg', tab['URL'])

            title = ET.SubElement(item, 'title')
            title.text = tab['Title']

            subtitle = ET.SubElement(item, 'subtitle')
            subtitle.text = 'iCloud Device: '+device_name

            icon = ET.SubElement(item, 'icon')
            icon.set('type', 'fileicon')
            icon.text = '/Applications/Safari.app'

print ET.tostring(root)
