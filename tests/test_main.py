from quick_zip.core.config import APP_VERSION, CONFIG_FILE, generate_config
from quick_zip.schema.config import AppConfig


def test_version():
    assert APP_VERSION == "v0.1.0"


class ConfigTests:
    @staticmethod
    def test_generate_config():
        app_config = generate_config(CONFIG_FILE)

        assert isinstance(app_config, AppConfig)
        test_config = AppConfig(
            enable_webhooks=False,
            webhook_address="https://webhooks.com/webhook",
        )

        assert app_config.enable_webhooks == test_config.enable_webhooks
        assert app_config.webhook_address == test_config.webhook_address
