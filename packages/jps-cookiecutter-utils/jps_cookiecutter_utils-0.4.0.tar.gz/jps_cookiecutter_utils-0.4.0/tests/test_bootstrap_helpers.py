from scripts import bootstrap


def test_derive_code_repository_underscore():
    assert bootstrap.derive_code_repository_underscore("jps-sample-utils") == "jps_sample_utils"


def test_parse_infile(tmp_path):
    infile = tmp_path / "bootstrap.txt"
    infile.write_text("AUTHOR=Jaideep Sundaram\nAUTHOR-EMAIL=js@example.com\n")
    values = bootstrap.parse_infile(infile)
    assert values["AUTHOR"] == "Jaideep Sundaram"
    assert values["AUTHOR-EMAIL"] == "js@example.com"


def test_parse_infile_ignores_comments_and_empty_lines(tmp_path):
    infile = tmp_path / "bootstrap.txt"
    infile.write_text("# comment\n\nCODE-REPOSITORY=jps-cookiecutter-utils\n")
    values = bootstrap.parse_infile(infile)
    assert "CODE-REPOSITORY" in values


def test_build_placeholder_map():
    supplied = {"AUTHOR": "Jaideep"}
    mapping = bootstrap.build_placeholder_map("jps-cookiecutter-utils", supplied)
    assert mapping["{{__CODE-REPOSITORY__}}"] == "jps-cookiecutter-utils"
    assert mapping["{{__CODE_REPOSITORY__}}"] == "jps_cookiecutter_utils"
    assert mapping["{{__AUTHOR__}}"] == "Jaideep"


def test_files_with_any_placeholder(tmp_path):
    file_with_placeholder = tmp_path / "file1.txt"
    file_with_placeholder.write_text("{{__AUTHOR__}}")
    file_without_placeholder = tmp_path / "file2.txt"
    file_without_placeholder.write_text("No placeholders here.")
    token_map = {"{{__AUTHOR__}}": "Jaideep"}
    hits = bootstrap.files_with_any_placeholder(
        [file_with_placeholder, file_without_placeholder], token_map
    )
    assert file_with_placeholder in hits
    assert file_without_placeholder not in hits
