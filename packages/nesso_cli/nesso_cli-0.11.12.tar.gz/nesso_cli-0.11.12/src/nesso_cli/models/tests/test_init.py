import json
import shutil
from pathlib import Path

from nesso_cli.models.config import config, yaml
from nesso_cli.models.init import (
    TEMPLATE_FILES_TO_RENDER,
    TEMPLATES_DIR,
    _generate_user_profile,
    create_directory_structure,
    create_profiles_yml_template,
    render_jinja_template_file,
    render_project_files,
    render_string,
)
from nesso_cli.models.main import app
from nesso_cli.models.models import DBTSQLServerConfig, NessoDBTConfig
from typer.testing import CliRunner

TEST_PROJECT_NAME = "test_project"
TEST_PROJECT_PATH = Path(__file__).parent.joinpath("dbt_projects", TEST_PROJECT_NAME)
TEST_PROJECT_PATH.mkdir(parents=True, exist_ok=True)
TEST_EXAMPLE_PROFILES_PATH = TEST_PROJECT_PATH / "profiles.yml.example"
TEST_PROJECT_FILE = TEST_PROJECT_PATH / "test_file.sql"
TEST_TEMPLATE_FILE = TEMPLATES_DIR / "test_file.sql"
TEST_TEMPLATE_FILE_TEMPLATED_FILENAME = TEMPLATES_DIR / "{{test_filename}}.sql"

TEST_BRONZE_SCHEMA = "test_bronze_schema"
TEST_SILVER_SCHEMA = "test_silver_schema"
TEST_GOLD_LAYER = "test_marts"

runner = CliRunner()


def test_create_directory_structure():
    # Assumptions.
    assert not TEST_PROJECT_PATH.joinpath("models").exists()

    # Test.
    create_directory_structure(
        project_dir=TEST_PROJECT_PATH,
        bronze_schema=TEST_BRONZE_SCHEMA,
        silver_schema=TEST_SILVER_SCHEMA,
        gold_layer_name=TEST_GOLD_LAYER,
    )

    assert TEST_PROJECT_PATH.joinpath("models").exists()
    assert TEST_PROJECT_PATH.joinpath("models", "sources", TEST_BRONZE_SCHEMA).exists()
    assert TEST_PROJECT_PATH.joinpath("models", TEST_SILVER_SCHEMA).exists()
    assert TEST_PROJECT_PATH.joinpath("models", TEST_GOLD_LAYER).exists()
    assert TEST_PROJECT_PATH.joinpath(".nesso").exists()

    # Cleanup.
    shutil.rmtree(TEST_PROJECT_PATH.joinpath("models"), ignore_errors=True)


def test_render_string():
    test_template_string = "hello, {{thing}}!"
    thing = "world"
    result = render_string(template_string=test_template_string, thing=thing)
    assert result == "hello, world!"


def test_render_jinja_template_file_stream_output():
    """Test that render_jinja_template_file() returns correct string output
    when stream_output is set to True."""
    # Assumptions.
    assert TEST_TEMPLATE_FILE.exists() is False

    # Create a test template file.
    with open(TEST_TEMPLATE_FILE, "w") as f:
        f.write("select * from {{test_variable}}")

    # Test.
    result = render_jinja_template_file(
        template_path=TEST_TEMPLATE_FILE.name,
        stream_output=True,
        test_variable="test123",
    )
    assert result == "select * from test123"

    # Cleanup.
    TEST_TEMPLATE_FILE.unlink()


def test_render_jinja_template_file():
    assert TEST_TEMPLATE_FILE.exists() is False

    # Create a test template file.
    with open(TEST_TEMPLATE_FILE, "w") as f:
        f.write("select * from {{test_variable}}")

    # Test.
    render_jinja_template_file(
        template_path=TEST_TEMPLATE_FILE.name,
        output_dir_path=TEST_PROJECT_PATH,
        test_variable="test123",
    )

    with open(TEST_PROJECT_FILE, "r") as f:
        content = f.read()

    assert content == "select * from test123"

    # Cleanup.
    TEST_TEMPLATE_FILE.unlink()
    TEST_PROJECT_FILE.unlink()


def test_render_jinja_template_file_templated_filename():
    """Test that render_jinja_template_file() correctly renders a template
    if the template filename is itself templated."""

    # Assumptions.
    assert TEST_TEMPLATE_FILE_TEMPLATED_FILENAME.exists() is False

    # Create a test template file.
    with open(TEST_TEMPLATE_FILE_TEMPLATED_FILENAME, "w") as f:
        f.write("select * from {{test_variable}}")

    # Test.
    test_filename = "test_file"
    render_jinja_template_file(
        template_path=TEST_TEMPLATE_FILE_TEMPLATED_FILENAME.name,
        output_dir_path=TEST_PROJECT_PATH,
        test_filename=test_filename,
        test_variable="test123",
    )

    with open(TEST_PROJECT_PATH / (test_filename + ".sql"), "r") as f:
        content = f.read()

    assert content == "select * from test123"

    # Cleanup.
    TEST_TEMPLATE_FILE_TEMPLATED_FILENAME.unlink()
    TEST_PROJECT_FILE.unlink()


def test_render_project_files():
    render_project_files(
        project_name=TEST_PROJECT_NAME,
        data_architecture="marts",
        db_type="sqlserver",
        bronze_schema=TEST_BRONZE_SCHEMA,
        silver_schema=TEST_SILVER_SCHEMA,
        silver_schema_prefix="int",
        gold_layer_name=TEST_GOLD_LAYER,
        macros_path=config.macros_path,
        default_env=config.default_env,
        nesso_cli_version="v0.0.0",
        luma=True,
        snakecase_columns=True,
    )

    # CWD is tests/dbt_projects/postgres. The files will be rendered in a subfolder
    # named TEST_PROJECT_NAME.
    test_project_path = TEST_PROJECT_PATH.parent / "postgres" / TEST_PROJECT_NAME

    for file in TEMPLATE_FILES_TO_RENDER:
        file_path = test_project_path / file
        if file == "config.yml":
            file_path = test_project_path / ".nesso" / file
        elif file == "dbt_project.yml":
            assert file_path.exists()
            with open(file_path, "r") as f:
                project_config = yaml.load(f)
                assert project_config.get("name") == TEST_PROJECT_NAME
                assert config.macros_path in project_config.get("macro-paths")
                continue
        elif file == "README.md":
            assert file_path.exists()
            assert file_path.read_text().startswith(f"# {TEST_PROJECT_NAME}")
            continue
        elif file == "requirements.txt":
            assert file_path.exists()
            assert "sqlserver" in file_path.read_text()
            continue
        elif file == "packages.yml":
            assert file_path.exists()
            assert "tsql_utils" in file_path.read_text()
        elif file == "prepare.sh":
            assert file_path.exists()
            assert "microsoft" in file_path.read_text()
            continue
        elif file == "{{ bronze_schema }}.yml":
            # We check the project file, so need to use the rendered filename,
            # not the name of the template file, which is itself templated.
            rendered_file_name = TEST_BRONZE_SCHEMA + ".yml"
            file_path = (
                test_project_path
                / "models"
                / "sources"
                / TEST_BRONZE_SCHEMA
                / rendered_file_name
            )
        elif file == "CONTRIBUTING.md":
            assert file_path.exists()
            assert project_config.get("name") in file_path.read_text()
        assert file_path.exists()

    # Cleanup.
    shutil.rmtree(test_project_path, ignore_errors=True)


def test_create_profiles_yml_template():
    # Assumptions.
    assert TEST_EXAMPLE_PROFILES_PATH.exists() is False

    # Test.
    create_profiles_yml_template(
        db_type="sqlserver",
        project_name=TEST_PROJECT_NAME,
        profiles_path=TEST_EXAMPLE_PROFILES_PATH,
        driver="test_driver",
        host="test_host",
        port=1234,
        database="test_database",
    )
    with open(TEST_EXAMPLE_PROFILES_PATH, "r") as f:
        config = yaml.load(f)

    expected_config = {
        TEST_PROJECT_NAME: {
            "target": "dev",
            "outputs": {
                "dev": DBTSQLServerConfig(
                    database="test_database",
                    host="test_host",
                    port=1234,
                    driver="test_driver",
                ).dict(by_alias=True),
            },
        }
    }
    assert config == expected_config

    # Cleanup.
    TEST_EXAMPLE_PROFILES_PATH.unlink()


def test__generate_user_profile():
    # Assumptions.
    assert TEST_EXAMPLE_PROFILES_PATH.exists() is False

    # Create a template profiles.yml to be used as basis for user config.
    create_profiles_yml_template(
        db_type="sqlserver",
        project_name=TEST_PROJECT_NAME,
        profiles_path=TEST_EXAMPLE_PROFILES_PATH,
        driver="test_driver",
        host="test_host",
        port=1234,
        database="test_database",
    )

    profile = _generate_user_profile(
        user="test_user",
        password="test_password",
        schema="test_schema",
        template_profiles_yml_path=TEST_EXAMPLE_PROFILES_PATH,
    )

    expected_profile_config = DBTSQLServerConfig(
        database="test_database",
        host="test_host",
        port=1234,
        driver="test_driver",
        user="test_user",
        password="test_password",
        schema="test_schema",
    ).dict(by_alias=True)

    # Use NessoDBTConfig to avoid hardcoding any values.
    profile_template = NessoDBTConfig(
        db_type="sqlserver", project_name=TEST_PROJECT_NAME
    ).dict(by_alias=True)
    target = profile_template[TEST_PROJECT_NAME]["target"]
    profile_template[TEST_PROJECT_NAME]["outputs"][target].update(
        expected_profile_config
    )

    expected_profile = profile_template

    assert profile == expected_profile

    # Cleanup.
    TEST_EXAMPLE_PROFILES_PATH.unlink()


def test_init_user():
    TEST_USER_PROFILES_PATH = TEST_PROJECT_PATH.joinpath("test_profile.yml")

    # Assumptions.
    assert TEST_EXAMPLE_PROFILES_PATH.exists() is False
    assert TEST_USER_PROFILES_PATH.exists() is False

    # Create a template profiles.yml to be used as basis for user config.
    create_profiles_yml_template(
        db_type="sqlserver",
        project_name=TEST_PROJECT_NAME,
        profiles_path=TEST_EXAMPLE_PROFILES_PATH,
        driver="test_driver",
        host="test_host",
        port=1234,
        database="test_database",
    )

    result = runner.invoke(
        app,
        [
            "init",
            "user",
            "--user",
            "test_user",
            "--password",
            "test_password",
            "--schema",
            "test_schema",
            "--template-profiles-yml-path",
            str(TEST_EXAMPLE_PROFILES_PATH),
            "--profiles-path",
            str(TEST_USER_PROFILES_PATH),
            "--no-install-dependencies",
        ],
    )
    assert result.exit_code == 0
    assert TEST_USER_PROFILES_PATH.exists()

    expected_profile_config = DBTSQLServerConfig(
        database="test_database",
        host="test_host",
        port=1234,
        driver="test_driver",
        user="test_user",
        password="test_password",
        schema="test_schema",
    ).dict(by_alias=True)

    # Use NessoDBTConfig to avoid hardcoding any values.
    profile_template = NessoDBTConfig(
        db_type="sqlserver", project_name=TEST_PROJECT_NAME
    ).dict(by_alias=True)
    target = profile_template[TEST_PROJECT_NAME]["target"]
    profile_template[TEST_PROJECT_NAME]["outputs"][target].update(
        expected_profile_config
    )

    expected_profile = profile_template

    with open(TEST_USER_PROFILES_PATH, "r") as f:
        profile = yaml.load(f)

    assert profile == expected_profile

    # Cleanup.
    TEST_EXAMPLE_PROFILES_PATH.unlink()
    TEST_USER_PROFILES_PATH.unlink()


def test_init_project():
    # CWD is tests/dbt_projects/postgres. The files will be created in a subfolder
    # named TEST_PROJECT_NAME.
    test_project_path = TEST_PROJECT_PATH.parent / "postgres" / TEST_PROJECT_NAME

    db_kwargs = json.dumps(
        {"host": "test_host", "port": 8080, "dbname": "test_db", "path": "fake_path"}
    )
    result = runner.invoke(
        app,
        [
            "init",
            "project",
            "--project-name",
            TEST_PROJECT_NAME,
            "--db-kwargs",
            db_kwargs,
            "--no-install-dependencies",
        ],
    )
    error_msg = f"Exit code: {result.exit_code}, stdout:\n{result.stdout}"
    assert result.exit_code == 0, error_msg

    # Cleanup.
    shutil.rmtree(test_project_path)
