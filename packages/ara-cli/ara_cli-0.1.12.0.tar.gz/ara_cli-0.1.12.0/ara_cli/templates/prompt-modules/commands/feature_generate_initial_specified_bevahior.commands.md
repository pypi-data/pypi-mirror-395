# COMMANDS FOR INITIALLY SPECIFYING APPLICATION BEHAVIOR USING FEATURE FILES

* Given a description of the wanted application behavior as bullet point list, specification document, ...

* And given this feature template with placeholders in <...>

```
@creator_Egermeier
Feature: <descriptive title>

  As a <user>
  I want to <do something | need something>
  So that <I can achieve something>

  Contributes to <here comes your parent artefact> <here comes your classifier of the parent artefact>  

  Description: <further optional description to understand
  the rule, no format defined, the example artefact is only a placeholder>

  Scenario: <descriptive scenario title>
    Given <precondition>
    When <action>
    Then <expected result>

  Scenario Outline: <descriptive scenario title>
    Given <precondition>
    When <action>
    Then <expected result>

    Examples:
      | descriptive scenario title | precondition         | action             | expected result    |
      | <example title 1>          | <example precond. 1> | <example action 1> | <example result 1> |
      | <example title 2>          | <example precond. 2> | <example action 2> | <example result 2> |
```

# Instructions
* Now formulate a set (one, two or many, each feature file should not consist of more than max 3 scenarios
* Each feature file should follow the single responsibility principle as well as the feature file formulations should follow the separation of concerns) of feature files that fully cover the human user observable behavior described in the specification notes. 
* Consider in your formulation of the Gherkin feature files when specifying the behavior of graphical user interfaces: Describe the behavior of the graphical user interfaces so that I can clearly imagine both how they work and their visual look and feel.
* Follow strictly the given template format in order to structure your feature files. You are allowed to use scenario outlines where useful. But in case they are not helpful in order to increase the readability you can just use standard scenario formulations.

* Wrap and return the formulated feature files as full copy pastable file content in the following format as markdown code block:

```artefact
# [ ] extract 
# filename: ara/features/{filename}.feature 
{formulation, with the valid feature file structure as given by the feature gherkin template}
```

* The extract and filename statements are only allowed once per markdown code block
* The first character of the first line inside your code block must be '#' and the first character of the second line inside your code block must be '#'
* replace the '# [ ] extract' statement of the template with '# [x] extract' in your response
* in case of files get deprecated give me a list of files that can be safely deleted