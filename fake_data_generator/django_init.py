#  init file to setup django environment:
import os
import pathlib
import sys
import django

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

sys.dont_write_bytecode = True
sys.path.append(str(BASE_DIR / "pr1604"))
os.environ["DJANGO_SETTINGS_MODULE"] = "pr1604.settings"
django.setup()
print("Django environment set up")
