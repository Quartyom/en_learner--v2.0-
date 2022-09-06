<h1> En_learner v2 </h1>

<h2> Overview </h2>

This app stores and manages foreign words, phrases (whatever and not only english). It helps to learn many of them simultaneously without concerning about organisation and sorting. Each word will be shown several times at increasing intervals according to <a href="https://daniilshat.ru/" target="_blank">Forgetting curve</a>, increasing the chances of memorization.

<h2> Functions </h2>

The single words can be added, monitored, edited and deleted.
<b>/learn</b> command will show you all the words, which should be repeated so far. To checkout the entire dictionary, type <b>/viewdict</b>.
There are also commands to change localization, clean console, open stats etc.
Don't forget about <b>/help</b> and <b>/help [command_name]</b>.

<h2> Setup </h2>

You may do it either via git or by downloading zip file. Just lauch main.py to get started.

<h2> Shortcut </h2>

To create a shortcut, you'll need a compiled language e.g. C & C++. Just comile the the code snippet below (the is an icon in /rcs) and place it the project folder with main.py. Then create a shortcut.

#include <stdlib.h>
int main() {
	system("main.py");
}

<h2> Localization </h2>

They are stored in /rsc. To add your own, i recommend to copy <b>/rsc/ru</b> directory and use it like a template. The presence of <b>tag.json</b> and <b>/command_descriptions</b> is necessary.

<h2> Code </h2>

There are some folders. /libs folder is liable for the app classes. The core of the app is Qu_parse (explore it thoroughly) which provides the means to add and call functions by their names. They are used for scenes and console methods. /inits folder have instances of classes from /libs. /rsc folder is (surpise) the folder with resources such as localizations and settings and other self-explanatory files. The main.py is the starter point of the app which imports files from /init and then handles scenes. Firstly, the menu scene.
