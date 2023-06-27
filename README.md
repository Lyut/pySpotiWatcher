# pySpotiWatcher
Prints to terminal what you're listening to from Spotify and keeps track of it from an experimental dashboard!

# Requirements
  * frida (it spawns the Spotify process and then hooks functions that handle track lifecycle)
  * catimg (to print the image output)
    
# Configuring the webserver
On the back-end (pyspotiwatch-be), make sure to change the application.properties file to include your MongoDB configuration.

`spring.data.mongodb.host=localhost
spring.data.mongodb.port=27017
spring.data.mongodb.database=spotify`

Run the back-end.

On the front-end, run `npm install` then edit environment.ts to reflect your back-end configuration.

If everything went correctly, visiting http://localhost:4200 should show something like this:

<img src="https://i.imgur.com/6U32rrv.png">

This has been tested on Spotify version 1.2.11.916.geb595a67, although the Spotify package must be compiled by yourself as I'm afraid it doesn't work if installed through snapd.

Other versions could/could not work.

<img src="https://i.imgur.com/zdKTn8R.png">
