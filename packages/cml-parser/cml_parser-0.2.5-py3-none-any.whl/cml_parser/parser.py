from dataclasses import asdict
from pathlib import Path
from typing import List, Optional, Any, Union
import argparse
import json
import sys
import os

from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

from .antlr.CMLLexer import CMLLexer
from .antlr.CMLParser import CMLParser
from .cml_model_builder import CMLModelBuilder
from .cml_objects import (
    CML,
    ParseResult,
    Diagnostic,
    Domain,
    Subdomain,
    SubdomainType,
    ContextMap,
    Context,
    Relationship,
    RelationshipType,
    UseCase,
    Entity,
    ValueObject,
    DomainEvent,
    Enum,
    Aggregate,
    Service,
    Repository,
    Attribute,
    Operation,
    Parameter
)

class CmlSyntaxError(Exception):
    def __init__(self, diagnostic: Diagnostic):
        super().__init__(diagnostic.pretty())
        self.diagnostic = diagnostic

class CMLErrorListener(ErrorListener):
    def __init__(self, filename: str = None):
        super().__init__()
        self.filename = filename
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(Diagnostic(
            message=msg,
            line=line,
            col=column,
            filename=self.filename
        ))

def parse_file(file_path) -> CML:
    """
    Strict parsing of a .cml file. Raises CmlSyntaxError on failure.
    """
    return _parse_internal(path=file_path, text=None, strict=True)

def parse_file_safe(file_path) -> CML:
    return _parse_internal(path=file_path, text=None, strict=False)

def parse_text(text: str, *, filename: Optional[str] = None, strict: bool = True) -> CML:
    return _parse_internal(path=filename, text=text, strict=strict)

def _parse_internal(path: Optional[str], text: Optional[str], strict: bool) -> CML:
    filename = str(path) if path else None
    source = text
    if path and source is None:
        source = Path(path).read_text(encoding="utf-8")
    
    input_stream = InputStream(source)
    lexer = CMLLexer(input_stream)
    
    # Custom error listener
    error_listener = CMLErrorListener(filename)
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)
    
    token_stream = CommonTokenStream(lexer)
    parser = CMLParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    
    # Parse
    tree = parser.definitions()
    
    errors = error_listener.errors
    if errors and strict:
        raise CmlSyntaxError(errors[0])
        
    # Build model if no critical errors (or even if there are, try best effort)
    cml = CML()
    if not errors or not strict:  # pragma: no branch
        try:
            builder = CMLModelBuilder(filename)
            cml = builder.visit(tree)
        except Exception as e:
            # Capture builder errors
            errors.append(Diagnostic(message=f"Model building error: {str(e)}", filename=filename))
            if strict:
                raise CmlSyntaxError(errors[-1]) from e

    model = cml if not errors else None

    parse_result = ParseResult(
        model=model,  # Only expose model when parsing succeeded
        errors=errors,
        warnings=[],
        source=source,
        filename=filename
    )
    
    cml.parse_results = parse_result # Attach parse result to CML object
    
    return cml

def main(argv=None) -> int:
    """
    Minimal CLI entrypoint to parse a single .cml file.
    """
    args = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(prog="cml-parse", add_help=True)
    parser.add_argument("file", nargs="?", help="Path to .cml file")
    parser.add_argument("--json", action="store_true", help="Emit parse result as JSON")
    parser.add_argument("--summary", action="store_true", help="Print a short success summary")
    parsed = parser.parse_args(args)

    if not parsed.file:
        parser.print_usage(file=sys.stderr)
        return 1

    cml = parse_file_safe(parsed.file)
    if not cml.parse_results.ok:
        print(f"Error parsing {parsed.file}:", file=sys.stderr)
        for err in cml.parse_results.errors:
            print(err.pretty(), file=sys.stderr)
        return 1

    if parsed.json:
        print(json.dumps(cml.parse_results.to_dict(), default=str, indent=2))
        return 0
        
    if parsed.summary:
        print(f"Successfully parsed {parsed.file}")
        print(f"Domains: {len(cml.domains)}")
        print(f"Context Maps: {len(cml.context_maps)}")
        return 0

    print(f"Successfully parsed {parsed.file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
