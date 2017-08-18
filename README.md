# iCloudTabs AlfredWorkflow

This workflow retrieves iCloud tabs from the local `~/Library/SyncedPreferences/com.apple.Safari.plist` file for all connected iCloud devices and displays the links.  Tabs from current device are excluded.

**NOTE**:  This doesn't work in macOS 10.12 Sierra or newer since the contents of com.apple.Safari.plist are now encrypted.


## Usage

* `tabs` keyword for showing list of tabs with device indicated.
* `alltabs` keyword to open all tabs at once.
* `tabdump` keyword to dump all tabs as date-stamped markdown file to desktop.

## Changes

* September 5 2013; updated to work when devices in the plist file don't have any tabs.
* October 25 2013; added `alltabs` for opening all links from all devices at once.
* February 2 2014; added `tabdump` to export a markdown file on the desktop with all tabs from all devices.
* March 6 2014; added filtering with optional keyword (thanks Felipe Manoeli!).
* March 7 2014; tabdump no longer requires the non-default mechanize library to fetch page titles.
