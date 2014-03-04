#!/bin/bash
adb remount
adb push special-powers\@mozilla.org /system/b2g/distribution/bundles/special-powers\@mozilla.org
adb push marionette\@mozilla.org /system/b2g/distribution/bundles/marionette\@mozilla.org
adb shell stop b2g
adb shell start b2g
echo "waiting for b2g to start"
TRIES=30
while [ $TRIES -gt 0 ]; do
  sleep 5
  echo "checking if b2g has started"
  adb shell b2g-ps | grep b2g
  if [ $? == 0 ]; then
    break
  fi
  let TRIES=TRIES-1
done
if [ $TRIES == 0 ]; then
  echo "b2g did not start up!"
  exit 1
fi
