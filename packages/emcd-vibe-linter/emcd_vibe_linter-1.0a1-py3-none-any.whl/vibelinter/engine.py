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



''' Central linter engine coordinating single-pass CST analysis. '''


from . import __
from . import exceptions as _exceptions
from .rules import context as _context
from .rules import registry as _registry
from .rules import violations as _violations
from .rules.base import BaseRule as _BaseRule


def _create_empty_rule_parameters( ) -> __.immut.Dictionary[
    str, __.immut.Dictionary[ str, __.typx.Any ] ]:
    ''' Creates empty rule parameters dictionary. '''
    return __.immut.Dictionary( )


class EngineConfiguration( __.immut.DataclassObject ):
    ''' Configuration for linter engine behavior and rule selection. '''

    enabled_rules: __.typx.Annotated[
        frozenset[ str ],
        __.ddoc.Doc( 'VBL codes of rules to execute.' ) ]
    rule_parameters: __.typx.Annotated[
        __.immut.Dictionary[
            str, __.immut.Dictionary[ str, __.typx.Any ] ],
        __.ddoc.Doc(
            'Rule-specific configuration parameters indexed by VBL code.'
        ) ] = __.dcls.field( default_factory = _create_empty_rule_parameters )
    context_size: __.typx.Annotated[
        int,
        __.ddoc.Doc(
            'Number of context lines to extract around violations.' ) ] = 2
    include_context: __.typx.Annotated[
        bool,
        __.ddoc.Doc(
            'Whether to extract source context for violations.' ) ] = True


class Report( __.immut.DataclassObject ):
    ''' Results of linting analysis including violations and metadata. '''

    violations: __.typx.Annotated[
        tuple[ _violations.Violation, ... ],
        __.ddoc.Doc( 'All violations detected during analysis.' ) ]
    contexts: __.typx.Annotated[
        tuple[ _violations.ViolationContext, ... ],
        __.ddoc.Doc( 'Violation contexts when context extraction enabled.' ) ]
    filename: __.typx.Annotated[
        str, __.ddoc.Doc( 'Path to analyzed source file.' ) ]
    rule_count: __.typx.Annotated[
        int, __.ddoc.Doc( 'Number of rules executed during analysis.' ) ]
    analysis_duration_ms: __.typx.Annotated[
        float,
        __.ddoc.Doc( 'Time spent in analysis phase excluding parsing.' ) ]


class Engine:
    ''' Central orchestrator for linting analysis.

        Implements single-pass CST traversal with multiple rule execution.
    '''

    def __init__(
        self,
        registry_manager: __.typx.Annotated[
            _registry.RuleRegistryManager,
            __.ddoc.Doc( 'Rule registry for instantiating rules.' ) ],
        configuration: __.typx.Annotated[
            EngineConfiguration,
            __.ddoc.Doc( 'Engine configuration and rule selection.' ) ],
    ) -> None:
        self.registry_manager = registry_manager
        self.configuration = configuration

    def lint_file(
        self,
        file_path: __.typx.Annotated[
            __.pathlib.Path,
            __.ddoc.Doc( 'Path to Python source file to analyze.' ) ]
    ) -> __.typx.Annotated[
        Report,
        __.ddoc.Doc(
            'Analysis results including violations and metadata.' ) ]:
        ''' Analyzes a Python source file and returns violations. '''
        source_code = file_path.read_text( encoding = 'utf-8' )
        return self.lint_source( source_code, str( file_path ) )

    def _create_metadata_wrapper(
        self, source_code: str, filename: str
    ) -> tuple[ __.libcst.metadata.MetadataWrapper, tuple[ str, ... ] ]:
        ''' Parses source and creates metadata wrapper. '''
        module = __.libcst.parse_module( source_code )
        source_lines = tuple( source_code.splitlines( ) )
        try: wrapper = __.libcst.metadata.MetadataWrapper( module )
        except Exception as exc:
            raise _exceptions.MetadataProvideFailure( filename ) from exc
        return wrapper, source_lines

    def _instantiate_rules(
        self,
        wrapper: __.libcst.metadata.MetadataWrapper,
        source_lines: tuple[ str, ... ],
        filename: str
    ) -> list[ _BaseRule ]:
        ''' Instantiates all enabled rules with configuration. '''
        rules: list[ _BaseRule ] = [ ]
        for vbl_code in self.configuration.enabled_rules:
            params = self.configuration.rule_parameters.get(
                vbl_code, __.immut.Dictionary( ) )
            try:
                rule = self.registry_manager.produce_rule_instance(
                    vbl_code = vbl_code,
                    filename = filename,
                    wrapper = wrapper,
                    source_lines = source_lines,
                    **params )
                rules.append( rule )
            except Exception as exc:
                raise _exceptions.RuleExecuteFailure( vbl_code ) from exc
        return rules

    def _execute_rules(
        self,
        rules: list[ _BaseRule ],
        wrapper: __.libcst.metadata.MetadataWrapper
    ) -> None:
        ''' Executes rules via single-pass CST traversal. '''
        for rule in rules:
            try: wrapper.visit( rule )
            except Exception as exc:  # noqa: PERF203
                raise _exceptions.RuleExecuteFailure( rule.rule_id ) from exc

    def _collect_violations(
        self, rules: list[ _BaseRule ]
    ) -> list[ _violations.Violation ]:
        ''' Collects and sorts violations from all rules. '''
        all_violations: list[ _violations.Violation ] = [ ]
        for rule in rules:
            all_violations.extend( rule.violations )
        all_violations.sort( key = lambda v: ( v.line, v.column ) )
        return all_violations

    def lint_source(
        self,
        source_code: __.typx.Annotated[
            str,
            __.ddoc.Doc( 'Python source code to analyze.' ) ],
        filename: __.typx.Annotated[
            str,
            __.ddoc.Doc( 'Logical filename for source code.' ) ] = '<string>',
    ) -> __.typx.Annotated[
        Report,
        __.ddoc.Doc(
            'Analysis results including violations and metadata.' ) ]:
        ''' Analyzes Python source code and returns violations. '''
        analysis_start_time = __.time.perf_counter( )
        wrapper, source_lines = self._create_metadata_wrapper(
            source_code, filename )
        rules = self._instantiate_rules( wrapper, source_lines, filename )
        self._execute_rules( rules, wrapper )
        all_violations = self._collect_violations( rules )
        violation_contexts: tuple[
            _violations.ViolationContext, ... ] = ( )
        if self.configuration.include_context and all_violations:
            violation_contexts = _context.extract_contexts_for_violations(
                all_violations,
                source_lines,
                self.configuration.context_size )
        analysis_duration_ms = (
            ( __.time.perf_counter( ) - analysis_start_time ) * 1000 )
        return Report(
            violations = tuple( all_violations ),
            contexts = violation_contexts,
            filename = filename,
            rule_count = len( rules ),
            analysis_duration_ms = analysis_duration_ms )

    def lint_files(
        self,
        file_paths: __.typx.Annotated[
            __.cabc.Sequence[ __.pathlib.Path ],
            __.ddoc.Doc( 'Paths to Python source files to analyze.' ) ]
    ) -> __.typx.Annotated[
        tuple[ Report, ... ],
        __.ddoc.Doc( 'Analysis results for all files.' ) ]:
        ''' Analyzes multiple Python source files. '''
        reports: list[ Report ] = [ ]
        for file_path in file_paths:
            try: report = self.lint_file( file_path )
            except Exception: continue  # noqa: S112
            reports.append( report )
        return tuple( reports )
