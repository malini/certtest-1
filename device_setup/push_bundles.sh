adb remount
adb push special-powers\@mozilla.org /system/b2g/distribution/bundles/special-powers\@mozilla.org
adb push marionette\@mozilla.org /system/b2g/distribution/bundles/marionette\@mozilla.org
adb shell stop b2g
adb shell start b2g
