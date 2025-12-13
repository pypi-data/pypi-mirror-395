### COMMANDS FOR FIXING BUGS

Your job is now to fix the described error:

* Silently analyze the given error description or error log files
* Silently review the provided source files and if given the provided feature file (specified behavior) to understand the current faulty implementation and draft silently a potential solution to fix the error
* Develop implementation strategies that minimize code changes, prefer reusing existing methods over new implementations. Also always prefer to use existing python packages over your own implementation.

When you touch code or need to generate code for bug fixing:
* The max function or method length should not exceed 40 lines.
* The max class length should not exceed 150 lines.
* The max file length should not exceed 150 lines.
* Split implementation files or functions/methods/classes in case they exceed their defined length maximum.
* Apply as coding and design principle the separation of concerns and single responsibility principle in general and specifically when you need to split.

* Important: you are NOT allowed to do any further refactorings not related to the bug fixing implementation. Refactoring for enhancing the code quality is not allowed.
* The fixed code must fully implement the specified behavior in an easy testable and modular/extensible way.
* Follow PEP8 coding guidelines.
* Use descriptive numpy style docstrings for inline method and class documentation.
* Use the python logger logging package to implement logging for all application modules that enables a fine granular full observability of the program flow by the log file. Use ./logs/<module_name>.log as filepath for logging.

* Only return full copy pastable file content.
* Use for every single generated code block this markdown code block format:

```python
# [ ] extract
# filename: src/{filename}.py
{python code}
```

* The extract and filename statements are only allowed once per code block
* The first character of the first line inside your code block must be '#' and the first character of the second line inside your code block must be '#'
* replace the '# [ ] extract' statement of the template with '# [x] extract' in your response
* in case of files get deprecated give me a list of files that can be safely deleted