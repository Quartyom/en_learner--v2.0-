import os, time                         # now()
from libs.qu_parse import *             # menu_parser
import libs.qu_words                    # new()
import libs.qu_files                    # help()
import libs.qu_datetime as qu_datetime  # new()
from libs.words_similarity import *
from inits.qu_json_init import *        # new()
from inits.scene_controller  import *   # run()
from inits.scene_parsers_init import *
from inits.userdata import *
from inits.settings import *
from inits.qu_locale_init import *
import inits.mistakes_counter

@scene_controller.method("multy")
def run():
    pass
