# Puffco-Voice - An alexa voice skill & python program to control a puffco peak pro. v0.5

Requirements:
  - Puffco Peak Pro
  - an Alexa device
  - windows or mac
  - Python3 (bleak, aioflask)

Step 1:
  Download everything included (alexa skill & python program).
  
Step 2: https://developer.amazon.com/alexa/console/ask/create-new-skill
  Create an Alexa skill and upload the puffco voice alexa skill to it. (Model to add to skill is custom, Choose a method to host your skill's backend resources will be python), click continue and select "Start from Scratch". Click on the button "Continue with template".
  
Step 3:
  Setup the python part. Open PuffcoWebAPI and install the requirements by opening "Install Python Requirements.bat". Once the requirements install open "Find Puffco.bat" and if your puffco is in bluetooth mode it will find the device and give you the mac address. Copy this address, edit main.py and put the mac address in between the "" on line 7.
  
Step 4:
  Start up an ngrok webserver and the localhost webserver by opening "Start.bat".  Ngrok is so Alexa can pass commands to your webserver. The webserver is what controls the puffco. You can get ngrok at https://ngrok.com/. The Ngrok console will give you a url like the following http://18f0-xx-xx-xx-xx.ngrok.io. Copy this URL and put it in the Alexa skill under the 'Code' tab. You will want to replace the pre existing URL in the Alexa skill where url = "" is
  
Step 5 (On alexa developer console):
  Under the build tab, click Invocation name and change the 'change me' to 'my puffco'. After that save the model and build it

Step 6:
  Open the code tab in the alexa developer console and import the "PuffcoAlexa" files. Click save then deploy.
Step 7: 
  Enable the dev skill in your alexa app on the phone and enjoy! 
  
 
Whats new in 0.5:
 - cable charging ready mode
  
Commands:
  1. Alexa, tell my puffco to connect - This will connect to your puffco, only need to run it once.
  2. Alexa, tell my puffco to preheat - preheats the current profile and tells you info about it (name, temp, time).
  3. Alexa, tell my puffco to preheat profile (1-4) - this preheats the profile you choose.
  4. Alexa, tell my puffco to preheat to (temperature) for (seconds) - This will change the current profile's settings so the settings you change works when preheating.
  5. Alexa, tell my puffco to [enable/turn on] / [disable/turn off] lantern mode - This will turn on/off lantern mode.
  6. Alexa, tell my puffco to [enable/turn on] / [disable/turn off] party mode - This will turn on/off party mode.
  7. Alexa, tell my puffco to [enable/turn on] / [disable/turn off] stealth mode - This will turn on/off stealth mode.
  8. Alexa, ask my puffco how many dabs I've taken in total - This will tell you how many dabs you've taken in total.
  9. Alexa, ask my puffco how many dabs I take daily - This will tell you your daily dab count.
  10. Alexa, ask my puffco how many dabs remaining - This will tell you roughly how many dabs left before the battery dies.
  11. Alexa, tell my puffco to set lantern colour to (colour) - This will set lantern colour to specified colour.
  12. Alexa, ask my puffco how much battery is left - This will tell you how much battery percent is left (and flash the battery level on the puffco)
  13. Alexa, tell my puffco to boost - This will boost if theres currently a cycle active
  14. Alexa, tell my puffco to cancel/stop preheat - This will stop a preheat cycle if active.
  15. Alexa, tell my puffco to [enable/turn on] / [disable/turn off] ready mode - This will enable ready mode for cable charging


  
