from dataclasses import dataclass

from argparse_boost import from_dict


def test_parse_nested_dataclass_from_flat_dict_keys():
    @dataclass
    class DBConfig:
        url: str

    @dataclass
    class Config:
        db: DBConfig

    config = from_dict(
        {"db_url": "sqlite:///test.db"},
        Config,
    )
    assert config.db.url == "sqlite:///test.db"


def test_parse_nested_dataclass_from_dataclass():
    @dataclass
    class DBConfig:
        url: str

    @dataclass
    class Config:
        db: DBConfig

    config = from_dict(
        {"db": DBConfig(url="sqlite:///test.db")},
        Config,
    )
    assert config.db.url == "sqlite:///test.db"


def test_parse_nested_dataclass_from_dict():
    @dataclass
    class DBConfig:
        url: str

    @dataclass
    class Config:
        db: DBConfig

    config = from_dict(
        {"db": {"url": "sqlite:///test.db"}},
        Config,
    )
    assert config.db.url == "sqlite:///test.db"
