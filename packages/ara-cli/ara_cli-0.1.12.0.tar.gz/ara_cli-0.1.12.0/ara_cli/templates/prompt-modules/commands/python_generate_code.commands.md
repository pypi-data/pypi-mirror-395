### COMMANDS FOR IMPLEMENTING ONE OR A SET OF NEW OR CHANGED FEATURE FILES

Your job is now:
* Silently analyze the given feature files and the specified behavior.
* Develop implementation strategies that minimize code changes with respect to any given code and test files, prefer reusing existing methods over new implementations.
* The max function length should not exceed 25 lines. The max file length should not exceed 120 lines.
* Always prefer to use existing python packages over your own implementation.
* In case additional implementation instructions are given as:
  * Specified in files with extensions "*.technology.md" follow strictly the specified mandatory python packages and tech stack
  * Explicitly specified as example reference implementation: use this reference information as starting point for your own implementation
* Fully implement the specified behavior in an easy testable and modular/extensible way, fully implement unit tests for your production code (try to achieve at least 90% code coverage) and implement for all given feature files the corresponding step definitions. Follow PEP8 coding guidelines, use numpy style docstrings for inline function documentation, apply as coding and design principle the separation of concerns and single responsibility principle.
* Generated or reworked python methods must not exceed 25 lines of code. In case methods exceed this length they need to be split according to the single responsibility principle and separation of concerns.
* Generated or reworked python files must not exceed 120 lines of code. In case files exceed this length they need to be split according to the single responsibility principle and separation of concerns.
* Use the python logger logging package to implement logging for all application modules that enable a full observability of the program flow over the log file. Use ./logs/<module_name>.log as filepath for logging.

* Only return full copy pastable file content for production code, unit test files and step definition files. Use for every single generated code block this markdown code block format:

```python
# [ ] extract
# filename: src/{filename}.py
{python code}
```

* The extract and filename statements are only allowed once per markdown code block
* The first character of the first line inside your code block must be '#' and the first character of the second line inside your code block must be '#'
* replace the '# [ ] extract' statement of the template with '# [x] extract' in your response
* in case of files get deprecated give me a list of files that can be safely deleted