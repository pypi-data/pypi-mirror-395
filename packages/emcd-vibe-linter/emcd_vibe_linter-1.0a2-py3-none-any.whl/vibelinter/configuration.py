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


''' Configuration file discovery and parsing. '''


from tomli import loads as _toml_loads

from . import __
from . import exceptions as _exceptions


PathLike: __.typx.TypeAlias = str | __.pathlib.Path


class ConfigurationInvalidity( _exceptions.Omnierror, ValueError ):
    ''' Configuration file invalidity. '''

    def __init__( self, location: PathLike, reason: str ) -> None:
        self.location = str( location )
        self.reason = reason
        super( ).__init__( f'Invalid configuration at {location}: {reason}' )


class ConfigurationAbsence( _exceptions.Omnierror, FileNotFoundError ):
    ''' Configuration file absence. '''

    def __init__(
        self,
        location: __.Absential[ PathLike ] = __.absent,
    ) -> None:
        self.location = (
            None if __.is_absent( location ) else str( location ) )
        super( ).__init__(
            "No pyproject.toml found in current or parent directories"
            if __.is_absent( location )
            else f"Configuration file not found: {location}" )


class Configuration( __.immut.DataclassObject ):
    ''' Linter configuration from pyproject.toml file.

        Supports rule selection, file filtering, and context configuration.
    '''

    select: __.typx.Annotated[
        __.Absential[ tuple[ str, ... ] ],
        __.ddoc.Doc( 'VBL codes to enable (whitelist).' ) ] = __.absent
    exclude_rules: __.typx.Annotated[
        __.Absential[ tuple[ str, ... ] ],
        __.ddoc.Doc( 'VBL codes to disable (blacklist).' ) ] = __.absent
    include_paths: __.typx.Annotated[
        __.Absential[ tuple[ str, ... ] ],
        __.ddoc.Doc( 'File path patterns to include.' ) ] = __.absent
    exclude_paths: __.typx.Annotated[
        __.Absential[ tuple[ str, ... ] ],
        __.ddoc.Doc( 'File path patterns to exclude.' ) ] = __.absent
    context: __.typx.Annotated[
        __.Absential[ int ],
        __.ddoc.Doc( 'Number of context lines around violations.' )
    ] = __.absent
    rule_parameters: __.typx.Annotated[
        __.immut.Dictionary[ str, __.immut.Dictionary[ str, __.typx.Any ] ],
        __.ddoc.Doc( 'Per-rule configuration parameters.' )
    ] = __.dcls.field( default_factory = lambda: __.immut.Dictionary( ) )
    per_file_ignores: __.typx.Annotated[
        __.immut.Dictionary[ str, tuple[ str, ... ] ],
        __.ddoc.Doc( 'Per-file rule exclusions.' )
    ] = __.dcls.field( default_factory = lambda: __.immut.Dictionary( ) )


def discover_configuration(
    start_directory: __.Absential[ PathLike ] = __.absent,
) -> __.Absential[ Configuration ]:
    ''' Discovers and loads configuration from pyproject.toml.

        Searches from start directory up through parent directories.
        Returns absent if no configuration file found.
    '''
    config_path = _discover_pyproject_toml( start_directory )
    if __.is_absent( config_path ):
        return __.absent
    return load_configuration( config_path )


def load_configuration( location: PathLike ) -> Configuration:
    ''' Loads configuration from specified pyproject.toml file. '''
    file_path = __.pathlib.Path( location )
    try: content = file_path.read_text( encoding = 'utf-8' )
    except ( OSError, IOError ) as exception:
        raise ConfigurationAbsence( location ) from exception
    try: data = _toml_loads( content )
    except Exception as exception:
        raise ConfigurationInvalidity(
            location, f'Invalid TOML syntax: {exception}' ) from exception
    try: tool_config = data.get( 'tool', { } ).get( 'vibelinter', { } )
    except AttributeError as exception:
        raise ConfigurationInvalidity(
            location, 'Invalid TOML structure' ) from exception
    return _parse_configuration( tool_config, location )


def _discover_pyproject_toml(
    start_directory: __.Absential[ PathLike ],
) -> __.Absential[ __.pathlib.Path ]:
    ''' Searches for pyproject.toml from start directory upward. '''
    if __.is_absent( start_directory ):
        current = __.pathlib.Path.cwd( )
    else:
        current = __.pathlib.Path( start_directory ).resolve( )
    if current.is_file( ):
        current = current.parent
    while True:
        candidate = current / 'pyproject.toml'
        if candidate.exists( ) and candidate.is_file( ):
            return candidate
        parent = current.parent
        if parent == current:
            return __.absent
        current = parent


def _parse_configuration(
    data: __.cabc.Mapping[ str, __.typx.Any ],
    location: PathLike,
) -> Configuration:
    ''' Parses configuration dictionary from TOML data. '''
    select = _parse_string_sequence( data, 'select', location )
    exclude_rules = _parse_string_sequence( data, 'exclude', location )
    include_paths = _parse_string_sequence( data, 'include', location )
    exclude_paths = _parse_string_sequence(
        data, 'exclude_paths', location )
    context = _parse_optional_int( data, 'context', location )
    rule_parameters = _parse_rule_parameters( data, location )
    per_file_ignores = _parse_per_file_ignores( data, location )
    return Configuration(
        select = select,
        exclude_rules = exclude_rules,
        include_paths = include_paths,
        exclude_paths = exclude_paths,
        context = context,
        rule_parameters = rule_parameters,
        per_file_ignores = per_file_ignores,
    )


def _parse_optional_int(
    data: __.cabc.Mapping[ str, __.typx.Any ],
    key: str,
    location: PathLike,
) -> __.Absential[ int ]:
    ''' Parses optional integer value from configuration. '''
    if key not in data:
        return __.absent
    value = data[ key ]
    if not isinstance( value, int ):
        typename = type( value ).__name__
        raise ConfigurationInvalidity(
            location, f'"{key}" must be an integer, got {typename}' )
    if value < 0:
        raise ConfigurationInvalidity(
            location, f'"{key}" must be non-negative, got {value}' )
    return value


def _parse_rule_parameters(
    data: __.cabc.Mapping[ str, __.typx.Any ],
    location: PathLike,
) -> __.immut.Dictionary[ str, __.immut.Dictionary[ str, __.typx.Any ] ]:
    ''' Parses per-rule configuration from [tool.vibelinter.rules.*]. '''
    rules_section: __.typx.Any = data.get( 'rules', { } )
    if not isinstance( rules_section, dict ):
        typename = type( rules_section ).__name__
        raise ConfigurationInvalidity(
            location, f'"rules" must be a table, got {typename}' )
    result: dict[ str, __.immut.Dictionary[ str, __.typx.Any ] ] = { }
    section_dict = __.typx.cast(
        dict[ __.typx.Any, __.typx.Any ], rules_section )
    for rule_code, params in section_dict.items( ):
        if not isinstance( rule_code, str ):
            typename: str = type( rule_code ).__name__
            raise ConfigurationInvalidity(
                location, f'Rule code must be string, got {typename}' )
        if not isinstance( params, dict ):
            typename = type( params ).__name__
            raise ConfigurationInvalidity(
                location,
                f'Rule "{rule_code}" parameters must be a table, '
                f'got {typename}' )
        param_dict = __.typx.cast( dict[ str, __.typx.Any ], params )
        result[ rule_code ] = __.immut.Dictionary( param_dict )
    return __.immut.Dictionary( result )


def _parse_per_file_ignores(
    data: __.cabc.Mapping[ str, __.typx.Any ],
    location: PathLike,
) -> __.immut.Dictionary[ str, tuple[ str, ... ] ]:
    ''' Parses [tool.vibelinter.per-file-ignores]. '''
    ignores_section: __.typx.Any = data.get( 'per-file-ignores', { } )
    if not isinstance( ignores_section, dict ):
        typename = type( ignores_section ).__name__
        raise ConfigurationInvalidity(
            location, f'"per-file-ignores" must be a table, got {typename}' )
    result: dict[ str, tuple[ str, ... ] ] = { }
    section_dict = __.typx.cast(
        dict[ __.typx.Any, __.typx.Any ], ignores_section )
    for pattern, rules in section_dict.items( ):
        if not isinstance( pattern, str ):
            typename: str = type( pattern ).__name__
            raise ConfigurationInvalidity(
                location,
                f'Per-file-ignores pattern must be string, got {typename}' )
        if isinstance( rules, str ):
            result[ pattern ] = ( rules, )
            continue
        if not isinstance( rules, list ):
            typename = type( rules ).__name__
            raise ConfigurationInvalidity(
                location,
                f'Per-file-ignores rules for "{pattern}" must be list, '
                f'got {typename}' )
        rules_list = __.typx.cast( list[ __.typx.Any ], rules )
        rule_list: list[ str ] = [ ]
        for i, rule in enumerate( rules_list ):
            if not isinstance( rule, str ):
                typename = type( rule ).__name__
                raise ConfigurationInvalidity(
                    location,
                    f'Rule in "{pattern}"[{i}] must be string, '
                    f'got {typename}' )
            rule_list.append( rule )
        result[ pattern ] = tuple( rule_list )
    return __.immut.Dictionary( result )


def _parse_string_sequence(
    data: __.cabc.Mapping[ str, __.typx.Any ],
    key: str,
    location: PathLike,
) -> __.Absential[ tuple[ str, ... ] ]:
    ''' Parses optional list of strings from configuration. '''
    if key not in data:
        return __.absent
    value: __.typx.Any = data[ key ]
    if isinstance( value, str ):
        return ( value, )
    if not isinstance( value, list ):
        typename = type( value ).__name__
        raise ConfigurationInvalidity(
            location,
            f'"{key}" must be a string or list of strings, '
            f'got {typename}' )
    result: list[ str ] = [ ]
    value_list = __.typx.cast( list[ __.typx.Any ], value )
    for i, item in enumerate( value_list ):
        if not isinstance( item, str ):
            typename: str = type( item ).__name__
            raise ConfigurationInvalidity(
                location,
                f'"{key}"[{i}] must be a string, got {typename}' )
        result.append( item )
    return tuple( result )
