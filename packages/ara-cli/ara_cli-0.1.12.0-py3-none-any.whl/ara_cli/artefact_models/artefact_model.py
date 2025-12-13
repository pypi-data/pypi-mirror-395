from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Literal, Union, Dict, ClassVar
from typing_extensions import Self
from enum import Enum
from abc import ABC, abstractmethod
from ara_cli.classifier import Classifier
import warnings
import string
import os


ALLOWED_STATUS_VALUES = ("to-do", "in-progress", "review", "done", "closed")


def replace_space_with_underscore(input: string):
    return input.replace(' ', '_')


def replace_underscore_with_space(input: string):
    return input.replace('_', ' ')


class ArtefactType(str, Enum):
    vision = "vision"
    businessgoal = "businessgoal"
    capability = "capability"
    epic = "epic"
    userstory = "userstory"
    example = "example"
    keyfeature = "keyfeature"
    feature = "feature"
    task = "task"
    issue = "issue"


class Contribution(BaseModel):
    artefact_name: Optional[str] = Field(
        default=None,
        description="Parent artefact identifier and name, can't contain spaces"
    )
    classifier: Optional[Union[str, ArtefactType]] = Field(
        default=None,
        description=f"Classifier of the parent artefact. Allowed options are {', '.join(ArtefactType)}"
    )
    rule: Optional[str] = Field(
        default=None,
        description="Rule the contribution is using. The classifier of the parent must be userstory or epic if this is used"
    )

    PLACEHOLDER_NAME: ClassVar[str] = "<filename or title of the artefact>"
    PLACEHOLDER_CLASSIFIER: ClassVar[str] = "<agile requirement artefact category> <(optional in case the contribution is to an artefact that is detailed with rules)"
    PLACEHOLDER_RULE: ClassVar[str] = "<rule as it is formulated>"

    @model_validator(mode="after")
    def validate_parent(self) -> Self:
        artefact_name = self.artefact_name
        classifier = self.classifier
        rule = self.rule

        if (
            artefact_name == Contribution.PLACEHOLDER_NAME
            or classifier == Contribution.PLACEHOLDER_CLASSIFIER
            or rule == Contribution.PLACEHOLDER_RULE
        ):
            return self

        if artefact_name:
            artefact_name = replace_space_with_underscore(artefact_name)
        if not artefact_name or not classifier:
            self.artefact_name = None
            self.classifier = None
            self.rule = None
            return self
        if rule and classifier not in [ArtefactType.epic, ArtefactType.userstory]:
            raise ValueError("rule can be used only if parent is a userstory or an epic")

        return self

    @field_validator('artefact_name')
    def validate_artefact_name(cls, value):
        if not value or value == Contribution.PLACEHOLDER_NAME:
            return value
        if ' ' in value:
            warnings.warn(message="artefact_name can not contain spaces. Replacing spaces with '_'")
            value = replace_space_with_underscore(value)
        return value

    @field_validator('classifier', mode='after')
    def validate_classifier(cls, v):
        if not v or v == Contribution.PLACEHOLDER_CLASSIFIER:
            return v
        try:
            return ArtefactType(v)
        except ValueError:
            raise ValueError(f"Invalid classifier '{v}'. Allowed classifiers are {', '.join(ArtefactType)}")

    @classmethod
    def deserialize_from_line(cls, line: str, contribution_line_start: str) -> 'Contribution':
        if ":" in line:
            line = line.replace(':', '')
        if not line.startswith(contribution_line_start):
            raise ValueError(f"Contribution line '{line}' does not start with '{contribution_line_start}'")

        parent_text = line[len(contribution_line_start):].strip()
        rule_specifier = " using rule "

        placeholder_line = f"{cls.PLACEHOLDER_NAME} {cls.PLACEHOLDER_CLASSIFIER}{rule_specifier}{cls.PLACEHOLDER_RULE}"
        if parent_text == placeholder_line:
            return cls(
                artefact_name=cls.PLACEHOLDER_NAME,
                classifier=cls.PLACEHOLDER_CLASSIFIER,
                rule=cls.PLACEHOLDER_RULE
            )

        artefact_name = None
        classifier = None
        rule = None

        if rule_specifier in parent_text:
            parent_text, rule_text = parent_text.split(rule_specifier, 1)
            rule = rule_text
        parent_text_list = parent_text.split(' ')
        classifier = parent_text_list[-1].lower()
        artefact_name = '_'.join([s for s in parent_text_list if s][:-1])

        return cls(
            artefact_name=artefact_name,
            classifier=classifier,
            rule=rule
        )

    def serialize(self) -> str:
        if not self.classifier or not self.artefact_name:
            return ""
        artefact_type = Classifier.get_artefact_title(self.classifier) or self.classifier
        artefact_name = replace_underscore_with_space(self.artefact_name)
        contribution = f"{artefact_name} {artefact_type}"
        if self.rule:
            contribution = f"{contribution} using rule {self.rule}"
        return contribution


class Intent(BaseModel, ABC):
    model_config = {
        "validate_assignment": True
    }

    @classmethod
    @abstractmethod
    def deserialize_from_lines(cls, lines: List[str], start_index: int = 0) -> 'Intent':    # pragma: no cover
        pass

    @classmethod
    def deserialize(cls, text: str, start_index: int = 0) -> 'Intent':
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

        return cls.deserialize_from_lines(lines, start_index)

    @abstractmethod
    def serialize(self) -> str:    # pragma: no cover
        pass


class Artefact(BaseModel, ABC):

    model_config = {
        "validate_assignment": True
    }

    _file_path: Optional[str] = None
    artefact_type: ArtefactType = Field(
        ...,
        description=f"Artefact classifier (mandatory). Allowed classifiers are {', '.join(ArtefactType)}"
    )
    status: Optional[Literal[ALLOWED_STATUS_VALUES]] = Field(
        default=None,
        description="Work status of the artefact. May be one of 'to-do', 'in-progress', 'review', 'done', 'closed'."
    )
    users: List[str] = Field(
        default=[],
        description="Optional list of users assigned to the artefact"
    )
    tags: List[str] = Field(
        default=[],
        description="Optional list of tags (0-many)",
    )
    author: Optional[str] = Field(
        default="creator_unknown",
        description="Author of the artefact, must be a single entry of the form 'creator_<someone>'."
    )
    title: str = Field(
        ...,
        description="Descriptive Artefact title (mandatory)",

    )
    contribution: Optional[Contribution] = Field(
        default=None,
        description="Artefact details to which this artefact contributes. It is strongly recommended to always have a contribution set."
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional further description to understand the artefact. The description should summerize the core intention of the artefact and give additional valuable information about the artefact."
    )

    @property
    def file_path(self) -> str:
        if self._file_path is not None:
            return self._file_path
        sub_dir = Classifier.get_sub_directory(self.artefact_type)
        return f"{sub_dir}/{self.title}.{self.artefact_type}"

    @model_validator(mode="after")
    def ensure_file_path_consistency(self):
        if not self._file_path:
            return self
        file_path = self._file_path
        dir_path = os.path.dirname(file_path)
        artefact_type = self._artefact_type()
        file_path = f"{dir_path}/{self.title}.{artefact_type.value}"
        self._file_path = file_path
        return self

    @model_validator(mode="after")
    def validate_contribution(self):
        contribution = self.contribution
        classifier = self.artefact_type.value
        name = self.title
        if not contribution:
            warnings.warn(f"Contribution of {classifier} '{name}' is not set and will be empty")
        return self

    @field_validator('artefact_type')
    def validate_artefact_type(cls, v):
        if not isinstance(v, ArtefactType):
            raise TypeError(f"Invalid type of artefact variable {v}: {type(v)}. Must be ArtefactType and one of {', '.join(ArtefactType)}")
        if v != cls._artefact_type():
            raise ValueError(f"Invalid artefact type: {v}\nMust be {cls._artefact_type()}")
        return v

    @field_validator('status', mode='before')
    def validate_status(cls, v):
        if not v:
            return v
        allowed_statuses = ["to-do", "in-progress", "review", "done", "closed"]
        if v not in allowed_statuses:
            raise ValueError(f"Invalid status: {v}. Allowed statuses are {', '.join(allowed_statuses)}")
        return v

    @field_validator('tags')
    def validate_tags(cls, v):
        status_list = ["to-do", "in-progress", "review", "done", "closed"]
        for tag in v:
            if ' ' in tag:
                raise ValueError(f"Tag '{tag}' should not contain empty spaces")
            if tag in status_list:
                raise ValueError(f"Tag '{tag}' has the form of a status tag. Set `status` field instead of passing it with other tags")
            if tag.startswith("user_"):
                raise ValueError(f"Tag '{tag} has the form of a user tag. Set `users` field instead of passing it with other tags")
            if tag.startswith("creator_"):
                raise ValueError(f"Tag '{tag}' has the form of an author tag. Set `author` field instead of passing it with other tags")
        return v

    @field_validator('author')
    def validate_author(cls, v):
        if v:
            if not v.startswith("creator_"):
                raise ValueError(f"Author '{v}' must start with 'creator_'.")
            if len(v) <= len("creator_"):
                raise ValueError("Creator name cannot be empty in author tag.")
        return v

    @field_validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError("artefact_title must not be empty")
        v = replace_space_with_underscore(v).strip()

        whitelisted_placeholder = "<descriptive_title>"
        if v == whitelisted_placeholder:
            return v

        letters = list(string.ascii_letters)
        digits = list(string.digits)
        allowed_special_characters = ['-', '_', 'Ä', 'Ö', 'Ü', 'ä', 'ö', 'ü', 'ß']
        allowed_characters = letters + digits + allowed_special_characters
        allowed_characters_set = set(allowed_characters)
        not_in_allowed = [char for char in v if char not in allowed_characters_set]
        if len(not_in_allowed) != 0:
            raise ValueError(f"`title` field must not contain {', '.join(not_in_allowed)}. Allowed characters are {allowed_characters}")

        return v

    @classmethod
    @abstractmethod
    def _title_prefix(cls) -> str:    # pragma: no cover
        pass

    @classmethod
    @abstractmethod
    def _artefact_type(cls) -> ArtefactType:    # pragma: no cover
        pass

    @classmethod
    def _deserialize_tags(cls, lines) -> (Dict[str, str], List[str]):
        assert len(lines) > 0, "Empty lines given, can't extract tags"
        tag_line = lines[0]
        if not tag_line.startswith('@'):
            return {}, lines

        tags = tag_line.split()
        tag_dict = cls._process_tags(tags)
        return tag_dict, lines[1:]

    @classmethod
    def _process_tags(cls, tags) -> Dict[str, str]:
        """Process a list of tags and return a dictionary with categorized tags."""
        status = None
        regular_tags = []
        users = []
        author = None
        
        for tag in tags:
            cls._validate_tag_format(tag)
            
            if cls._is_status_tag(tag):
                status = cls._process_status_tag(tag, status)
            elif cls._is_user_tag(tag):
                users.append(cls._extract_user_from_tag(tag))
            elif cls._is_author_tag(tag):
                author = cls._process_author_tag(tag, author)
            else:
                regular_tags.append(tag[1:])
        
        return {
            "status": status,
            "users": users,
            "tags": regular_tags,
            "author": author
        }

    @classmethod
    def _validate_tag_format(cls, tag):
        """Validate that tag starts with @."""
        if not tag.startswith('@'):
            raise ValueError(f"Tag '{tag}' should start with '@' but started with '{tag[0]}'")

    @classmethod
    def _is_status_tag(cls, tag) -> bool:
        """Check if tag is a status tag."""
        status_list = ["@to-do", "@in-progress", "@review", "@done", "@closed"]
        return tag in status_list

    @classmethod
    def _process_status_tag(cls, tag, current_status):
        """Process status tag and check for duplicates."""
        if current_status is not None:
            raise ValueError(f"Multiple status tags found: '@{current_status}' and '{tag}'")
        return tag[1:]  # Remove @ prefix

    @classmethod
    def _is_user_tag(cls, tag) -> bool:
        """Check if tag is a user tag."""
        user_prefix = "@user_"
        return tag.startswith(user_prefix) and len(tag) > len(user_prefix)

    @classmethod
    def _extract_user_from_tag(cls, tag) -> str:
        """Extract username from user tag."""
        user_prefix = "@user_"
        return tag[len(user_prefix):]

    @classmethod
    def _is_author_tag(cls, tag) -> bool:
        """Check if tag is an author tag."""
        creator_prefix = "@creator_"
        return tag.startswith(creator_prefix) and len(tag) > len(creator_prefix)

    @classmethod
    def _process_author_tag(cls, tag, current_author):
        """Process author tag and check for duplicates."""
        if current_author is not None:
            raise ValueError(f"Multiple author tags found: '@{current_author}' and '@{tag[1:]}'")
        return tag[1:] 

    @classmethod
    def _deserialize_title(cls, lines) -> (str, List[str]):
        assert len(lines) > 0, "Empty lines given, can't extract title"
        title_prefix = cls._title_prefix()
        title_line = lines[0]
        del lines[0]
        if not title_line.startswith(title_prefix):
            raise ValueError(
                f"No title found in {cls._artefact_type()}. Expected '{title_prefix}' as start of the title in line '{title_line}'")
        title = title_line[len(title_prefix):].strip()
        title = replace_space_with_underscore(title)
        return title, lines

    @classmethod
    def _deserialize_contribution(cls, lines) -> (Optional[Contribution], List[str]):
        contribution_start = cls._contribution_starts_with()
        contribution_line = ""
        for i in range(len(lines)):
            if lines[i].startswith(contribution_start):
                contribution_line = lines[i]
                del lines[i]
                break
        if not contribution_line:
            return None, lines
        contribution = Contribution.deserialize_from_line(contribution_line, contribution_start)
        return contribution, lines

    @classmethod
    def _deserialize_description(cls, lines: List[str]) -> (Optional[str], List[str]):
        description_start = cls._description_starts_with()
        start_index = -1
        for i, line in enumerate(lines):
            if line.startswith(description_start):
                start_index = i
                break

        if start_index == -1:
            return None, lines

        first_line_content = lines[start_index][len(description_start):].strip()

        description_lines = ([first_line_content] if first_line_content else []) + lines[start_index + 1:]

        description = "\n".join(description_lines)

        remaining_lines = lines[:start_index]

        return (description if description else None), remaining_lines

    @classmethod
    def _parse_common_fields(cls, text: str) -> dict:
        """
        Parse fields common to all artefacts from the text.
        Returns a dictionary of field names and values.
        """
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        tags, remaining_lines = cls._deserialize_tags(lines)
        title, remaining_lines = cls._deserialize_title(remaining_lines)
        contribution, remaining_lines = cls._deserialize_contribution(remaining_lines)
        description, remaining_lines = cls._deserialize_description(remaining_lines)

        fields = {
            'artefact_type': cls._artefact_type(),
            'tags': tags.get('tags', []),
            'users': tags.get('users', []),
            'status': tags.get('status'),
            'title': title,
            'contribution': contribution,
            'description': description,
        }
        if tags.get("author"):
            fields["author"] = tags.get("author")
        return fields

    @classmethod
    def deserialize(cls, text: str) -> 'Artefact':
        """
        Deserialize text into an Artefact instance using common fields.
        """
        fields = cls._parse_common_fields(text)
        return cls(**fields)

    @classmethod
    def _contribution_starts_with(cls) -> str:
        return "Contributes to"

    @classmethod
    def _description_starts_with(cls) -> str:
        return "Description:"

    @abstractmethod
    def serialize(self) -> str:    # pragma: no cover
        pass

    def _serialize_title(self) -> str:
        title = replace_underscore_with_space(self.title)
        return f"{self._title_prefix()} {title}"

    def _serialize_tags(self) -> (Optional[str]):
        tags = []
        if self.status:
            tags.append(f"@{self.status}")
        for user in self.users:
            tags.append(f"@user_{user}")
        if self.author:
            tags.append(f"@{self.author}")
        for tag in self.tags:
            tags.append(f"@{tag}")
        return ' '.join(tags)

    def _serialize_contribution(self) -> str:
        cls = self.__class__
        line = cls._contribution_starts_with()
        if self.contribution:
            line = f"{line} {self.contribution.serialize()}"
        return line

    def _serialize_description(self) -> Optional[str]:
        description = "Description: "
        if self.description is None:
            return description
        return f"{description}{self.description}"

    def set_contribution(self, artefact_name, classifier, rule=None):
        contribution = Contribution(
            artefact_name=artefact_name,
            classifier=classifier,
            rule=rule
        )
        self.contribution = contribution