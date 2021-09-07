from airtest.core.api import *
from GameSettings.PackageNameMapping import PackageNameMapping
import os

auto_setup(__file__)

print("游戏启动： " + packageName)

start_app(packageName)

sleep(5)