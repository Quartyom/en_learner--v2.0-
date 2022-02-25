from libs.qu_json import *
from libs.qu_locale import *
import time
import libs.qu_datetime

Userdata = Qu_json("rsc/userdata.json")

@Userdata.set_default_func()
def userdata_set_default_func():
    Userdata.data = dict()
    Userdata.add("the_first_launch", libs.qu_datetime.now())
    Userdata.add("locale", "en")
    Userdata.add("words_learned", 0)
    Userdata.add("the_last_launch", libs.qu_datetime.now())  # its not a doubled statement
    Userdata.save()


if "the_first_launch" not in Userdata.data:
    Userdata.set_default()

delta_from_the_last_launch = libs.qu_datetime.now() - Userdata.data["the_last_launch"]

Userdata.add("the_last_launch", libs.qu_datetime.now())  # its not a doubled statement

Userdata.save()
