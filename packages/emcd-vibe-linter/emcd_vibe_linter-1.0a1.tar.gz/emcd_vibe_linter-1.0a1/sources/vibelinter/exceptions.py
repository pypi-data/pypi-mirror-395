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


''' Family of exceptions for package API. '''


from . import __


class Omniexception( __.immut.exceptions.Omniexception ):
    ''' Base for all exceptions raised by package API. '''


class Omnierror( Omniexception, Exception ):
    ''' Base for error exceptions raised by package API. '''

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders exception as JSON-compatible dictionary. '''
        return {
            'type': self.__class__.__name__,
            'message': str( self ),
        }

    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders exception as text lines. '''
        return (
            f'## {self.__class__.__name__}',
            f'**Message**: {self}',
        )


# Rule execution exceptions
class RuleExecuteFailure( Omnierror ):
    ''' Raised when rule execution encounters unrecoverable error. '''

    def __init__( self, context: str ) -> None:
        super( ).__init__(
            f'Rule execution failed for {context!r}' )
        self.context = context

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders exception with context information. '''
        return {
            'type': self.__class__.__name__,
            'message': str( self ),
            'context': self.context,
        }

    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders exception with context information. '''
        return (
            f'## {self.__class__.__name__}',
            f'**Message**: {self}',
            f'**Context**: {self.context}',
        )


class MetadataProvideFailure( Omnierror ):
    ''' Raised when LibCST metadata provider initialization fails. '''

    def __init__( self, filename: str ) -> None:
        super( ).__init__(
            f'Failed to initialize LibCST metadata for {filename!r}' )
        self.filename = filename

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders exception with filename information. '''
        return {
            'type': self.__class__.__name__,
            'message': str( self ),
            'filename': self.filename,
        }

    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders exception with filename information. '''
        return (
            f'## {self.__class__.__name__}',
            f'**Message**: {self}',
            f'**Filename**: {self.filename}',
        )


# Configuration exceptions
class RuleRegistryInvalidity( Omnierror ):
    ''' Raised when rule registry contains invalid mappings. '''

    def __init__( self, identifier: str ) -> None:
        super( ).__init__(
            f'Unknown or invalid rule identifier: {identifier!r}' )
        self.identifier = identifier

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders exception with identifier information. '''
        return {
            'type': self.__class__.__name__,
            'message': str( self ),
            'identifier': self.identifier,
        }

    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders exception with identifier information. '''
        return (
            f'## {self.__class__.__name__}',
            f'**Message**: {self}',
            f'**Identifier**: {self.identifier}',
        )


class RuleConfigureFailure( Omnierror ):
    ''' Raised when rule configuration parameters are invalid. '''
