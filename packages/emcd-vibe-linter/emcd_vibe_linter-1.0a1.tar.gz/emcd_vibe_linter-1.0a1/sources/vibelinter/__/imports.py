# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Common imports used throughout the package. '''

# ruff: noqa: F401


import                      abc
import collections.abc as   cabc
import contextlib as        ctxl
import dataclasses as       dcls
import                      enum
import                      json
import                      os
import                      pathlib
import                      sys
import                      time
import                      types

import accretive as         accret
import                      libcst
import                      libcst.metadata
import typing_extensions as typx
import                      wcmatch
import wcmatch.glob as      wcglob
# --- BEGIN: Injected by Copier ---
import dynadoc as           ddoc
import frigid as            immut
import                      tyro
# --- END: Injected by Copier ---

# --- BEGIN: Injected by Copier ---
from absence import Absential, absent, is_absent
# --- END: Injected by Copier ---
