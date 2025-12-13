### COMMANDS FOR CREATING AND CORRECTING STEP DEFINITIONS FOR FEATURE FILES

**MANDATORY INPUT VALIDATION:**
- Feature files (.feature) must be provided
- Behave test report must be provided

**PROMPT DEFINITION ERROR:** If mandatory input is missing, immediately stop and return: "ERROR: Missing mandatory input. Please provide both feature files (.feature) and behave test report before proceeding."

**OPTIONAL INPUT:**
- Already existing step definitions

**PROMPT DEFINITION WARNING:** If optional input is missing: "WARNING: No existing step definitions provided. If step definitions already exist in your project, please include them as input context to avoid duplication and ensure consistency."

### Your job is now:
* Silently analyze the given feature files and behave test report to understand current test failures and missing step implementations.
* Silently review any provided existing step definitions to avoid duplication and maintain consistency.
* Develop step definition implementation strategies that minimize code changes with respect to existing step definitions, prefer reusing existing step patterns over new implementations.
* The max function length should not exceed 25 lines. The max file length should not exceed 120 lines.
* Always prefer to use existing python packages over your own implementation.
* Use the behave testing framework for all step definition implementations.
* Apply mocking extensively to isolate step definitions from external inputs and interfaces using unittest.mock or pytest-mock.
* Fully implement all missing step definitions for the given feature files in an easy testable and modular/extensible way. Follow PEP8 coding guidelines, use numpy style docstrings for inline function documentation, apply as coding and design principle the separation of concerns and single responsibility principle.
* Generated or reworked python methods must not exceed 25 lines of code. In case methods exceed this length they need to be split according to the single responsibility principle and separation of concerns.
* Generated or reworked python files must not exceed 120 lines of code. In case files exceed this length they need to be split according to the single responsibility principle and separation of concerns.
* Implement proper assertion methods that provide clear error messages when steps fail.
* Use context.scenario, context.feature, and context.table appropriately for data sharing between steps.
* Implement proper cleanup in @after_scenario and @after_feature hooks when necessary.

* Only return full copy pastable file content for step definition files. Use for every single generated code block this markdown code block format:

```python
# [ ] extract
# filename: ara/features/steps/{filename}_steps.py
{python code}
```

* The extract and filename statements are only allowed once per markdown code block
* The first character of the first line inside your code block must be '#' and the first character of the second line inside your code block must be '#'
* replace the '# [ ] extract' statement of the template with '# [x] extract' in your response
* in case of files get deprecated give me a list of files that can be safely deleted