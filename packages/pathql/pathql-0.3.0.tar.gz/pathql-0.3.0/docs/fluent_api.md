# PQuery Enhanced Fluent API

## Overview

The PQuery API has been enhanced with a fluent builder pattern that allows for intuitive and flexible file system queries. You can now chain methods in any order to build complex queries.

## Key Features

### Default Constructor
```python
# Default to current directory
q = PQuery()  # Searches current directory recursively
```

### Chainable From Methods
```python
# Single path
q = PQuery().from_(path)

# Multiple paths - from_() replaces, from_path() adds
q = PQuery().from_(path1).from_path(path2).from_path(path3)
```

### Recursive Control
```python
# Control recursive behavior
q = PQuery().recursive(True)   # Search subdirectories (default)
q = PQuery().recursive(False)  # Only search specified directories
```

### Method Chaining
```python
# Methods can be chained in any order (except where() should be last)
q = PQuery().from_(src_dir).from_path(test_dir).recursive(True).where(lambda p: p.suffix == ".py")
q = PQuery().recursive(False).from_(config_dir).where(lambda p: "config" in p.name)
```

## Complete Example
```python
from tpath.pquery import PQuery

# Build a complex query
large_python_files = (PQuery()
                     .from_("src")
                     .from_path("scripts") 
                     .from_path("tools")
                     .recursive(True)
                     .where(lambda p: p.suffix == ".py" and p.size.bytes > 1000)
                     .files())

# Use different result methods
query = PQuery().from_("logs").where(lambda p: p.suffix == ".log")

files = query.files()              # List of files
first = query.first()              # First match
exists = query.exists()            # Boolean
count = query.count()              # Number of matches
names = query.select(lambda p: p.name)  # Extract properties

# Direct iteration
for log_file in query:
    print(f"Log: {log_file.name} ({log_file.size.bytes} bytes)")
```

## Backwards Compatibility

The original `pquery()` function still works:
```python
from tpath.pquery import pquery

# Old style still supported
old_style = pquery(from_="src").where(lambda p: p.suffix == ".py").files()

# New fluent style
new_style = PQuery().from_("src").where(lambda p: p.suffix == ".py").files()
```

## Package Structure

```
src/tpath/pquery/
├── __init__.py          # Package exports
├── _pquery.py           # Core PQuery implementation
└── ...

test/pquery/
├── test_pquery.py       # Original tests
├── test_pquery_comprehensive.py  # Edge case tests  
├── test_fluent_api.py   # Fluent API tests
└── ...
```

## Test Coverage

- **28 pquery-specific tests** covering all functionality
- **134 total tests** in the full test suite
- **100% backwards compatibility** maintained

The enhanced API provides a modern, chainable interface while maintaining full compatibility with existing code.