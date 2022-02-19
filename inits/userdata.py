from libs.qu_json import *
import time

Userdata = Qu_json("rsc/userdata.json")

if Userdata.data["the_first_launch"] == -1:
    Userdata.data["the_first_launch"] = int(time.time())

Userdata.data["the_last_launch"] = int(time.time())

Userdata.save()
