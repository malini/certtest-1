adb remount
adb push marionette\@mozilla.org /system/b2g/distribution/bundles/marionette\@mozilla.org
adb shell stop b2g
adb shell start b2g
