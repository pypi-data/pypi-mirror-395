# COMMANDS FOR ADDING OR MODIFYING EXISTING SPECIFIED BEHAVIOR

**At first**: 

Check if a set of feature files is given

* In case no feature files are given:
  * Stop immediately and respond with: "Error in prompt context: no feature files are given as already specified application behavior"

* Else:
  * Continue following the given instructions

# Instructions
Your job is now:
* Silently analyze the given feature files and the specified behavior.
* Silently analyze the additionally given information about new wanted behavior or changes of existing behavior
* Develop adaptation strategies that minimize feature file changes with respect to any given already existing feature files, prefer reusing and adapting existing formulations/scenarios and steps over completely new formulations
* Now formulate to fully cover the new or changed behavior (one, two or many changed or new feature files)

Follow these feature file quality rules:
* Each feature file should not consist of more than max 3 scenarios, each feature file should follow the single responsibility principle as well as the feature file formulations should follow the separation of concerns of feature files that fully cover the human user observable behavior described in the specification notes. Consider in your formulation of the Gherkin feature files that, when implementing the graphical user interfaces, the full functionality of the Python package Streamlit can be utilized.
* Follow strictly the given feature file format in order to structure your feature files. 
* You are allowed to use scenario outlines where useful. But in case they are not helpful in order to increase the readability you can just use standard scenario formulations.

* Wrap and return the formulated feature files as full copy pastable file content in the following format as markdown code block:

```artefact
# [ ] extract 
# filename: ara/features/{filename}.feature
{formulation, with the valid feature file structure following the given feature files as reference}
```

* The extract and filename statements are only allowed once per markdown code block
* The first character of the first line inside your code block must be '#' and the first character of the second line inside your code block must be '#'
* replace the '# [ ] extract' statement of the template with '# [x] extract' in your response
* in case of files get deprecated give me a list of files that can be safely deleted