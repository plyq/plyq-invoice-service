"""Test config"""
import os

from app.config.service import Config


class TestConfig0:
    """Test config correct attributes"""

    def test_from_file0(self) -> None:
        """Test that config0.json was readed correctly."""
        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "resources", "config0.json"
        )
        config = Config.from_file(config_path)
        assert config.level0_0.level1_0 == "00"
        assert config.level0_0.level1_1.level2_0 == "010"
        assert config.level0_1.level1_0 == "10"

    def test_dict0(self) -> None:
        """Test that config from dict was readed correctly."""
        config = Config.from_nested_dicts({"a": {"b": {"c": "d"}}})
        assert config.a.b.c == "d"
