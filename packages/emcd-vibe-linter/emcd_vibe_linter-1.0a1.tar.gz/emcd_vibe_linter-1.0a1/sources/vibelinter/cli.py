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


''' Command-line interface. '''

# ruff: noqa: F821


from appcore import cli as _appcore_cli

from . import __
from . import configuration as _configuration
from . import engine as _engine
from . import rules as _rules


class DiffFormats( __.enum.Enum ):
    ''' Diff visualization formats. '''

    Unified = 'unified'
    Context = 'context'


class DisplayFormats( __.enum.Enum ):
    ''' Output formats for reporting. '''

    Text = 'text'
    Json = 'json'


class DisplayOptions( _appcore_cli.DisplayOptions ):
    ''' Display options extending appcore.cli with output format selection.

        Adds format-specific output control for linter reporting.
    '''

    format: __.typx.Annotated[
        DisplayFormats,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Output format for reporting. ''' )
    ] = DisplayFormats.Text
    context: __.typx.Annotated[
        int,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Show context lines around violations. ''' )
    ] = 0


RuleSelectorArgument: __.typx.TypeAlias = __.typx.Annotated[
    str,
    __.tyro.conf.arg( prefix_name = False ),
    __.ddoc.Doc( ''' Comma-separated VBL rule codes (e.g. VBL101,VBL201). ''' )
]
PathsArgument: __.typx.TypeAlias = __.tyro.conf.Positional[
    tuple[ str, ... ]
]


class RenderableResult( __.immut.DataclassProtocol, __.typx.Protocol ):
    ''' Protocol for command results with format-specific rendering.

        Combines DataclassProtocol and Protocol to provide both structural
        typing and dataclass compatibility. Result classes should explicitly
        inherit from this base class.
    '''

    @__.abc.abstractmethod
    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders result as JSON-compatible dictionary. '''
        raise NotImplementedError

    @__.abc.abstractmethod
    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders result as text lines. '''
        raise NotImplementedError


class CheckResult( RenderableResult ):
    ''' Result from check command execution. '''

    paths: tuple[ str, ... ]
    reports: tuple[ __.typx.Any, ... ]  # Engine Report objects
    total_violations: int
    total_files: int
    rule_selection: __.Absential[ str ] = __.absent

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders result as JSON-compatible dictionary. '''
        files_data: list[ dict[ str, __.typx.Any ] ] = [ ]
        for report_obj in self.reports:
            typed_report = __.typx.cast( _engine.Report, report_obj )
            violations_data = [
                v.render_as_json( ) for v in typed_report.violations
            ]
            files_data.append( {
                'filename': typed_report.filename,
                'violations': violations_data,
                'violation_count': len( typed_report.violations ),
                'rule_count': typed_report.rule_count,
                'analysis_duration_ms': typed_report.analysis_duration_ms,
            } )
        result: dict[ str, __.typx.Any ] = {
            'files': files_data,
            'total_violations': self.total_violations,
            'total_files': self.total_files,
        }
        if not __.is_absent( self.rule_selection ):
            result[ 'rule_selection' ] = self.rule_selection
        return result

    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders result as text lines. '''
        lines: list[ str ] = [ ]
        for report_obj in self.reports:
            typed_report = __.typx.cast( _engine.Report, report_obj )
            if typed_report.violations:
                lines.append( f'\n{typed_report.filename}:' )
                lines.extend(
                    v.render_as_text( )
                    for v in typed_report.violations )
        if not lines:
            lines.append( 'No violations found.' )
        else:
            lines.append(
                f'\nFound {self.total_violations} violations '
                f'in {self.total_files} files.' )
        return tuple( lines )


class FixResult( RenderableResult ):
    ''' Result from fix command execution. '''

    paths: tuple[ str, ... ]
    simulate: bool
    diff_format: str
    apply_dangerous: bool
    rule_selection: __.Absential[ str ] = __.absent

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders result as JSON-compatible dictionary. '''
        result: dict[ str, __.typx.Any ] = {
            'paths': list( self.paths ),
            'simulate': self.simulate,
            'diff_format': self.diff_format,
            'apply_dangerous': self.apply_dangerous,
        }
        if not __.is_absent( self.rule_selection ):
            result[ 'rule_selection' ] = self.rule_selection
        return result

    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders result as text lines. '''
        lines = [ f'Fixing paths: {self.paths}' ]
        if not __.is_absent( self.rule_selection ):
            lines.append( f'  Rule selection: {self.rule_selection}' )
        lines.append( f'  Simulate: {self.simulate}' )
        lines.append( f'  Diff format: {self.diff_format}' )
        lines.append( f'  Apply dangerous: {self.apply_dangerous}' )
        return tuple( lines )


class ConfigureResult( RenderableResult ):
    ''' Result from configure command execution. '''

    validate: bool
    interactive: bool
    display_effective: bool

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders result as JSON-compatible dictionary. '''
        return {
            'validate': self.validate,
            'interactive': self.interactive,
            'display_effective': self.display_effective,
        }

    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders result as text lines. '''
        return (
            'Configure command',
            f'  Validate: {self.validate}',
            f'  Interactive: {self.interactive}',
            f'  Display effective: {self.display_effective}',
        )


class DescribeRulesResult( RenderableResult ):
    ''' Result from describe rules command execution. '''

    details: bool

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders result as JSON-compatible dictionary. '''
        return { 'details': self.details }

    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders result as text lines. '''
        return (
            'Available rules',
            f'  Details: {self.details}',
        )


class DescribeRuleResult( RenderableResult ):
    ''' Result from describe rule command execution. '''

    rule_id: str
    details: bool

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders result as JSON-compatible dictionary. '''
        return {
            'rule_id': self.rule_id,
            'details': self.details,
        }

    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders result as text lines. '''
        return (
            f'Rule: {self.rule_id}',
            f'  Details: {self.details}',
        )


class ServeResult( RenderableResult ):
    ''' Result from serve command execution. '''

    protocol: str

    def render_as_json( self ) -> dict[ str, __.typx.Any ]:
        ''' Renders result as JSON-compatible dictionary. '''
        return {
            'protocol': self.protocol,
            'status': 'not_implemented',
        }

    def render_as_text( self ) -> tuple[ str, ... ]:
        ''' Renders result as text lines. '''
        return (
            f'Protocol server: {self.protocol}',
            '  (Not yet implemented)',
        )


class CheckCommand( __.immut.DataclassObject ):
    ''' Analyzes code and reports violations. '''

    paths: PathsArgument = ( '.',)
    select: __.Absential[ RuleSelectorArgument ] = __.absent
    jobs: __.typx.Annotated[
        __.typx.Union[ int, __.typx.Literal[ 'auto' ] ],
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Number of parallel processing jobs. ''' )
    ] = 'auto'

    async def __call__( self, display: DisplayOptions ) -> int:
        ''' Executes the check command. '''
        # TODO: Implement parallel processing with jobs parameter
        _ = self.jobs  # Suppress vulture warning
        config = _configuration.discover_configuration( )
        file_paths = _discover_python_files( self.paths )
        if not __.is_absent( config ):
            file_paths = _apply_path_filters( file_paths, config )
        if not file_paths:
            result = CheckResult(
                paths = self.paths,
                reports = ( ),
                total_violations = 0,
                total_files = 0,
                rule_selection = self.select,
            )
            async with __.ctxl.AsyncExitStack( ) as exits:
                await _render_and_print_result( result, display, exits )
            return 0
        enabled_rules = _merge_rule_selection( self.select, config )
        context_size = _merge_context_size( display.context, config )
        rule_parameters: __.immut.Dictionary[
            str, __.immut.Dictionary[ str, __.typx.Any ] ]
        if __.is_absent( config ):
            rule_parameters = __.immut.Dictionary( )
        else:
            rule_parameters = config.rule_parameters
        configuration = _engine.EngineConfiguration(
            enabled_rules = enabled_rules,
            context_size = context_size,
            include_context = context_size > 0,
            rule_parameters = rule_parameters,
        )
        registry_manager = _rules.create_registry_manager( )
        engine = _engine.Engine( registry_manager, configuration )
        reports = engine.lint_files( file_paths )
        total_violations = sum( len( r.violations ) for r in reports )
        result = CheckResult(
            paths = self.paths,
            reports = reports,
            total_violations = total_violations,
            total_files = len( reports ),
            rule_selection = self.select,
        )
        async with __.ctxl.AsyncExitStack( ) as exits:
            await _render_and_print_result( result, display, exits )
        return 1 if total_violations > 0 else 0


class FixCommand( __.immut.DataclassObject ):
    ''' Applies automated fixes with safety controls. '''

    paths: PathsArgument = ( '.',)
    select: __.Absential[ RuleSelectorArgument ] = __.absent
    simulate: __.typx.Annotated[
        bool,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Preview changes without applying them. ''' )
    ] = False
    diff_format: __.typx.Annotated[
        DiffFormats,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Diff visualization format. ''' )
    ] = DiffFormats.Unified
    apply_dangerous: __.typx.Annotated[
        bool,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Enable potentially unsafe fixes. ''' )
    ] = False

    async def __call__( self, display: DisplayOptions ) -> int:
        ''' Executes the fix command. '''
        result = FixResult(
            paths = self.paths,
            simulate = self.simulate,
            diff_format = self.diff_format.value,
            apply_dangerous = self.apply_dangerous,
            rule_selection = self.select,
        )
        async with __.ctxl.AsyncExitStack( ) as exits:
            await _render_and_print_result( result, display, exits )
        return 0


class ConfigureCommand( __.immut.DataclassObject ):
    ''' Manages configuration without destructive file editing. '''

    validate: __.typx.Annotated[
        bool,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc(
            ''' Validate existing configuration without analysis. ''' )
    ] = False
    interactive: __.typx.Annotated[
        bool,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Interactive configuration wizard. ''' )
    ] = False
    display_effective: __.typx.Annotated[
        bool,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Display effective merged configuration. ''' )
    ] = False

    async def __call__( self, display: DisplayOptions ) -> int:
        ''' Executes the configure command. '''
        result = ConfigureResult(
            validate = self.validate,
            interactive = self.interactive,
            display_effective = self.display_effective,
        )
        async with __.ctxl.AsyncExitStack( ) as exits:
            await _render_and_print_result( result, display, exits )
        return 0


class DescribeRulesCommand( __.immut.DataclassObject ):
    ''' Lists all available rules with descriptions. '''

    details: __.typx.Annotated[
        bool,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc(
            ''' Display detailed rule information including '''
            ''' configuration status. ''' )
    ] = False

    async def __call__( self, display: DisplayOptions ) -> int:
        ''' Executes the describe rules command. '''
        result = DescribeRulesResult( details = self.details )
        async with __.ctxl.AsyncExitStack( ) as exits:
            await _render_and_print_result( result, display, exits )
        return 0


class DescribeRuleCommand( __.immut.DataclassObject ):
    ''' Displays detailed information for a specific rule. '''

    rule_id: __.tyro.conf.Positional[ str ]
    details: __.typx.Annotated[
        bool,
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc(
            ''' Display detailed rule information including '''
            ''' configuration status. ''' )
    ] = False

    async def __call__( self, display: DisplayOptions ) -> int:
        ''' Executes the describe rule command. '''
        result = DescribeRuleResult(
            rule_id = self.rule_id,
            details = self.details,
        )
        async with __.ctxl.AsyncExitStack( ) as exits:
            await _render_and_print_result( result, display, exits )
        return 0


class DescribeCommand( __.immut.DataclassObject ):
    ''' Displays rule information and documentation. '''

    subcommand: __.typx.Union[
        __.typx.Annotated[
            DescribeRulesCommand,
            __.tyro.conf.subcommand( 'rules', prefix_name = False ),
        ],
        __.typx.Annotated[
            DescribeRuleCommand,
            __.tyro.conf.subcommand( 'rule', prefix_name = False ),
        ],
    ]

    async def __call__( self, display: DisplayOptions ) -> int:
        ''' Delegates to selected subcommand. '''
        return await self.subcommand( display )


class ServeCommand( __.immut.DataclassObject ):
    ''' Starts a protocol server (future implementation). '''

    protocol: __.typx.Annotated[
        __.typx.Literal[ 'lsp', 'mcp' ],
        __.tyro.conf.arg( prefix_name = False ),
        __.ddoc.Doc( ''' Protocol server to start. ''' )
    ] = 'mcp'

    async def __call__( self, display: DisplayOptions ) -> int:
        ''' Executes the serve command. '''
        result = ServeResult( protocol = self.protocol )
        async with __.ctxl.AsyncExitStack( ) as exits:
            await _render_and_print_result( result, display, exits )
        return 0


class Cli( __.immut.DataclassObject ):
    ''' Linter command-line interface. '''

    command: __.typx.Union[
        __.typx.Annotated[
            CheckCommand,
            __.tyro.conf.subcommand(
                'check', prefix_name = False, default = True ),
        ],
        __.typx.Annotated[
            FixCommand,
            __.tyro.conf.subcommand( 'fix', prefix_name = False ),
        ],
        __.typx.Annotated[
            ConfigureCommand,
            __.tyro.conf.subcommand( 'configure', prefix_name = False ),
        ],
        __.typx.Annotated[
            DescribeCommand,
            __.tyro.conf.subcommand( 'describe', prefix_name = False ),
        ],
        __.typx.Annotated[
            ServeCommand,
            __.tyro.conf.subcommand( 'serve', prefix_name = False ),
        ],
    ]
    display: __.typx.Annotated[
        DisplayOptions,
        __.tyro.conf.arg( prefix_name = False ),
    ] = __.dcls.field( default_factory = DisplayOptions )
    verbose: __.typx.Annotated[
        bool,
        __.ddoc.Doc( ''' Enable verbose output. ''' )
    ] = False

    async def __call__( self ) -> None:
        ''' Invokes selected subcommand after system preparation. '''
        # TODO: Implement verbose logging setup
        _ = self.verbose  # Suppress vulture warning
        async with intercept_errors( self.display ):
            exit_code = await self.command( self.display )
            raise SystemExit( exit_code )


def execute( ) -> None:
    ''' Entrypoint for CLI execution. '''
    from asyncio import run
    config = (
        __.tyro.conf.EnumChoicesFromValues,
        __.tyro.conf.HelptextFromCommentsOff,
    )
    try: run( __.tyro.cli( Cli, config = config )( ) ) # pyright: ignore
    except SystemExit: raise
    except BaseException:
        # TODO: Log exception with proper error handling
        raise SystemExit( 1 ) from None


@__.ctxl.asynccontextmanager
async def intercept_errors(
    display: DisplayOptions,
) -> __.cabc.AsyncIterator[ None ]:
    ''' Context manager that intercepts and renders exceptions.

        Catches Omnierror exceptions and renders them according to the
        display format. Handles unexpected exceptions by logging and
        formatting as errors.
    '''
    from . import exceptions as _exceptions
    try:
        yield
    except _exceptions.Omnierror as exc:
        async with __.ctxl.AsyncExitStack( ) as exits:
            stream = await display.provide_stream( exits )
            match display.format:
                case DisplayFormats.Json:
                    stream.write(
                        __.json.dumps( exc.render_as_json( ), indent = 2 ) )
                    stream.write( '\n' )
                case DisplayFormats.Text:
                    for line in exc.render_as_text( ):
                        stream.write( line )
                        stream.write( '\n' )
        raise SystemExit( 1 ) from exc
    except ( SystemExit, KeyboardInterrupt ):
        raise
    except BaseException as exc:
        # TODO: Log exception with proper error handling via scribe
        async with __.ctxl.AsyncExitStack( ) as exits:
            stream = await display.provide_stream( exits )
            match display.format:
                case DisplayFormats.Json:
                    error_data = {
                        'type': 'unexpected_error',
                        'message': str( exc ),
                    }
                    stream.write( __.json.dumps( error_data, indent = 2 ) )
                    stream.write( '\n' )
                case DisplayFormats.Text:
                    stream.write( '## Unexpected Error\n' )
                    stream.write( f'**Message**: {exc}\n' )
        raise SystemExit( 1 ) from exc


def _discover_python_files(
    paths: __.cabc.Sequence[ str ]
) -> tuple[ __.pathlib.Path, ... ]:
    ''' Discovers Python files from file paths or directories. '''
    python_files: list[ __.pathlib.Path ] = [ ]
    for path_str in paths:
        path = __.pathlib.Path( path_str )
        if not path.exists( ):
            continue
        if path.is_file( ) and path.suffix == '.py':
            python_files.append( path )
        elif path.is_dir( ):
            python_files.extend( path.rglob( '*.py' ) )
    return tuple( sorted( set( python_files ) ) )


def _apply_path_filters(
    file_paths: tuple[ __.pathlib.Path, ... ],
    config: __.typx.Any,
) -> tuple[ __.pathlib.Path, ... ]:
    ''' Applies include/exclude path filters from configuration. '''
    typed_config = __.typx.cast( _configuration.Configuration, config )
    filtered = list( file_paths )
    if not __.is_absent( typed_config.include_paths ):
        filtered = [
            fp for fp in filtered
            if _matches_any_pattern( fp, typed_config.include_paths )
        ]
    if not __.is_absent( typed_config.exclude_paths ):
        patterns = typed_config.exclude_paths
        filtered = [
            fp for fp in filtered
            if not _matches_any_pattern( fp, patterns )
        ]
    return tuple( filtered )


def _matches_any_pattern(
    file_path: __.pathlib.Path,
    patterns: tuple[ str, ... ],
) -> bool:
    ''' Checks if file path matches any glob pattern. '''
    path_str = str( file_path )
    for pattern in patterns:
        if __.wcglob.globmatch(
            path_str, pattern, flags = __.wcglob.GLOBSTAR ):
            return True
    return False


def _merge_context_size(
    cli_context: int,
    config: __.Absential[ __.typx.Any ],
) -> int:
    ''' Merges context size from CLI and configuration. '''
    if cli_context > 0:
        return cli_context
    if __.is_absent( config ):
        return 0
    typed_config = __.typx.cast( _configuration.Configuration, config )
    if __.is_absent( typed_config.context ):
        return 0
    return typed_config.context


def _merge_rule_selection(
    cli_selection: __.Absential[ str ],
    config: __.Absential[ __.typx.Any ],
) -> frozenset[ str ]:
    ''' Merges rule selection from CLI and configuration. '''
    from .rules.implementations.__ import RULE_DESCRIPTORS
    all_rules = frozenset( RULE_DESCRIPTORS.keys( ) )
    if not __.is_absent( cli_selection ):
        codes = cli_selection.split( ',' )
        return frozenset( code.strip( ) for code in codes )
    if __.is_absent( config ):
        return all_rules
    typed_config = __.typx.cast( _configuration.Configuration, config )
    if not __.is_absent( typed_config.select ):
        selected = set( typed_config.select )
    else:
        selected = set( all_rules )
    if not __.is_absent( typed_config.exclude_rules ):
        selected -= set( typed_config.exclude_rules )
    return frozenset( selected )


async def _render_and_print_result(
    result: RenderableResult,
    display: DisplayOptions,
    exits: __.ctxl.AsyncExitStack,
) -> None:
    ''' Renders and prints a result object based on display options. '''
    stream = await display.provide_stream( exits )
    match display.format:
        case DisplayFormats.Json:
            stream.write( __.json.dumps( result.render_as_json( ) ) )
            stream.write( '\n' )
        case DisplayFormats.Text:
            for line in result.render_as_text( ):
                stream.write( line )
                stream.write( '\n' )
