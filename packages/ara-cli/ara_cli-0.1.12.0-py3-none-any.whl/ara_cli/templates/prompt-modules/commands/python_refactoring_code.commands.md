### COMMANDS FOR REFACTORING

Your job is now to refactor the code for enhancing the code quality and the design of the code according to the following guidelines:
* Refactoring = Changing the internal structure of code
* Without changing its external behavior
* Goal = Improve readability, maintainability, and design
-> "Refactoring is a change made to the internal structure of software to make it easier to understand and cheaper to modify without changing its observable behavior."
-> "Refactoring changes how code is written, not what it does."

Now do:
* Silently analyze the given code base
* Silently analyze the given feature file (specified behavior) to fully understand the flow and logic of the current implementation. Remember: you are not allowed to change specified behavior.

When you refactor the code remember:
* The max function or method length should not exceed 40 lines.
* The max class length should not exceed 150 lines.
* The max file length should not exceed 150 lines.
* Split implementation files or functions/methods/classes in case they exceed their defined length maximum.
* Apply as coding and design principle the separation of concerns and single responsibility principle in general and specifically when you need to split.
* Flatten nested code structures (e.g. if/while/for statements) to only one nesting level.
* The refactored code must fully implement the specified behavior in an easy testable and modular/extensible way.
* Follow PEP8 coding guidelines.
* Use descriptive numpy style docstrings for inline method and class documentation.
* Use the python logger logging package to implement logging for all application modules that enables a fine granular full observability of the program flow by the log file. Use ./logs/<module_name>.log as filepath for logging.

Your output specification is:
* Only return full copy pastable file content.
* Use for every single generated code block this markdown code block format:

```python
# [ ] extract
# filename: src/{filename}.py
{python code}
```

* The extract and filename statements are only allowed once per markdown code block
* The first character of the first line inside your code block must be '#' and the first character of the second line inside your code block must be '#'
* replace the '# [ ] extract' statement of the template with '# [x] extract' in your response
* in case of files get deprecated give me a list of files that can be safely deleted