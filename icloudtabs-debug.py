#!/usr/bin/python
#
# Alfred2 workflow for listing iCloud tabs
#

try:
	import os
	import subprocess
	import shutil
	import tempfile
	import plistlib
	import xml.etree.ElementTree as ET
except:
	print "ERROR: Problem importing modules"


def create_temporary_copy(path):
    try:
	    temp_dir = tempfile.gettempdir()
	    temp_path = os.path.join(temp_dir, 'safari_sync_plist_copy.plist')
	    shutil.copy2(os.path.expanduser(path), temp_path)
	    print "STATUS: Temp path created ok: %s" % temp_path
	    return temp_path
    except:
    	print "ERROR: Problem creating temp path"


# make a temp copy of the plist file

try:
	temp_plist = create_temporary_copy(
    	'~/Library/SyncedPreferences/com.apple.Safari.plist')
	print "STATUS: com.apple.Safari.plist found ok"
except:
	print "ERROR: Could not parse com.apple.Safari.plist"

# Use plutil to convert binary plist to xml

try:
	os.system('plutil -convert xml1 %s' % temp_plist)
	print "STATUS: plutil converted plist to XML ok"
except:
	print "ERROR: Could not convert com.apple.Safari.plist to XML"


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

print '\n'

hostname_proc = subprocess.Popen(
    ['scutil --get LocalHostName'], stdout=subprocess.PIPE, shell=True)
(hostname_out, hostname_err) = hostname_proc.communicate()
hostname = hostname_out.strip()

print "HostName = %s" % hostname

computername_proc = subprocess.Popen(
    ['scutil --get ComputerName'], stdout=subprocess.PIPE, shell=True)
(computername_out, computername_err) = computername_proc.communicate()
computername = computername_out.strip()

print "ComputerName = %s" % computername

# Generate Alfred's XML

print '\n'

root = ET.Element('items')

for device in devicetabs:

    device_name = device[0]

    print "Device: %s, Tab Count: %s" % (device_name, len(device[1]))

    if device_name not in [hostname, computername.decode("utf-8")]:

        for tab in device[1]:

            #if '{query}'.lower() not in tab['Title'].lower():
            #    continue

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


    else:

    	print "\n"
    	print "%s is local device; tabs excluded from results\n\n" % device_name

# print ET.tostring(root)
