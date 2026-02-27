import os
import importlib

from pathlib import Path
import sys

# ensure app package on path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

import config


def test_default_values_present():
    # defaults should be numbers and greater than zero
    assert config.DEFAULT_PURCHASE_PRICE > 0
    assert config.DEFAULT_EQUITY >= 0
    assert config.DEFAULT_INTEREST_RATE >= 0
    assert config.DEFAULT_INITIAL_AMORTIZATION >= 0
    assert isinstance(config.DEFAULT_INTEREST_BINDING_YEARS, int)


def test_env_overrides(monkeypatch):
    # set environment variables and reload module
    monkeypatch.setenv("DEFAULT_PURCHASE_PRICE", "123456")
    monkeypatch.setenv("DEFAULT_EQUITY", "5000")
    monkeypatch.setenv("DEFAULT_INTEREST_RATE", "1.5")
    monkeypatch.setenv("DEFAULT_INITIAL_AMORTIZATION", "0.5")
    monkeypatch.setenv("DEFAULT_INTEREST_BINDING_YEARS", "7")
    monkeypatch.setenv("DEFAULT_ANNUAL_SPECIAL_PAYMENT", "250")

    # reload config to pick up changed env
    importlib.reload(config)

    assert config.DEFAULT_PURCHASE_PRICE == 123456
    assert config.DEFAULT_EQUITY == 5000
    assert config.DEFAULT_INTEREST_RATE == 1.5
    assert config.DEFAULT_INITIAL_AMORTIZATION == 0.5
    assert config.DEFAULT_INTEREST_BINDING_YEARS == 7
    assert config.DEFAULT_ANNUAL_SPECIAL_PAYMENT == 250
