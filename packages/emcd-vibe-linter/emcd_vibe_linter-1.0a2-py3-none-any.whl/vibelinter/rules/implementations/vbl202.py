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



''' VBL202: Import spaghetti detection - prevents excessive relative imports.



    Category: Imports / Architecture
    Subcategory: Module Coupling

    This rule prevents "import spaghetti" by restricting the depth of relative
    imports. Specifically:

    1. Relative imports with more than 2 parent levels (e.g., `...`, `....`)
       are never allowed anywhere.

    2. Relative imports with exactly 2 parent levels (e.g., `from .. import`)
       are only allowed in private re-export hub modules (configurable,
       defaults to `__.py`).

    3. Relative imports with exactly 1 level (e.g., `from . import`) are not
       allowed in re-export hub modules (`__.py`). This prevents backward
       imports since siblings expect to do `from . import __`.

    This maintains low coupling between packages and prevents complex
    dependency chains that make code hard to understand and refactor.
'''


from . import __


# Maximum allowed relative import depth
_MAX_RELATIVE_IMPORT_DEPTH = 2


class VBL202( __.BaseRule ):
    ''' Enforces restrictions on relative import depth. '''

    @property
    def rule_id( self ) -> str:
        return 'VBL202'

    def __init__(
        self,
        filename: str,
        wrapper: __.libcst.metadata.MetadataWrapper,
        source_lines: tuple[ str, ... ],
        reexport_hub_patterns: __.Absential[ tuple[ str, ... ] ] = __.absent,
    ) -> None:
        super( ).__init__( filename, wrapper, source_lines )
        # Store re-export hub patterns from configuration or use defaults
        self._reexport_hub_patterns: tuple[ str, ... ] = (
            reexport_hub_patterns if not __.is_absent( reexport_hub_patterns )
            else ( '__.py', ) )
        # Determine if this file is a re-export hub module
        self._is_reexport_hub: bool = self._is_reexport_hub_module( )
        # Collections for violations
        self._excessive_depth_imports: list[ __.libcst.ImportFrom ] = [ ]
        self._two_level_imports: list[ __.libcst.ImportFrom ] = [ ]
        self._one_level_imports_in_hub: list[ __.libcst.ImportFrom ] = [ ]

    def visit_ImportFrom( self, node: __.libcst.ImportFrom ) -> bool:
        ''' Collects relative import statements with parent references. '''
        # Calculate the relative import depth
        depth = self._calculate_relative_depth( node )
        if depth == 0:
            # Not a relative import, no violation
            return True
        if depth > _MAX_RELATIVE_IMPORT_DEPTH:
            # More than 2 levels is always a violation
            self._excessive_depth_imports.append( node )
        elif depth == _MAX_RELATIVE_IMPORT_DEPTH and not self._is_reexport_hub:
            # Exactly 2 levels is only allowed in re-export hubs
            self._two_level_imports.append( node )
        elif depth == 1 and self._is_reexport_hub:
            # Single-level imports are not allowed in re-export hubs
            self._one_level_imports_in_hub.append( node )
        return True

    def _analyze_collections( self ) -> None:
        ''' Analyzes collected imports and generates violations. '''
        for node in self._excessive_depth_imports:
            self._report_excessive_depth_violation( node )
        for node in self._two_level_imports:
            self._report_two_level_violation( node )
        for node in self._one_level_imports_in_hub:
            self._report_one_level_in_hub_violation( node )

    def _is_reexport_hub_module( self ) -> bool:
        ''' Checks if current file matches any re-export hub pattern.

            Uses glob patterns from configuration to identify re-export hubs.
            Patterns are matched against both the filename and full path.
        '''
        file_path = __.pathlib.Path( self.filename )
        for pattern in self._reexport_hub_patterns:
            # Try matching against the file path
            if file_path.match( pattern ):
                return True
            # Try matching with wildcard prefix for path-based patterns
            if file_path.match( f'*/{pattern}' ):
                return True
        return False

    def _calculate_relative_depth( self, node: __.libcst.ImportFrom ) -> int:
        ''' Calculates the depth of relative import (number of parent levels).

            Examples:
            - from . import foo       -> depth 1
            - from .. import foo      -> depth 2
            - from ... import foo     -> depth 3
            - from .... import foo    -> depth 4
            - from foo import bar     -> depth 0 (absolute import)
        '''
        # Check if this is a relative import
        if node.relative:
            # Count the dots
            # node.relative is a sequence of Dot objects
            return len( node.relative )
        return 0

    def _report_excessive_depth_violation(
        self, node: __.libcst.ImportFrom
    ) -> None:
        ''' Reports violation for import with more than 2 parent levels. '''
        depth = self._calculate_relative_depth( node )
        dots = '.' * depth
        message = (
            f"Excessive relative import depth ({depth} levels): '{dots}'. "
            f"Maximum allowed depth is {_MAX_RELATIVE_IMPORT_DEPTH} levels."
        )
        self._produce_violation( node, message, severity = 'error' )

    def _report_two_level_violation(
        self, node: __.libcst.ImportFrom
    ) -> None:
        ''' Reports violation for 2-level import outside re-export hub. '''
        patterns_str = ', '.join( self._reexport_hub_patterns )
        message = (
            "Two-level relative import ('from .. import') is only allowed "
            f"in re-export hub modules ({patterns_str}). "
            "Move this import to a re-export hub or reduce import depth."
        )
        self._produce_violation( node, message, severity = 'warning' )

    def _report_one_level_in_hub_violation(
        self, node: __.libcst.ImportFrom
    ) -> None:
        ''' Reports violation for single-level import in re-export hub. '''
        patterns_str = ', '.join( self._reexport_hub_patterns )
        message = (
            "Single-level relative import ('from . import') is not allowed "
            f"in re-export hub modules ({patterns_str}). This creates "
            "backward imports since siblings expect to import the hub "
            "(e.g., 'from . import __'). Import from parent package "
            "instead using 'from .. import'."
        )
        self._produce_violation( node, message, severity = 'warning' )


# Self-register this rule
__.RULE_DESCRIPTORS[ 'VBL202' ] = __.RuleDescriptor(
    vbl_code = 'VBL202',
    descriptive_name = 'import-spaghetti-detection',
    description = 'Prevents excessive relative import depth.',
    category = 'imports',
    subcategory = 'architecture',
    rule_class = VBL202,
)
