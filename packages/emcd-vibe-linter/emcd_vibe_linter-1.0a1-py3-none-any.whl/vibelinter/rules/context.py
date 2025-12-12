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


''' Context extraction utilities for enhanced violation reporting. '''


from . import __
from . import violations as _violations


class ContextExtractor:
    ''' Extracts source code context around violations. '''

    def __init__(
        self,
        source_lines: __.typx.Annotated[
            tuple[ str, ... ],
            __.ddoc.Doc( 'Source file lines for context extraction.' ) ]
    ) -> None:
        self.source_lines = source_lines

    def extract_violation_context(
        self,
        violation: __.typx.Annotated[
            _violations.Violation,
            __.ddoc.Doc( 'Violation to extract context for.' ) ],
        context_size: __.typx.Annotated[
            int,
            __.ddoc.Doc(
                'Number of lines to show before and after violation.'
            ) ] = 2,
    ) -> __.typx.Annotated[
        _violations.ViolationContext,
        __.ddoc.Doc( 'Violation with surrounding source context.' ) ]:
        ''' Extracts source code context around a violation. '''
        line = violation.line
        start_line = max( 1, line - context_size )
        end_line = min( len( self.source_lines ), line + context_size )
        # Extract context lines (convert to 0-indexed for array access)
        context_lines = tuple(
            self.source_lines[ i ]
            for i in range( start_line - 1, end_line )
        )
        return _violations.ViolationContext(
            violation = violation,
            context_lines = context_lines,
            context_start_line = start_line,
        )

    def format_context_display(
        self,
        context: __.typx.Annotated[
            _violations.ViolationContext,
            __.ddoc.Doc( 'Violation context to format for display.' ) ],
        highlight_line: __.typx.Annotated[
            bool,
            __.ddoc.Doc( 'Whether to highlight the violation line.' ) ] = (
                True ),
    ) -> __.typx.Annotated[
        tuple[ str, ... ],
        __.ddoc.Doc(
            'Formatted context lines with line numbers and highlighting.'
        ) ]:
        ''' Formats violation context for display. '''
        formatted_lines: list[ str ] = [ ]
        violation_line = context.violation.line
        for i, line in enumerate( context.context_lines ):
            line_number = context.context_start_line + i
            prefix = (
                '→ ' if highlight_line and line_number == violation_line
                else '  ' )
            formatted_lines.append( f'{line_number:4d}{prefix}{line}' )
        return tuple( formatted_lines )


def extract_contexts_for_violations(
    violations: __.typx.Annotated[
        _violations.ViolationSequence,
        __.ddoc.Doc( 'Sequence of violations to extract contexts for.' ) ],
    source_lines: __.typx.Annotated[
        __.cabc.Sequence[ str ],
        __.ddoc.Doc( 'Source file lines for context extraction.' ) ],
    context_size: __.typx.Annotated[
        int,
        __.ddoc.Doc(
            'Number of lines to show before and after each violation.'
        ) ] = 2,
) -> tuple[ _violations.ViolationContext, ... ]:
    ''' Extracts contexts for multiple violations efficiently. '''
    extractor = ContextExtractor( tuple( source_lines ) )
    return tuple(
        extractor.extract_violation_context( violation, context_size )
        for violation in violations
    )
