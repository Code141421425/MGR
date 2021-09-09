from airtest.core.api import *
from GameSettings.PackageNameMapping import PackageNameMapping
import os

auto_setup(__file__)

for i in range(Times):
    touch([500,500])
    sleep(0.2)