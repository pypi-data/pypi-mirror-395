"""Structured validation errors with JSON path tracking."""

from collections import defaultdict


class ValidationError:
    """Collects validation errors with bi-directional lookups.

    Supports querying by path or error type.
    Displays grouped, concise error messages.

    Examples:
        >>> err = ValidationError()
        >>> err.add("$.name", "missing")
        >>> err.add("$.age", "missing")
        >>> err.add("$.email", "format", "invalid email")
        >>> print(err)
        Missing required fields: name, age
        email: invalid email

        >>> err.for_type("missing")
        ['$.name', '$.age']

        >>> err.for_path("$.email")
        [('format', 'invalid email')]
    """

    # Error types
    MISSING = "missing"
    EXTRA = "extra"
    TYPE = "type"
    FORMAT = "format"
    RANGE = "range"
    ENUM = "enum"

    def __init__(self):
        self._by_path = defaultdict(list)  # path -> [(type, msg), ...]
        self._by_type = defaultdict(list)  # type -> [path, ...]

    def add(self, path: str, error_type: str, message: str = ""):
        """Add error at path.

        Args:
            path: JSON path (e.g., "$.name", "$.items[0].price")
            error_type: Error type (use constants: MISSING, EXTRA, etc.)
            message: Optional detail message
        """
        self._by_path[path].append((error_type, message))
        if path not in self._by_type[error_type]:
            self._by_type[error_type].append(path)

    def for_path(self, path: str) -> list[tuple[str, str]]:
        """Get all (type, message) tuples for a path."""
        return self._by_path.get(path, [])

    def for_type(self, error_type: str) -> list[str]:
        """Get all paths with this error type."""
        return self._by_type.get(error_type, [])

    def __bool__(self) -> bool:
        """True if any errors exist."""
        return bool(self._by_path)

    def __str__(self) -> str:
        """Format errors grouped by type, concise."""
        if not self._by_path:
            return ""

        lines = []

        # Missing fields - group together
        if self.MISSING in self._by_type:
            fields = [p.lstrip("$.") for p in self._by_type[self.MISSING]]
            lines.append(f"Missing required fields: {', '.join(fields)}")

        # Extra fields - group together
        if self.EXTRA in self._by_type:
            fields = [p.lstrip("$.") for p in self._by_type[self.EXTRA]]
            lines.append(f"Unknown fields: {', '.join(fields)}")

        # Type/format/range/enum - show individually with context
        for error_type in [self.TYPE, self.FORMAT, self.RANGE, self.ENUM]:
            if error_type in self._by_type:
                for path in self._by_type[error_type]:
                    field = path.lstrip("$.")
                    for etype, msg in self._by_path[path]:
                        if etype == error_type and msg:
                            lines.append(f"{field}: {msg}")

        return "\n".join(lines)

    __repr__ = __str__
