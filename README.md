# iCloudTabs AlfredWorkflow

This workflow retrieves iCloud tabs from the local `~/Library/Safari/CloudTabs.db` database for all connected iCloud devices and displays the links.  Tabs from current device are excluded.

**NOTE**:  For support in macOS 10.12 Sierra or newer, `~/Library/Safari/CloudTabs.db` is used rather than the previous method of using `~/Library/SyncedPreferences/com.apple.Safari.plist` since that plist is now encrypted.  I only tested on macOS 10.13 High Sierra and have limited resource for testing on any other version of macOS.


## Usage

* `tabs` keyword for showing list of tabs with device indicated.
* `alltabs` keyword to open all tabs at once
* `tabdump` keyword to dump all tabs as date-stamped markdown file to desktop.

## Changes

* **2013-09-05**: Updated to work when devices in the plist file don't have any tabs.
* **2013-10-25**: Added `alltabs` for opening all links from all devices at once.
* **2014-02-02**: Added `tabdump` to export a markdown file on the desktop with all tabs from all devices.
* **2014-03-06**: Added filtering with optional keyword (thanks Felipe Manoeli!).
* **2014-03-07**: Tabdump no longer requires the non-default mechanize library to fetch page titles.
* **2017-11-11**: Updated to use CloudTabs.db rather than com.apple.Safari.plist for support in macOS 10.12 and later.  Also no longer fetching page titles for `tabdump` since already available locally, so much faster Markdown export.
