### COMMANDS FOR CREATING AND CORRECTING UNIT TESTS

**MANDATORY INPUT VALIDATION:**
- Feature files (.feature) must be provided
- Code coverage report or pytest test report must be provided

**PROMPT DEFINITION ERROR:** If mandatory input is missing, immediately stop and return: "ERROR: Missing mandatory input. Please provide both feature files (.feature) and code coverage/pytest test report before proceeding."

**OPTIONAL INPUT:**
- Already existing unit tests

**PROMPT DEFINITION WARNING:** If optional input is missing: "WARNING: No existing unit tests provided. If unit tests already exist in your project, please include them as input context to avoid duplication and ensure consistency."

#### Your job is now:
* Silently analyze the given feature files and code coverage/pytest test report to understand current test gaps and implementation requirements.
* Silently review any provided existing unit tests to avoid duplication and maintain consistency with existing test patterns.
* Develop unit test implementation strategies that minimize code changes with respect to existing tests, prefer reusing existing test patterns and fixtures over new implementations.
* The max function length should not exceed 25 lines. The max file length should not exceed 120 lines.
* Always prefer to use existing python packages over your own implementation.
* Use the pytest testing framework for all unit test implementations.
* Apply mocking extensively to isolate unit tests from external inputs and interfaces using unittest.mock or pytest-mock. Mock all external dependencies, file I/O, network calls, and database interactions.
* Fully implement comprehensive unit tests that achieve at least 90% code coverage for the specified behavior in an easy maintainable and modular/extensible way. Follow PEP8 coding guidelines, use numpy style docstrings for inline function documentation, apply as coding and design principle the separation of concerns and single responsibility principle.
* Generated or reworked python methods must not exceed 25 lines of code. In case methods exceed this length they need to be split according to the single responsibility principle and separation of concerns.
* Generated or reworked python files must not exceed 120 lines of code. In case files exceed this length they need to be split according to the single responsibility principle and separation of concerns.

* Implement comprehensive test cases covering:
  - Happy path scenarios
  - Edge cases and boundary conditions
  - Error handling and exception scenarios
  - Input validation scenarios

* Use pytest fixtures for test data setup and teardown to ensure test isolation.
* Implement parametrized tests using @pytest.mark.parametrize for testing multiple input combinations efficiently.
* Use descriptive test method names that clearly indicate what is being tested.
* Include proper assertions with meaningful error messages.

* Only return full copy pastable file content for unit test files. Use for every single generated code block this markdown code block format:

```python
# [ ] extract
# filename: test/test_{filename}.py
{python code}
```

* The extract and filename statements are only allowed once per markdown code block
* The first character of the first line inside your code block must be '#' and the first character of the second line inside your code block must be '#'
* replace the '# [ ] extract' statement of the template with '# [x] extract' in your response
* in case of files get deprecated give me a list of files that can be safely deleted