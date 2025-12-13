import pytest

from scripts import bootstrap


def test_copy_templates_and_replace_placeholders(tmp_path):
    # Prepare fake template dir
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "README.md"
    template_file.write_text("Author: {{__AUTHOR__}}")

    # Destination project dir
    project_root = tmp_path / "project"
    project_root.mkdir()

    copied = bootstrap.copy_templates(template_dir, project_root)
    assert len(copied) == 1
    assert copied[0].exists()

    # Replace placeholders
    token_map = {"{{__AUTHOR__}}": "Jaideep"}
    bootstrap.replace_placeholders_in_files(copied, token_map)
    content = copied[0].read_text()
    assert "Jaideep" in content


def test_create_project_structure(tmp_path):
    project_root = tmp_path / "newproj"
    bootstrap.create_project_structure(project_root)
    expected_dirs = ["src", "tests", "docs", ".github/workflow"]
    for d in expected_dirs:
        assert (project_root / d).exists()
