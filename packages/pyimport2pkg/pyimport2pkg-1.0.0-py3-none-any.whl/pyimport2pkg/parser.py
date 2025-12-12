"""
Parser module: Parses Python files and extracts import statements.

Uses AST to analyze Python source code and extract all import information
including context (conditional, try-except, function scope, etc.).
"""

import ast
from pathlib import Path
from typing import Iterator

from .models import ImportInfo, ImportType, ImportContext


class ImportVisitor(ast.NodeVisitor):
    """
    AST visitor that extracts import statements with context information.
    """

    def __init__(self, source: str, file_path: Path | None = None):
        self.source = source
        self.source_lines = source.splitlines()
        self.file_path = file_path
        self.imports: list[ImportInfo] = []
        self._context_stack: list[ImportContext] = [ImportContext.TOP_LEVEL]

    def _get_current_context(self) -> ImportContext:
        """Get the current import context."""
        return self._context_stack[-1]

    def _get_source_line(self, lineno: int) -> str:
        """Get the source line at the given line number."""
        if 0 < lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1].strip()
        return ""

    def _is_optional_context(self) -> bool:
        """Check if current context makes the import optional."""
        ctx = self._get_current_context()
        return ctx in (ImportContext.TRY_EXCEPT, ImportContext.CONDITIONAL)

    def _create_import_info(
        self,
        module_name: str,
        node: ast.AST,
        import_type: ImportType,
        is_relative: bool = False,
    ) -> ImportInfo:
        """Create an ImportInfo object from parsed data."""
        parts = module_name.split(".")
        statement = self._get_source_line(node.lineno)

        return ImportInfo(
            module_name=module_name,
            top_level=parts[0],
            sub_modules=parts[1:] if len(parts) > 1 else [],
            file_path=self.file_path,
            line_number=node.lineno,
            import_statement=statement,
            import_type=import_type,
            context=self._get_current_context(),
            is_optional=self._is_optional_context(),
            is_relative=is_relative,
        )

    def visit_Import(self, node: ast.Import) -> None:
        """Handle: import xxx, import xxx.yyy"""
        for alias in node.names:
            module_name = alias.name
            info = self._create_import_info(
                module_name=module_name,
                node=node,
                import_type=ImportType.STANDARD,
            )
            self.imports.append(info)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Handle: from xxx import yyy, from . import yyy"""
        # Check for relative import
        is_relative = node.level > 0

        if is_relative:
            # Relative import - we'll record it but mark as relative
            # The module name might be empty for "from . import x"
            module_name = node.module or ""
            info = self._create_import_info(
                module_name=module_name,
                node=node,
                import_type=ImportType.FROM,
                is_relative=True,
            )
            self.imports.append(info)
        else:
            # Absolute import
            if node.module:
                info = self._create_import_info(
                    module_name=node.module,
                    node=node,
                    import_type=ImportType.FROM,
                )
                self.imports.append(info)

        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """Track conditional context."""
        self._context_stack.append(ImportContext.CONDITIONAL)
        self.generic_visit(node)
        self._context_stack.pop()

    def visit_Try(self, node: ast.Try) -> None:
        """Track try-except context."""
        # Visit try body with TRY_EXCEPT context
        self._context_stack.append(ImportContext.TRY_EXCEPT)
        for stmt in node.body:
            self.visit(stmt)
        self._context_stack.pop()

        # Visit except handlers with TRY_EXCEPT context
        self._context_stack.append(ImportContext.TRY_EXCEPT)
        for handler in node.handlers:
            for stmt in handler.body:
                self.visit(stmt)
        self._context_stack.pop()

        # Visit else and finally without special context
        for stmt in node.orelse:
            self.visit(stmt)
        for stmt in node.finalbody:
            self.visit(stmt)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Track function context."""
        self._context_stack.append(ImportContext.FUNCTION)
        self.generic_visit(node)
        self._context_stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Track async function context."""
        self._context_stack.append(ImportContext.FUNCTION)
        self.generic_visit(node)
        self._context_stack.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Track class context."""
        self._context_stack.append(ImportContext.CLASS)
        self.generic_visit(node)
        self._context_stack.pop()

    def visit_Call(self, node: ast.Call) -> None:
        """Detect dynamic imports like importlib.import_module()."""
        if self._is_import_module_call(node):
            self._handle_dynamic_import(node)
        self.generic_visit(node)

    def _is_import_module_call(self, node: ast.Call) -> bool:
        """Check if this is a call to importlib.import_module or __import__."""
        # Check for __import__('xxx')
        if isinstance(node.func, ast.Name) and node.func.id == "__import__":
            return True

        # Check for importlib.import_module('xxx')
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "import_module":
                # Could be importlib.import_module or importlib.util.import_module
                return True

        return False

    def _handle_dynamic_import(self, node: ast.Call) -> None:
        """Handle dynamic import calls."""
        if not node.args:
            return

        first_arg = node.args[0]

        # Try to extract the module name if it's a string literal
        if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
            module_name = first_arg.value
            info = self._create_import_info(
                module_name=module_name,
                node=node,
                import_type=ImportType.DYNAMIC,
            )
            info.is_dynamic = True
            info.warnings.append(
                f"Dynamic import detected at line {node.lineno}. "
                "Please verify this package is needed."
            )
            self.imports.append(info)
        else:
            # Can't statically determine the module name
            info = ImportInfo(
                module_name="<dynamic>",
                top_level="<dynamic>",
                file_path=self.file_path,
                line_number=node.lineno,
                import_statement=self._get_source_line(node.lineno),
                import_type=ImportType.DYNAMIC,
                context=self._get_current_context(),
                is_dynamic=True,
                warnings=[
                    f"Dynamic import with non-literal argument at line {node.lineno}. "
                    "Cannot statically determine the module name. Manual review required."
                ],
            )
            self.imports.append(info)


class Parser:
    """
    Parser for extracting import statements from Python source code.
    """

    def parse_source(
        self,
        source: str,
        file_path: Path | None = None,
    ) -> list[ImportInfo]:
        """
        Parse Python source code and extract import statements.

        Args:
            source: Python source code string
            file_path: Optional path to the source file (for error reporting)

        Returns:
            List of ImportInfo objects
        """
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            # Return empty list with a warning for syntax errors
            info = ImportInfo(
                module_name="<syntax_error>",
                top_level="<syntax_error>",
                file_path=file_path,
                line_number=e.lineno or 0,
                warnings=[f"Syntax error: {e.msg}"],
            )
            return [info]

        visitor = ImportVisitor(source, file_path)
        visitor.visit(tree)
        return visitor.imports

    def parse_file(self, file_path: Path) -> list[ImportInfo]:
        """
        Parse a Python file and extract import statements.

        Args:
            file_path: Path to the Python file

        Returns:
            List of ImportInfo objects
        """
        file_path = Path(file_path)

        try:
            source = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Try with latin-1 as fallback
            try:
                source = file_path.read_text(encoding="latin-1")
            except Exception as e:
                return [
                    ImportInfo(
                        module_name="<read_error>",
                        top_level="<read_error>",
                        file_path=file_path,
                        warnings=[f"Failed to read file: {e}"],
                    )
                ]
        except Exception as e:
            return [
                ImportInfo(
                    module_name="<read_error>",
                    top_level="<read_error>",
                    file_path=file_path,
                    warnings=[f"Failed to read file: {e}"],
                )
            ]

        return self.parse_source(source, file_path)

    def parse_files(self, file_paths: list[Path]) -> Iterator[ImportInfo]:
        """
        Parse multiple Python files.

        Args:
            file_paths: List of paths to Python files

        Yields:
            ImportInfo objects from all files
        """
        for file_path in file_paths:
            yield from self.parse_file(file_path)


def parse_source(source: str, file_path: Path | None = None) -> list[ImportInfo]:
    """
    Convenience function to parse Python source code.

    Args:
        source: Python source code string
        file_path: Optional path for error reporting

    Returns:
        List of ImportInfo objects
    """
    parser = Parser()
    return parser.parse_source(source, file_path)


def parse_file(file_path: Path) -> list[ImportInfo]:
    """
    Convenience function to parse a Python file.

    Args:
        file_path: Path to the Python file

    Returns:
        List of ImportInfo objects
    """
    parser = Parser()
    return parser.parse_file(file_path)
