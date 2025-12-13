import argparse
import base64
import enum
import functools
import importlib
import io
import inspect
import json
import math
import mimetypes
import operator
import os
import platform
import random
import re
import shutil
import socket
import sys
import time
import typing
import uuid
import warnings
import subprocess
import gc

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import partial, reduce
from pathlib import Path
from pprint import pprint
from types import SimpleNamespace, MethodType
from typing import *
from collections import OrderedDict, defaultdict, namedtuple
from abc import abstractmethod, ABC

import fastcore.all as fastcore
import numpy as np
import pandas as pd
import PIL
import pyperclip
import rich

from fastcore.all import L
from loguru import logger
from PIL import Image, ImageDraw, ImageFile, ImageFont
from PIL import features as PILFeatures
from rich.progress import track
from rich.traceback import install
from tqdm.auto import tqdm
from typing_extensions import Literal

ImageFile.LOAD_TRUNCATED_IMAGES = True
PathLike = Union[str, Path]

logger = logger.opt(colors=True)

def is_package_available(name: str) -> bool:
    if importlib.util.find_spec(name):
          return True
    else: return False
