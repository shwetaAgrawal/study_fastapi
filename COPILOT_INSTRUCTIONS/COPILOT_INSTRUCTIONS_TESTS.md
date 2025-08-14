You are provided with the test_ and source code files. Analyze the source, then critically review the test_ file to identify missing test cases. Once identified, IMPLEMENT these. 

# GUIDELINES FOR IMPLEMENTING TESTS
## CORE PRINCIPLES

### 1. Editing Scope and Test Modifications
- **Scope**: Only modify test modules (filenames starting with `test_`). Do not change any `src/` files.

### 2. Required File Structure
Each test file must have this exact order:
1. Module docstring  
2. Imports
3. **Exactly one** `### Proposed Test Cases` section (see Planning Phase below)
   - **CRITICAL**: This section must be a COMMENT block, not executable code
    - **FOR NEW FILES ONLY**: Place immediately after imports, before any executable code
    - **FOR EXISTING FILES**: If the section exists, update it in-place. If none exists, **append it at the END of the file** to avoid reordering existing code.
4. Module-level fixtures and helper functions  
5. Test classes and functions  

**Example of proper placement in NEW files:**
```python
"""Module docstring here."""

import pytest
from src.module import MyClass

### Proposed Test Cases
# [IMPLEMENTED] `test_existing_method`: Already implemented test case.
# `test_new_method_scenario`: Brief one-line description of new test needed.

# End of Proposed Test Cases section

@pytest.fixture
def sample_fixture():
    return {"key": "value"}

class TestMyClass:
    def test_existing_method(self):
        # existing test code
        pass
```

**IMPORTANT**: When editing existing files:
- **UPDATE** existing test cases in the "Proposed Test Cases" section in-place
- **APPEND** new test cases to the existing "Proposed Test Cases" section if it exists
- **IF NO SECTION EXISTS**: **Create it at the END of the file** (not between imports and code) to minimize diff noise
- **MODIFY** existing test methods in-place when improvements are needed
- **ADD** new test methods at appropriate locations within existing test classes

### 3. Test File Path Structure
**CRITICAL**: Test files must mirror the source directory structure:
- **Source file**: `src/module/submodule/component.py`
- **Test file**: `tests/module/submodule/test_component.py`
- **Always prefix test filenames with `test_`**

**Examples**:
- Source: `src/core/agentic/rag_base.py` → Test: `tests/core/agentic/test_rag_base.py`
- Source: `src/agents/product_agent.py` → Test: `tests/agents/test_product_agent.py`
- Source: `src/utils/cache.py` → Test: `tests/utils/test_cache.py`

**When creating new test files**:
1. Create the full directory structure if it doesn't exist
2. Follow the exact source path hierarchy under `tests/`
3. Ensure test file names start with `test_`

## TEST IMPLEMENTATION WORKFLOW

### Analysis Phase
- Read source code completely; note public APIs, branches, loops, async paths, and error handling.
- Compare with existing tests to find coverage gaps using the methodology below.

### Planning Phase
- **Proposed Test Cases Section**: 
  - **FOR NEW FILES**: Must appear immediately after imports AS A COMMENT BLOCK
  - **FOR EXISTING FILES**: 
        - If section exists: Update existing section in-place
        - If no section exists: Create at END of file, not between imports and code
  - **CRITICAL PLACEMENT RULES**:
    - **New file**: Place after imports, before any code
        - **Existing file**: UPDATE existing section in-place, or create at end if none exists
  - **If section exists**: 
    - Review existing items
    - Mark completed items with `[IMPLEMENTED]` prefix in-place
    - Update existing test case descriptions if they need improvement
    - Append only NEW test cases that aren't already listed or implemented
    - **If section doesn't exist in existing file**: Create it at the END of the file (not between imports and code)  

### Implementation Phase

**CRITICAL EDITING RULES**:
- **MODIFY** existing test methods in-place when improvements are identified
- **ADD** new test methods within existing test classes at appropriate locations
- **UPDATE** existing fixtures in-place when enhancements are needed
- Create new test classes AFTER existing classes only when testing new components
- When adding fixtures, place them with other fixtures or update existing ones in-place

Implement tests in this priority order:
1. Core functionality tests (missing happy paths)
2. Edge cases and boundary conditions  
3. Error scenarios and exception handling
4. Integration tests  

### Verification Phase
- Verify imports, signatures, async usage, fixture availability, and logical assertions.
- Apply DRY principles: extract common setup into fixtures, use `@pytest.mark.parametrize`, remove unused code.

## TEST COVERAGE ANALYSIS METHODOLOGY

### 1. Code Path Coverage Analysis
- **Public methods** and their parameters
- **Conditional branches** (if/else, try/catch, match/case statements)
- **Loop constructs** and edge cases (empty collections, single items)
- **Async operations** and error handling
- **Configuration flags** and feature toggles

### 2. Data Flow Analysis
- **Input validation** (valid, invalid, edge cases)
- **State transitions** (initialization → processing → completion)
- **Error propagation** and exception handling
- **Side effects** (file I/O, network calls, cache updates, logging)

### 3. Integration Points Analysis
- **External dependencies** (APIs, databases, file systems)
- **Class collaborations** and object interactions
- **Inheritance hierarchies**
- **Event handling** (callbacks, async generators)

## MISSING TEST CASE IDENTIFICATION

Look for these common gaps:

### 1. Boundary Conditions
- Empty inputs (`""`, `None`, `[]`, `{}`)
- Maximum/minimum values for numeric inputs
- Unicode/special characters in strings
- Large datasets that might cause performance issues

### 2. Error Scenarios
- Network timeouts and connection failures
- Invalid API responses (malformed JSON, unexpected schemas)
- File system errors (permissions, disk space, missing files)
- Memory limitations and resource exhaustion

### 3. Concurrency and Timing
- Race conditions in async code
- Multiple simultaneous operations
- Timeout handling
- Resource cleanup in error scenarios
- **Flaky tests** that pass or fail intermittently without code changes

### 4. Configuration Variations
- Different environment variables
- Missing configuration values
- Invalid configuration formats
- Feature flag combinations

## IMPLEMENTATION BEST PRACTICES

### 1. Fixture Organization Decision Tree
**Use this decision tree to determine fixture placement:**

1. **Is the fixture needed by multiple test modules across different directories?**
   - YES → Place in `tests/conftest.py` (Global Fixtures)
   - NO → Continue to step 2

2. **Is the fixture needed by multiple test files in the same directory?**
   - YES → Place in local `conftest.py` in that directory (Component Fixtures)  
   - NO → Continue to step 3

3. **Is the fixture only needed by one test module?**
   - YES → Place in the test file itself (Local Fixtures)

**Examples:**
- **Global Fixtures** (`tests/conftest.py`): `MockAzureOpenAI`, `disable_azure_monitor`
- **Component Fixtures** (`tests/agents/conftest.py`): Agent-specific mocks used by multiple agent test files
- **Local Fixtures** (in test file): Setup specific to testing one class or module

### 2. Mocking and Patching Patterns

**CRITICAL: To bypass Pydantic validation errors, inherit mock classes from actual classes:**

```python
# Mock subclasses for type checking compatibility and Pydantic validation
class MockAzureOpenAI(AzureOpenAI):
    """A mock class that inherits from AzureOpenAI to pass Pydantic's isinstance checks."""
    def __init__(self, *args, **kwargs):
        # Override __init__ to prevent the real initialization
        self.chat = MagicMock()
        self.embeddings = MagicMock()
        self.chat.completions.create = MagicMock(return_value="mock completion")

class MockSearchClient(SearchClient):
    """A mock class that inherits from SearchClient to pass Pydantic validation."""
    def __init__(self, *args, **kwargs):
        self.search = MagicMock()
        self.get_document = MagicMock()
```

**Why this pattern is essential:**
- Pydantic models perform `isinstance()` checks that fail with standard `MagicMock` objects
- Inheriting from the actual class ensures type compatibility while allowing full mock control
- Prevents `ValidationError` exceptions during test execution
- Maintains test isolation while satisfying framework requirements

**Standard mocking patterns:**
```python
# Isolate dependencies with monkeypatch in autouse fixtures
@pytest.fixture(autouse=True)
def setup_patches(monkeypatch, mock_env_vars):
    for key, value in mock_env_vars.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setattr("src.module.Class", MockClass)
```

### 3. Parametrization for Scalable Testing
**Use `@pytest.mark.parametrize` to test multiple scenarios with a single test function.** This is the preferred method for testing boundary conditions, configuration variations, and error scenarios without duplicating code.

**Example:**
```python
@pytest.mark.parametrize(
    "input_value, expected_output, error_type",
    [
        ("valid_input", {"status": "success"}, None),  # happy path
        ("", None, ValueError),                           # empty input
        (None, None, ValueError),                          # None input
        ("invalid_format", None, TypeError),              # error scenario
    ],
    ids=["happy", "empty", "none", "invalid"],
)
def test_processing_logic(input_value, expected_output, error_type):
    """Test processing logic across multiple valid, edge, and error cases."""
    # Arrange
    if error_type:
        with pytest.raises(error_type):
            # Act
            process_function(input_value)
    else:
        # Act
        result = process_function(input_value)
        # Assert
        assert result == expected_output
```

### 4. Test Design Standards

#### Naming Conventions
- Test methods: `test_<functionality>_<scenario>`
- Test classes: `Test<ComponentName>`
- Fixtures: Descriptive names (`mock_redis_cache`, `sample_user_query`)

#### Test Structure (Arrange-Act-Assert)
```python
def test_method_with_valid_input(self, fixture_name):
    """Test that method processes valid input correctly."""
    # Arrange
    input_data = {"key": "value"}
    expected_result = {"processed": True}
    
    # Act
    result = method_under_test(input_data)
    
    # Assert
    assert result == expected_result
    assert isinstance(result, dict)
```

#### Test Independence and Atomicity Requirements
**Each test must be completely independent and atomic:**
- **Atomicity**: Each test method should ideally verify one single logical behavior or outcome. Avoid combining multiple unrelated assertions into a single test.
- Use fixtures for all setup/teardown (no manual cleanup in test methods)
- Never rely on test execution order
- Never modify global state directly (use monkeypatch for environment variables)
- Create fresh test data for each test (no shared mutable objects)
- **Exception**: Shared read-only fixtures (like configuration constants) are allowed

### 5. Assertion and Verification Patterns
```python
# Specific assertions with clear failure messages
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
assert isinstance(result, dict), f"Expected dict, got {type(result)}"

# Mock verification
mock_service.method.assert_called_once_with(expected_param=value)
assert mock_service.method1.call_count == 1
```

### 6. Coverage Requirements
Test all paths:
- **Happy Path**: Expected behavior with valid inputs
- **Alternative Paths**: Other valid scenarios (cache hits, different configurations)
- **Edge Cases**: Empty, `None`, or malformed inputs
- **Error Conditions**: Dependency failures and exception handling
- **Configuration Flags**: Feature toggles and environment variations

### 7. Async and Performance Testing
- Use `@pytest.mark.asyncio` for async functions
- Test timeout handling and retry mechanisms
- Verify resource cleanup (file handles, connections)
- Test memory management in long-running operations

### 8. Environment, Time, and IO Testing
- Use `monkeypatch.setenv` to inject environment variables; do not mutate `os.environ` directly.
- Use `monkeypatch.setattr` to stub time (e.g., `time.time`, `datetime.datetime.now`) or leverage libraries like `freezegun`.
- Prefer `tmp_path`/`tmp_path_factory` for filesystem operations; avoid writing into the repo.
- Use `caplog` for logging assertions and `capsys` for stdout/stderr when testing CLIs.

### 9. Marks and Selective Execution
- Use marks like `@pytest.mark.slow`, `@pytest.mark.integration` for long-running or external tests; ensure CI is configured accordingly.
- Keep unit tests fast and deterministic; avoid network and real I/O unless explicitly marked.

### 10. Factory Fixtures Pattern (Reusable Test Data)
Factory fixtures return callables that build fresh test objects with sensible defaults and easy overrides. This keeps tests DRY and independent.

1) Simple dict/data factory
```python
import uuid
import datetime as dt
import pytest

@pytest.fixture
def user_factory():
    """Create user dicts with overridable fields."""
    def make_user(**overrides):
        data = {
            "id": str(uuid.uuid4()),
            "name": "Alice",
            "email": "alice@example.com",
            "created_at": dt.datetime(2025, 1, 1, 0, 0, 0),
            "active": True,
        }
        data.update(overrides)
        return data
    return make_user
```

2) Dataclass/object factory
```python
from dataclasses import dataclass
import pytest

@dataclass
class Order:
    id: str
    amount: int
    status: str = "new"

@pytest.fixture
def order_factory():
    def make_order(**overrides) -> Order:
        base = Order(id="ord_1", amount=100, status="new")
        return Order(**{**base.__dict__, **overrides})
    return make_order
```

3) Composed factories
```python
import pytest

@pytest.fixture
def product_factory():
    def make_product(**overrides):
        data = {"sku": "SKU-1", "price": 10, "tags": []}
        data.update(overrides)
        return data
    return make_product

@pytest.fixture
def cart_factory(product_factory):
    def make_cart(items=None, **overrides):
        items = items or [product_factory(), product_factory(sku="SKU-2", price=20)]
        cart = {"items": items, "total": sum(i["price"] for i in items)}
        cart.update(overrides)
        return cart
    return make_cart
```

4) Parametrized factories
```python
import pytest

@pytest.mark.parametrize(
    "amount, expected_status",
    [(0, "empty"), (50, "partial"), (100, "full")],
    ids=["empty", "partial", "full"],
)
def test_status_by_amount(order_factory, amount, expected_status):
    order = order_factory(amount=amount)
    # derive status (example)
    status = "empty" if amount == 0 else "full" if amount == 100 else "partial"
    assert status == expected_status
```

5) Placement guidance
- Global factories used across many modules → `tests/conftest.py`.
- Component-level reuse within a folder → local `conftest.py` in that folder.
- Single-module specificity → factory fixture in the test file.

6) Libraries
- For complex graphs/ORMs, consider `factory_boy` + `pytest-factoryboy`. For small projects, prefer simple hand-rolled factories.

## QUALITY CHECKLIST

Before submitting tests, verify:
- [ ] "Proposed Test Cases" section is placed correctly (new files: after imports; existing files: updated in-place or appended at end)
- [ ] No existing test code has been moved or reorganized
- [ ] New tests are added at appropriate locations (end of classes/file)
- [ ] All public methods have corresponding tests
- [ ] Error conditions and edge cases are covered
- [ ] Async operations use `@pytest.mark.asyncio`
- [ ] Mocks are appropriate and verified
- [ ] Tests are independent and can run in any order
- [ ] Test names clearly describe what is being tested
- [ ] Assertions are specific and informative
- [ ] All tests in `### Proposed Test Cases` are implemented or marked `[IMPLEMENTED]`
- [ ] Configuration variations are covered
- [ ] Performance implications are considered
- [ ] Fixture placement follows the decision tree
- [ ] Factory fixtures used for reusable data; no shared mutable state between tests
- [ ] Tests are atomic and test one logical concept

## ANTI-PATTERNS TO AVOID

1. **Always appending instead of updating**: Modify existing code in-place when improvements are identified
2. **Reorganizing existing code**: Never move, reorder, or restructure existing test methods or classes unnecessarily
3. **Breaking existing file structure**: Update existing sections in-place when possible, append only when necessary
4. **Executable "Proposed Test Cases"**: This section must be comments, not Python code
5. **Over-mocking**: Mock only external dependencies, not the code under test
6. **Brittle tests**: Test behavior, not implementation details
7. **Test interdependence**: Each test must run independently in any order
8. **Flaky Tests**: Do not commit tests that rely on timing (`time.sleep`) or have other non-deterministic behavior. Use mocks and fixtures to create predictable outcomes.
9. **Inadequate cleanup**: Always use fixtures for setup/teardown
10. **Vague assertions**: Use specific assertions with clear error messages
11. **Missing error cases**: Test error conditions as thoroughly as success cases
12. **Hardcoded values**: Use fixtures and constants for maintainable test data
13. **Removing working tests**: Never remove tests that provide unique coverage.
    (Duplicates without unique coverage may be removed under the Test Preservation Policy.)
14. **Mixing setup methods**: Use either fixtures OR class-based setup, not both.
    If existing tests use class-based setup, first extract that logic into fixtures before migrating, to preserve coverage consistently.
15. **Inappropriate fixture scope**: Use the fixture placement decision tree
16. **Append-only mentality**: Update existing tests in-place when they need improvement rather than always adding new ones