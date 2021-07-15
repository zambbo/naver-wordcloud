import pandas as pd
import re
import os

def getNickNameFromFileName(_filename):
    nickname = re.findall('.*-\d{4}',_filename)[0][:-5]
    return nickname

def getFileListFromPath(_path):
    return os.listdir(_path)

