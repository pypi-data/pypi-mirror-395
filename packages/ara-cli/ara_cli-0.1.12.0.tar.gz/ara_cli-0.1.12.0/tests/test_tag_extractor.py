import pytest
from unittest.mock import MagicMock, patch
from ara_cli.tag_extractor import TagExtractor
from ara_cli.list_filter import ListFilter


@pytest.fixture
def artefact():
    """Fixture to create a mock artefact object."""
    class Artefact:
        def __init__(self, tags, status, users, author="creator_unknown", path="dummy.md", content=""):
            self.tags = tags
            self.status = status
            self.users = users
            self.author = author
            self.path = path
            self.content = content
    return Artefact


@pytest.mark.parametrize("navigate_to_target, filtered_extra_column, list_filter, artefact_data, expected_tags", [
    (
        False, False, None,
        {'artefacts': [
            (['tag1', 'tag2'], 'in-progress', ['user1'], "creator_unknown"),
            (['tag3'], 'done', ['user2'], "creator_unknown")
        ]},
        ['creator_unknown', 'done', 'in-progress', 'tag1', 'tag2', 'tag3', 'user_user1', 'user_user2']
    ),
    (
        False, True, None,
        {'artefacts': [
            (['project_a', 'priority_high'], None, ['user1'], "creator_unknown"),
            (['feature_x'], 'done', ['user2'], "creator_unknown")
        ]},
        ['project_a']
    ),
    (
        False, False, ListFilter(include_tags=['kritik']),
        {'artefacts': [
            (['release', 'kritik'], 'review', ['dev1'], "creator_unknown"),
            (['bugfix'], 'to-do', ['dev2'], "creator_unknown")
        ]},
        ['creator_unknown', 'kritik', 'release', 'review', 'user_dev1']
    ),
    (
        True, False, None,
        {'artefacts': [
            (['tag3'], 'status2', ['user3'], "creator_unknown")
        ]},
        ['creator_unknown', 'status2', 'tag3', 'user_user3']
    ),
    (
        False, False, None,
        {'artefacts': []},
        []
    ),
])
@patch('ara_cli.artefact_reader.ArtefactReader')
@patch('ara_cli.template_manager.DirectoryNavigator')
def test_extract_tags(mock_directory_navigator, mock_artefact_reader, artefact, navigate_to_target, filtered_extra_column, list_filter, artefact_data, expected_tags):
    mock_artefacts = {key: [artefact(
        *data) for data in artefact_list] for key, artefact_list in artefact_data.items()}
    mock_artefact_reader.read_artefacts.return_value = mock_artefacts

    mock_navigator_instance = mock_directory_navigator.return_value
    mock_navigator_instance.navigate_to_target = MagicMock()

    tag_extractor = TagExtractor()

    result = tag_extractor.extract_tags(
        navigate_to_target=navigate_to_target,
        filtered_extra_column=filtered_extra_column,
        list_filter=list_filter
    )

    if navigate_to_target:
        mock_navigator_instance.navigate_to_target.assert_called_once()
    else:
        mock_navigator_instance.navigate_to_target.assert_not_called()

    mock_artefact_reader.read_artefacts.assert_called_once()

    # Convert dictionary result to flat list for comparison
    actual_tags = []
    for group in result.values():
        actual_tags.extend(group)
    
    assert sorted(actual_tags) == sorted(expected_tags)