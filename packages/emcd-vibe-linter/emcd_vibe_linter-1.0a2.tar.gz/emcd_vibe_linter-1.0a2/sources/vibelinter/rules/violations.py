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


''' Core violation data structures for linting framework. '''


from . import __


class Violation( __.immut.DataclassObject ):
    ''' Represents a rule violation with precise location information. '''

    rule_id: __.typx.Annotated[
        str,
        __.ddoc.Doc(
            'VBL code identifier for the rule that detected this violation.'
        ) ]
    filename: __.typx.Annotated[
        str, __.ddoc.Doc( 'Path to source file containing violation.' ) ]
    line: __.typx.Annotated[
        int, __.ddoc.Doc( 'One-indexed line number of violation.' ) ]
    column: __.typx.Annotated[
        int, __.ddoc.Doc( 'One-indexed column position of violation.' ) ]
    message: __.typx.Annotated[
        str, __.ddoc.Doc( 'Human-readable description of violation.' ) ]
    severity: __.typx.Annotated[
        str,
        __.ddoc.Doc( "Severity level: 'error', 'warning', or 'info'." ) ] = (
            'error' )

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders violation as JSON-compatible dictionary. '''
        return {
            'rule_id': self.rule_id,
            'filename': self.filename,
            'line': self.line,
            'column': self.column,
            'message': self.message,
            'severity': self.severity,
        }

    def render_as_text( self ) -> str:
        ''' Renders violation as text line. '''
        return (
            f'  {self.line}:{self.column} '
            f'{self.rule_id} {self.message}' )


class ViolationContext( __.immut.DataclassObject ):
    ''' Represents source code context surrounding a violation.

        Provides enhanced error reporting with surrounding lines.
    '''

    violation: __.typx.Annotated[
        Violation, __.ddoc.Doc( 'The violation this context describes.' ) ]
    context_lines: __.typx.Annotated[
        tuple[ str, ... ],
        __.ddoc.Doc( 'Source lines surrounding violation.' ) ]
    context_start_line: __.typx.Annotated[
        int, __.ddoc.Doc( 'One-indexed starting line of context display.' ) ]


# Type aliases for rule framework contracts
ViolationSequence: __.typx.TypeAlias = __.cabc.Sequence[ Violation ]
ViolationContextSequence: __.typx.TypeAlias = (
    __.cabc.Sequence[ ViolationContext ] )
