from config.settings import settings


def test_environment_loaded():
    assert settings.ENVIRONMENT in ["dev", "staging", "prod"]


def test_openai_key_exists():
    # Optional: Just to check it's set (can be mocked in real tests)
    assert isinstance(settings.OPENAI_API_KEY, str)


def test_database_uri_format():
    assert settings.DATABASE_URI == "host=localhost port=5432 user=postgres password=postgres dbname=postgres"
