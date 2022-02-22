from libs.qu_json import *
from libs.qu_locale import *
import time
import libs.qu_datetime

Userdata = Qu_json("rsc/userdata.json")

if "the_first_launch" not in Userdata.data:
    Userdata.data = dict()
    Userdata.data["the_first_launch"] = libs.qu_datetime.now()
    Userdata.data["locale"] = "en"
    Userdata.data["words_learned"] = 0
    Userdata.data["the_last_launch"] = libs.qu_datetime.now()

delta_from_the_last_launch = libs.qu_datetime.now() - Userdata.data["the_last_launch"]

Userdata.data["the_last_launch"] = libs.qu_datetime.now()

Userdata.save()
