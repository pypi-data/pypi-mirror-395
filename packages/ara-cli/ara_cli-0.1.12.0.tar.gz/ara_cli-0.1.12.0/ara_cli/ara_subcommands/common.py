from typing import Optional
from enum import Enum
import typer
from ara_cli.classifier import Classifier
from ara_cli.template_manager import SpecificationBreakdownAspects
from ara_cli.completers import DynamicCompleters


# Get classifiers and aspects
classifiers = Classifier.ordered_classifiers()
aspects = SpecificationBreakdownAspects.VALID_ASPECTS


# Create enums for better type safety
ClassifierEnum = Enum('ClassifierEnum', {c: c for c in classifiers})
AspectEnum = Enum('AspectEnum', {a: a for a in aspects})
TemplateTypeEnum = Enum('TemplateTypeEnum', {
    'rules': 'rules',
    'intention': 'intention',
    'commands': 'commands',
    'blueprint': 'blueprint'
})


# Create typed arguments and options with autocompletion
def ClassifierArgument(help_text: str, default=...):
    """Create a classifier argument with autocompletion."""
    return typer.Argument(
        default,
        help=help_text,
        autocompletion=DynamicCompleters.create_classifier_completer()
    )


def ClassifierOption(help_text: str, *names):
    """Create a classifier option with autocompletion."""
    return typer.Option(
        None,
        *names,
        help=help_text,
        autocompletion=DynamicCompleters.create_classifier_completer()
    )


def ArtefactNameArgument(help_text: str, default=...):
    """Create an artefact name argument with autocompletion."""
    return typer.Argument(
        default,
        help=help_text,
        autocompletion=DynamicCompleters.create_artefact_name_completer()
    )



def ParentNameArgument(help_text: str):
    """Create a parent name argument with autocompletion."""
    return typer.Argument(
        help=help_text,
        autocompletion=DynamicCompleters.create_parent_name_completer()
    )


def AspectArgument(help_text: str):
    """Create an aspect argument with autocompletion."""
    return typer.Argument(
        help=help_text,
        autocompletion=DynamicCompleters.create_aspect_completer()
    )


def StatusArgument(help_text: str):
    """Create a status argument with autocompletion."""
    return typer.Argument(
        help=help_text,
        autocompletion=DynamicCompleters.create_status_completer()
    )


def TemplateTypeArgument(help_text: str):
    """Create a template type argument with autocompletion."""
    return typer.Argument(
        help=help_text,
        autocompletion=DynamicCompleters.create_template_type_completer()
    )


def ChatNameArgument(help_text: str, default=None):
    """Create a chat name argument with autocompletion."""
    return typer.Argument(
        default,
        help=help_text,
        autocompletion=DynamicCompleters.create_chat_file_completer()
    )


# Mock args class to maintain compatibility with existing action functions
class MockArgs:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
