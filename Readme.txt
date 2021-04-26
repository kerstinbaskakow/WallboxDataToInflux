Both files should be executed by cronjob
0-59/2 * * * * python3 /<yourdir>/WallboxDataToInflux/setWallboxChargeMode.py
1-59/2 * * * * python3 /<yourdir>/WallboxDataToInflux/readWallboxValues.py
Be aware that the may not run at the same time. In this case setting or reading
will not work
