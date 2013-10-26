# iCloudTabs AlfredWorkflow

This workflow retrieves iCloud tabs from the local `~/Library/SyncedPreferences/com.apple.Safari.plist` file for all connected iCloud devices and displays the links.  Tabs from current device are excluded.

## Usage

* `tabs` keyword for showing list of tabs with device indicated.
* `alltabs` keyword to open all tabs at once.

## Changes

* September 5 2013; updated to work when devices in the plist file don't have any tabs.
* October 25 2013; added `alltabs` for opening all links from all devices at once.