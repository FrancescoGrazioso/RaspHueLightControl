# RaspHueLightControl
A simple Hue light control for raspberry pi and Elegoo ir remote.

My setup:

  -Raspberry Pi Zero
  -Elegoo IR Reciver
  -Elegoo Remote

# HOW TO OBTAIN YOUR HUB IP ADDRESS AND API KEY

Step 1

First make sure your bridge is connected to your network and is functioning properly. Test that the smartphone app can control the lights on the same network.

Step 2

Then you need to discover the IP address of the bridge on your network. You can do this in a few ways.

1. Use a UPnP discovery app to find Philips hue in your network.
2. Use philips broker server discover process by visiting https://discovery.meethue.com
3. Log into your wireless router and look Philips hue up in the DHCP table.
4. Hue App method: Download the official Philips hue app. Connect your phone to the network the hue bridge is on. Start the hue app(iOS described here). Push link connect to the bridge. Use the app to find the bridge and try controlling lights. All working — Go to the settings menu in the app. Go to My Bridge. Go to Network settings. Switch off the DHCP toggle. The ip address of the bridge will show. Note the ip address, then switch DHCP back on

Step 3

Once you have the address load the test app by visiting the following address in your web browser.

https://<bridge ip address>/debug/clip.html
You should see an interface like this.

Using this debugger utility you can populate the components of an HTTPS call – the basis of all web traffic and of the hue RESTful interface.

You need to use the randomly generated username that the bridge creates for you. Fill in the info below and press the POST button.

URL	/api
Body	{"devicetype":"my_hue_app#android francesco"}
Method	POST
This command is basically saying please create a new resource inside /api (where usernames sit) with the following properties.

When you press the POST button you should get back an error message letting you know that you have to press the link button. This is our security step so that only apps you want to control your lights can. By pressing the button we prove that the user has physical access to the bridge.

Go and press the button on the bridge and then press the POST button again and you should get a success response like below.


Congratulations you’ve just created an authorized user, which we’ll use from now on!


# WIRING

-PIN 1 = POWER;
-PIN 40 = Ground;
-PIN 41 = DATA;


# HOW TO USE

Just download the python script and execute it
