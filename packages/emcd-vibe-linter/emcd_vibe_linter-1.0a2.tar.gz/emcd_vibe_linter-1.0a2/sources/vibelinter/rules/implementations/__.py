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


''' Re-exports and global registry for rule implementations. '''

# ruff: noqa: F403, F405, F401


from ..__ import *
from ..base import BaseRule
from ..registry import *


# Global mutable registry for self-registering rules
RULE_DESCRIPTORS: accret.Dictionary[ str, RuleDescriptor ] = (
    accret.Dictionary( ) )


def create_registry_manager( ) -> RuleRegistryManager:
    ''' Creates rule registry manager from self-registered rules. '''
    return RuleRegistryManager( dict( RULE_DESCRIPTORS ) )
