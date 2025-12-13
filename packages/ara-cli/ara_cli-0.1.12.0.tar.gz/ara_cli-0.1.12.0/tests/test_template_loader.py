import os
import pytest
from unittest.mock import MagicMock, patch, mock_open
from ara_cli.template_loader import TemplateLoader


@pytest.fixture
def mock_chat_instance():
    """Fixture for a mocked chat instance."""
    mock = MagicMock()
    mock.choose_file_to_load.return_value = "chosen_file.md"
    mock.load_file.return_value = True
    return mock


@pytest.fixture
def template_loader_cli():
    """Fixture for a TemplateLoader in CLI mode."""
    return TemplateLoader()


@pytest.fixture
def template_loader_chat(mock_chat_instance):
    """Fixture for a TemplateLoader in chat mode."""
    return TemplateLoader(chat_instance=mock_chat_instance)


def test_init(mock_chat_instance):
    """Test the constructor."""
    loader_cli = TemplateLoader()
    assert loader_cli.chat_instance is None

    loader_chat = TemplateLoader(chat_instance=mock_chat_instance)
    assert loader_chat.chat_instance == mock_chat_instance


@pytest.mark.parametrize("template_name, default_pattern, expected_method_to_call", [
    ("", "*.rules.md", "load_template_from_prompt_data"),
    ("my_rule", "*.rules.md", "load_template_from_global_or_local"),
])
def test_load_template_routing(template_loader_cli, template_name, default_pattern, expected_method_to_call):
    """Test that load_template calls the correct downstream method based on inputs."""
    with patch.object(TemplateLoader, 'load_template_from_prompt_data') as mock_from_prompt, \
         patch.object(TemplateLoader, 'load_template_from_global_or_local') as mock_from_global_local:

        template_loader_cli.load_template(
            template_name, "rules", "chat.md", default_pattern)

        if expected_method_to_call == "load_template_from_prompt_data":
            mock_from_prompt.assert_called_once()
            mock_from_global_local.assert_not_called()
        else:
            mock_from_prompt.assert_not_called()
            mock_from_global_local.assert_called_once()


def test_load_template_no_name_no_pattern(template_loader_cli, capsys):
    """Test load_template fails gracefully when no name or pattern is given."""
    result = template_loader_cli.load_template("", "blueprint", "chat.md", None)
    assert result is False
    captured = capsys.readouterr()
    assert "A template name is required for template type 'blueprint'" in captured.out


@pytest.mark.parametrize("template_type, expected_plural", [
    ("rules", "rules"),
    ("commands", "commands"),
    ("intention", "intentions"),
    ("blueprint", "blueprints"),
    ("custom", "customs"),
])
def test_get_plural_template_type(template_loader_cli, template_type, expected_plural):
    """Test the pluralization of template types."""
    assert template_loader_cli.get_plural_template_type(
        template_type) == expected_plural


@pytest.mark.parametrize("template_name, expected_method_to_call", [
    ("global/my_rule", "_load_global_template"),
    ("my_rule", "_load_local_template"),
])
def test_load_template_from_global_or_local_routing(template_loader_cli, template_name, expected_method_to_call):
    """Test routing between global and local template loading."""
    with patch.object(TemplateLoader, '_load_global_template') as mock_global, \
         patch.object(TemplateLoader, '_load_local_template') as mock_local:

        template_loader_cli.load_template_from_global_or_local(
            template_name, "rules", "chat.md")

        if expected_method_to_call == "_load_global_template":
            mock_global.assert_called_once()
            mock_local.assert_not_called()
        else:
            mock_global.assert_not_called()
            mock_local.assert_called_once()


@pytest.mark.parametrize("files, pattern, user_input, expected_return", [
    (["one.md"], "*.md", "", "one.md"),
    ([], "*.md", "", None),
    (["a.md", "b.md"], "*", "1", "a.md"),
    (["a.md", "b.md"], "*", "2", "b.md"),
    (["a.md", "b.md"], "*", "3", None),
    (["a.md", "b.md"], "*", "invalid", None),
])
def test_choose_file_for_cli(template_loader_cli, files, pattern, user_input, expected_return):
    """Test the interactive file selection for the CLI."""
    with patch('builtins.input', return_value=user_input):
        result = template_loader_cli._choose_file_for_cli(files, pattern)
        assert result == expected_return


def test_load_file_to_chat_cli_context(tmp_path):
    """Test writing template content to a chat file in a CLI context."""
    chat_file = tmp_path / "chat.md"
    chat_file.write_text("# ara prompt:\n")
    template_file = tmp_path / "template.md"
    template_content = "This is the template content."
    template_file.write_text(template_content)

    loader = TemplateLoader()
    result = loader._load_file_to_chat(
        str(template_file), "rules", str(chat_file))

    assert result is True
    final_content = chat_file.read_text()
    expected_content = f"# ara prompt:\n\n{template_content}\n"
    assert final_content == expected_content


def test_load_file_to_chat_chat_context(template_loader_chat, mock_chat_instance):
    """Test delegating file loading to the chat instance."""
    result = template_loader_chat._load_file_to_chat(
        "file.md", "rules", "chat.md")

    assert result is True
    mock_chat_instance.add_prompt_tag_if_needed.assert_called_once_with(
        "chat.md")
    mock_chat_instance.load_file.assert_called_once_with("file.md")


def test_find_project_root(tmp_path):
    """Test finding the project root directory."""
    project_root = tmp_path / "project"
    ara_dir = project_root / "ara"
    nested_dir = project_root / "src" / "component"
    ara_dir.mkdir(parents=True)
    nested_dir.mkdir(parents=True)

    no_ara_dir = tmp_path / "other"
    no_ara_dir.mkdir()

    loader = TemplateLoader()

    # Test finding the root from a nested directory
    assert loader._find_project_root(str(nested_dir)) == str(project_root)
    # Test finding the root from the root itself
    assert loader._find_project_root(str(project_root)) == str(project_root)
    # Test not finding the root
    assert loader._find_project_root(str(no_ara_dir)) is None


@patch('ara_cli.template_loader.TemplatePathManager')
@patch('ara_cli.template_loader.ConfigManager')
def test_get_available_templates(MockConfigManager, MockTemplatePathManager, tmp_path):
    """Test the discovery of global and local templates."""
    # Setup mock paths and config
    project_root = tmp_path / "project"
    ara_dir = project_root / "ara"
    araconfig_dir = project_root / ".araconfig"
    custom_modules_dir = araconfig_dir / "custom-prompt-modules" / "rules"
    global_modules_dir = tmp_path / "global_templates" / "prompt-modules" / "rules"

    for d in [ara_dir, custom_modules_dir, global_modules_dir]:
        d.mkdir(parents=True)

    (custom_modules_dir / "local_rule.md").touch()
    (global_modules_dir / "global_rule.md").touch()

    mock_config = MagicMock()
    mock_config.local_prompt_templates_dir = ".araconfig"
    mock_config.custom_prompt_templates_subdir = "custom-prompt-modules"
    MockConfigManager.get_config.return_value = mock_config
    MockTemplatePathManager.get_template_base_path.return_value = str(
        tmp_path / "global_templates")

    loader = TemplateLoader()
    templates = loader.get_available_templates(
        "rules", context_path=str(project_root))

    assert sorted(templates) == sorted(
        ["global/global_rule.md", "local_rule.md"])
