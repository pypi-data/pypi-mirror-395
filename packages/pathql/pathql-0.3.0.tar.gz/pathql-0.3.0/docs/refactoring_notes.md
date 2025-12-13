# PQuery Lazy Initialization Refactoring

## Before: Complex _ensure_defaults_applied() method

```python
def _ensure_defaults_applied(self) -> None:
    """Apply default values if they haven't been set explicitly."""
    # Apply from_ default
    if not self.start_paths:
        if self._init_from is not None:
            self.start_paths = [TPath(self._init_from)]
        else:
            self.start_paths = [TPath('.')]
    
    # Apply recursive default  
    if self._init_recursive is not None:
        self.is_recursive = self._init_recursive
    else:
        self.is_recursive = True
        
    # Apply where default
    if self._query_func is None:
        if self._init_where is not None:
            self._query_func = self._init_where
        else:
            # Default to files only (exclude directories)
            self._query_func = lambda p: p.is_file()

def _iter_files(self) -> Iterator[TPath]:
    """Internal method to iterate over all matching files."""
    # Ensure defaults are applied before running query
    self._ensure_defaults_applied()
    
    # _query_func should never be None after applying defaults
    assert self._query_func is not None, "Query function should be set after applying defaults"
        
    for start_path in self.start_paths:
        # ... rest of method
```

## After: Simple null coalescing pattern

```python
def _iter_files(self) -> Iterator[TPath]:
    """Internal method to iterate over all matching files."""
    # Apply defaults using null coalescing
    if not self.start_paths:
        default_path = self._init_from or '.'
        self.start_paths = [TPath(default_path)]
    
    self.is_recursive = self._init_recursive if self._init_recursive is not None else True
    
    if self._query_func is None:
        self._query_func = self._init_where or (lambda p: p.is_file())
        
    for start_path in self.start_paths:
        # ... rest of method
```

## Benefits of the refactoring:

1. **Removed 20+ lines of code** - eliminated entire `_ensure_defaults_applied()` method
2. **Simpler logic** - direct null coalescing instead of complex if/else chains  
3. **More readable** - `self._init_from or '.'` is clearer than nested if statements
4. **Less indirection** - defaults applied directly where needed
5. **Same functionality** - all tests still pass, behavior unchanged

## Key patterns used:

- `value or default` for simple cases
- `value if value is not None else default` for boolean values (to handle `False` correctly)
- Direct assignment at point of use rather than separate initialization method

This refactoring demonstrates how Python's null coalescing operators can make code much cleaner and more maintainable while preserving the exact same functionality.