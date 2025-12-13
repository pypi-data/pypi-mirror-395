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



''' VBL101: Detect blank lines between statements in function bodies.



    Category: Readability
    Subcategory: Compactness

    This rule detects blank lines between statements within function or
    method bodies and suggests their elimination to improve vertical
    compactness per the project coding standards. Blank lines inside
    string literals are allowed.
'''


from . import __


class VBL101( __.BaseRule ):
    ''' Detects blank lines between statements in function bodies. '''

    @property
    def rule_id( self ) -> str:
        return 'VBL101'

    def __init__(
        self,
        filename: str,
        wrapper: __.libcst.metadata.MetadataWrapper,
        source_lines: tuple[ str, ... ],
    ) -> None:
        super( ).__init__( filename, wrapper, source_lines )
        # Collection: store definition ranges (functions and classes)
        self._definition_ranges: list[
            tuple[ int, int, __.libcst.CSTNode ] ] = [ ]
        # Collection: store triple-quoted string literal line ranges
        self._string_ranges: list[ tuple[ int, int ] ] = [ ]
        # State: track reported lines to prevent duplicates in nested scopes
        self._reported_lines: set[ int ] = set( )

    def visit_FunctionDef( self, node: __.libcst.FunctionDef ) -> bool:
        ''' Collects function definitions for later analysis. '''
        self._collect_definition( node )
        return True  # Continue visiting children

    def visit_ClassDef( self, node: __.libcst.ClassDef ) -> bool:
        ''' Collects class definitions for later analysis. '''
        self._collect_definition( node )
        return True  # Continue visiting children

    def _collect_definition( self, node: __.libcst.CSTNode ) -> None:
        ''' Helper to collect ranges for functions and classes. '''
        try:
            position = self.wrapper.resolve(
                __.libcst.metadata.PositionProvider )[ node ]
            start_line = position.start.line
            end_line = position.end.line
            self._definition_ranges.append( ( start_line, end_line, node ) )
        except KeyError:
            # Position not available, skip this definition
            pass

    def visit_SimpleString( self, node: __.libcst.SimpleString ) -> bool:
        ''' Collects triple-quoted string literal ranges. '''
        # Only track triple-quoted strings (docstrings and multiline strings)
        if node.quote in ( '"""', "'''" ):
            try:
                position = self.wrapper.resolve(
                    __.libcst.metadata.PositionProvider )[ node ]
                start_line = position.start.line
                end_line = position.end.line
                self._string_ranges.append( ( start_line, end_line ) )
            except KeyError:
                # Position not available, skip this string
                pass
        return True  # Continue visiting children

    def visit_ConcatenatedString(
        self, node: __.libcst.ConcatenatedString
    ) -> bool:
        ''' Collects concatenated string literal ranges. '''
        # Check if any part is a triple-quoted string
        has_triple_quote = False
        for part in ( node.left, node.right ):
            if isinstance( part, __.libcst.SimpleString ):
                if part.quote in ( '"""', "'''" ):
                    has_triple_quote = True
                    break
            elif (
                isinstance( part, __.libcst.FormattedString )
                and part.start in ( '"""', "'''" )
            ):
                # f-strings can also be triple-quoted
                has_triple_quote = True
                break
        if has_triple_quote:
            try:
                position = self.wrapper.resolve(
                    __.libcst.metadata.PositionProvider )[ node ]
                start_line = position.start.line
                end_line = position.end.line
                self._string_ranges.append( ( start_line, end_line ) )
            except KeyError:
                # Position not available, skip this string
                pass
        return True  # Continue visiting children

    def _analyze_collections( self ) -> None:
        ''' Analyzes collected functions for blank lines between statements.
            Blank lines inside string literals are allowed.
            Blank lines around nested definitions are allowed.
        '''
        # Only analyze functions (skip classes as roots)
        # But we need all definitions for the adjacency check.
        function_nodes = [
            ( s, e, n ) for s, e, n in self._definition_ranges
            if isinstance( n, __.libcst.FunctionDef )
        ]
        for start_line, end_line, _func_node in function_nodes:
            # Get function body start (after the def line)
            body_start = start_line + 1
            for line_num in range( body_start, end_line + 1 ):
                if line_num - 1 >= len( self.source_lines ): break
                line = self.source_lines[ line_num - 1 ]
                stripped = line.strip( )
                # Report violation for blank lines between statements
                # Skip blank lines inside string literals
                # Skip blank lines immediately around nested definitions
                if (
                    not stripped
                    and not self._is_in_string( line_num )
                    and not self._is_adjacent_to_definition( line_num )
                ):
                    self._report_blank_line( line_num )

    def _is_in_string( self, line_num: int ) -> bool:
        ''' Checks if line is inside a triple-quoted string literal. '''
        return any(
            start <= line_num <= end
            for start, end in self._string_ranges )

    def _is_adjacent_to_definition( self, line_num: int ) -> bool:
        ''' Checks if line is immediately before or after a definition. '''
        return any(
            line_num == start - 1 or line_num == end + 1
            for start, end, _ in self._definition_ranges )

    def _report_blank_line( self, line_num: int ) -> None:
        ''' Reports a violation for a blank line in function body. '''
        if line_num in self._reported_lines: return
        self._reported_lines.add( line_num )
        from .. import violations as _violations
        violation = _violations.Violation(
            rule_id = self.rule_id,
            filename = self.filename,
            line = line_num,
            column = 1,
            message = "Blank line in function body.",
            severity = 'warning' )
        self._violations.append( violation )


# Self-register this rule
__.RULE_DESCRIPTORS[ 'VBL101' ] = __.RuleDescriptor(
    vbl_code = 'VBL101',
    descriptive_name = 'blank-line-elimination',
    description = 'Detects blank lines within function bodies.',
    category = 'readability',
    subcategory = 'compactness',
    rule_class = VBL101,
)
