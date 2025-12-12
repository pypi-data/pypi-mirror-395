"""
設定ファイル管理モジュール

TOML形式の設定ファイルを読み込み、環境変数と組み合わせて設定を提供する。
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import tomllib
except ImportError:
    import tomli as tomllib


@dataclass
class ApiConfig:
    """API設定"""
    google_api_key: Optional[str] = None


@dataclass
class DefaultsConfig:
    """デフォルト設定"""
    image_backend: str = "gemini"
    default_style: str = "yonkoma"
    default_ratio: str = "9:16"
    default_panels: int = 4
    default_output_dir: Optional[str] = None
    default_character: Optional[str] = None


@dataclass
class OutputConfig:
    """出力設定"""
    base_width: int = 1080
    quality: int = 95


@dataclass
class Config:
    """全体設定"""
    api: ApiConfig = field(default_factory=ApiConfig)
    defaults: DefaultsConfig = field(default_factory=DefaultsConfig)
    output: OutputConfig = field(default_factory=OutputConfig)


def find_config_file() -> Optional[Path]:
    """設定ファイルを探す"""
    # 探索する場所（優先順）
    search_paths = [
        Path.cwd() / "config.toml",
        Path.home() / ".config" / "enikki" / "config.toml",
    ]

    for path in search_paths:
        if path.exists():
            return path

    return None


def load_config(config_path: Optional[Path] = None) -> Config:
    """設定を読み込む"""
    config = Config()

    # 設定ファイルを探す
    if config_path is None:
        config_path = find_config_file()

    # 設定ファイルがあれば読み込む
    if config_path and config_path.exists():
        with open(config_path, "rb") as f:
            data = tomllib.load(f)

        # API設定
        if "api" in data:
            api_data = data["api"]
            config.api.google_api_key = api_data.get("google_api_key")

        # デフォルト設定
        if "defaults" in data:
            defaults_data = data["defaults"]
            if "image_backend" in defaults_data:
                config.defaults.image_backend = defaults_data["image_backend"]
            if "default_style" in defaults_data:
                config.defaults.default_style = defaults_data["default_style"]
            if "default_ratio" in defaults_data:
                config.defaults.default_ratio = defaults_data["default_ratio"]
            if "default_panels" in defaults_data:
                config.defaults.default_panels = defaults_data["default_panels"]
            if "default_output_dir" in defaults_data:
                config.defaults.default_output_dir = defaults_data["default_output_dir"]
            if "default_character" in defaults_data:
                config.defaults.default_character = defaults_data["default_character"]

        # 出力設定
        if "output" in data:
            output_data = data["output"]
            if "base_width" in output_data:
                config.output.base_width = output_data["base_width"]
            if "quality" in output_data:
                config.output.quality = output_data["quality"]

    # 環境変数で上書き（GEMINI_API_KEY または GOOGLE_API_KEY）
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        config.api.google_api_key = api_key
    if os.environ.get("ENIKKI_BACKEND"):
        config.defaults.image_backend = os.environ["ENIKKI_BACKEND"]

    return config


# グローバル設定インスタンス（遅延初期化）
_config: Optional[Config] = None


def get_config() -> Config:
    """設定を取得（シングルトン）"""
    global _config
    if _config is None:
        _config = load_config()
    return _config


def reload_config(config_path: Optional[Path] = None) -> Config:
    """設定を再読み込み"""
    global _config
    _config = load_config(config_path)
    return _config
