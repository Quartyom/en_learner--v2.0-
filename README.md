Good luck to figure out how it works

There are some folders. /libs folder is liable for the app classes. The core of the app is Qu_parse (explore it thoroughly) which provides the means to add and call functions by their names. They are used for scenes and console methods. /inits folder have instances of classes from /libs. /rsc folder is (surpise) the folder with resources such as localizations and settings and other self-explanatory files. The main.py is the starter point of the app which imports files from /init and then handles scenes. Firstly, the menu scene.
