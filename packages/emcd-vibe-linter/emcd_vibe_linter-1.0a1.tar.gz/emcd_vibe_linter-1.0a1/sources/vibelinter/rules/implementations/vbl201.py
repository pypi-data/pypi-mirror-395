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



''' VBL201: Import hub enforcement - no public imports in non-hub modules.



    Category: Imports / Architecture
    Subcategory: Namespace Management

    This rule enforces the import hub pattern by detecting non-private imports
    in modules that are not designated as import hubs. All imports must either:
    1. Be from __future__
    2. Result in private names (starting with _)
    3. Be in a hub module (identified by configurable glob patterns)

    This maintains architectural consistency, prevents namespace pollution,
    and makes the codebase self-documenting.
'''


from . import __


class VBL201( __.BaseRule ):
    ''' Enforces import hub pattern for non-hub modules. '''

    @property
    def rule_id( self ) -> str:
        return 'VBL201'

    def __init__(
        self,
        filename: str,
        wrapper: __.libcst.metadata.MetadataWrapper,
        source_lines: tuple[ str, ... ],
        hub_patterns: __.Absential[ tuple[ str, ... ] ] = __.absent,
    ) -> None:
        super( ).__init__( filename, wrapper, source_lines )
        # Store hub patterns from configuration or use defaults
        self._hub_patterns: tuple[ str, ... ] = (
            hub_patterns if not __.is_absent( hub_patterns )
            else ( '__init__.py', '__main__.py', '__.py', '__/imports.py' ) )
        # Determine if this file is a hub module
        self._is_hub_module: bool = self._is_import_hub_module( )
        # Track function nesting depth (to allow local imports)
        self._function_depth: int = 0
        # Collections for violations
        self._simple_imports: list[ __.libcst.Import ] = [ ]
        self._from_imports: list[ __.libcst.ImportFrom ] = [ ]

    def visit_FunctionDef( self, node: __.libcst.FunctionDef ) -> bool:
        ''' Tracks entry into function definitions. '''
        self._function_depth += 1
        return True

    def leave_FunctionDef(
        self, original_node: __.libcst.FunctionDef
    ) -> None:
        ''' Tracks exit from function definitions. '''
        self._function_depth -= 1

    def visit_Import( self, node: __.libcst.Import ) -> bool:
        ''' Collects module-level simple import statements (import foo). '''
        if self._is_hub_module:
            return True
        # Allow imports inside function bodies (local imports)
        if self._function_depth > 0:
            return True
        # Check if all imported names are private
        if all( self._is_alias_private( alias ) for alias in node.names ):
            return True
        self._simple_imports.append( node )
        return True

    def visit_ImportFrom( self, node: __.libcst.ImportFrom ) -> bool:
        ''' Collects module-level from imports (from foo import bar). '''
        if self._is_hub_module:
            return True
        # Allow imports inside function bodies (local imports)
        if self._function_depth > 0:
            return True
        if self._is_future_import( node ):
            return True
        if self._has_private_names( node ):
            return True
        self._from_imports.append( node )
        return True

    def _analyze_collections( self ) -> None:
        ''' Analyzes collected imports and generates violations. '''
        for node in self._simple_imports:
            self._report_simple_import_violation( node )
        for node in self._from_imports:
            self._report_from_import_violation( node )

    def _is_import_hub_module( self ) -> bool:
        ''' Checks if current file matches any hub module pattern.

            Uses glob patterns from configuration to identify hub modules.
            Patterns are matched against both the filename and full path.
        '''
        file_path = __.pathlib.Path( self.filename )
        for pattern in self._hub_patterns:
            # Try matching against the file path
            if file_path.match( pattern ):
                return True
            # Try matching with wildcard prefix for path-based patterns
            if file_path.match( f'*/{pattern}' ):
                return True
        return False

    def _is_future_import( self, node: __.libcst.ImportFrom ) -> bool:
        ''' Checks if import is from __future__. '''
        module = node.module
        if isinstance( module, __.libcst.Attribute ):
            return False
        if module is None:
            return False
        return module.value == '__future__'

    def _has_private_names( self, node: __.libcst.ImportFrom ) -> bool:
        ''' Checks if all imported names are private (start with _).

            Examples of allowed imports:
            - from . import __  (__ starts with _)
            - from . import exceptions as _exceptions  (alias starts with _)
            - from json import loads as _json_loads  (alias starts with _)

            Examples of violations:
            - from . import exceptions  (exceptions doesn't start with _)
            - from pathlib import Path  (Path doesn't start with _)
            - from pathlib import Path as P  (P doesn't start with _)
        '''
        # Star imports are never private
        if isinstance( node.names, __.libcst.ImportStar ):
            return False
        # Check each imported name
        return all( self._is_alias_private( alias ) for alias in node.names )

    def _is_alias_private( self, alias: __.libcst.ImportAlias ) -> bool:
        ''' Checks if an import alias results in a private name. '''
        if isinstance( alias.asname, __.libcst.AsName ):
            alias_name = alias.asname.name
            if isinstance( alias_name, __.libcst.Name ):
                return alias_name.value.startswith( '_' )
            return False
        node = alias.name
        while isinstance( node, __.libcst.Attribute ):
            node = node.value
        if isinstance( node, __.libcst.Name ):
            return node.value.startswith( '_' )
        return False

    def _report_simple_import_violation(
        self, node: __.libcst.Import
    ) -> None:
        ''' Reports violation for simple import statement. '''
        # Extract module name from import
        if node.names:
            module_name = node.names[ 0 ].name.value
            message = (
                f"Direct import of '{module_name}'. "
                f"Use import hub or private alias."
            )
        else:
            message = (
                "Direct import detected. Use import hub or private alias." )
        self._produce_violation( node, message, severity = 'warning' )

    def _report_from_import_violation(
        self, node: __.libcst.ImportFrom
    ) -> None:
        ''' Reports violation for from import statement. '''
        # Extract module name
        if node.module is None:
            module_name = "relative import"
        elif isinstance( node.module, __.libcst.Attribute ):
            module_name = self._extract_dotted_name( node.module )
        else:
            module_name = node.module.value
        # Extract imported names
        imported_names: list[ str ] = [ ]
        if isinstance( node.names, __.libcst.ImportStar ):
            imported_names = [ '*' ]
        else:
            for name in node.names:
                name_node = name.name
                if isinstance( name_node, __.libcst.Name ):
                    imported_names.append( name_node.value )
        names_str = ', '.join( imported_names )
        message = (
            f"Non-private import from '{module_name}': {names_str}. "
            f"Use private names (starting with _)."
        )
        self._produce_violation( node, message, severity = 'warning' )

    def _extract_dotted_name( self, attr: __.libcst.Attribute ) -> str:
        ''' Extracts dotted module name from Attribute node. '''
        parts: list[ str ] = [ ]
        current: __.libcst.BaseExpression = attr
        while isinstance( current, __.libcst.Attribute ):
            parts.append( current.attr.value )
            current = current.value
        if isinstance( current, __.libcst.Name ):
            parts.append( current.value )
        parts.reverse( )
        return '.'.join( parts )


# Self-register this rule
__.RULE_DESCRIPTORS[ 'VBL201' ] = __.RuleDescriptor(
    vbl_code = 'VBL201',
    descriptive_name = 'import-hub-enforcement',
    description = 'Enforces import hub pattern for non-hub modules.',
    category = 'imports',
    subcategory = 'architecture',
    rule_class = VBL201,
)
