# pySpotiWatcher
Prints to terminal what you're listening to from Spotify.
Requires frida (it spawns the Spotify process and then hooks functions that handle track lifecycle) and catimg (to print the image output)

Only works on Linux, Spotify version 1.2.11.916.geb595a67, package must be compiled by yourself as I'm afraid it doesn't work if installed through snapd.

<img src="https://i.imgur.com/zdKTn8R.png">
