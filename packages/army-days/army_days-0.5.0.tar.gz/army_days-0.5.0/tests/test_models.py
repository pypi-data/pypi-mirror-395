from datetime import datetime

from army_days.models import ConfigModel, DaysModel, EntryModel


def test_config_model():
    blank_model = ConfigModel()
    assert blank_model is not None
    assert blank_model.use_army_butt_days is False
    assert blank_model.show_completed is False


def test_days_model():
    blank_model = DaysModel(config=ConfigModel(), entries=[])
    assert blank_model is not None


def test_entry_model():
    simple_model = EntryModel(title="nothing", date=datetime(1, 1, 1))
    assert simple_model is not None
    assert simple_model.always_show is False
    assert simple_model.show_past_limit is None


def test_entry_model_with_always_show():
    model = EntryModel(title="test event", date=datetime(2024, 1, 1), always_show=True, show_past_limit=400)
    assert model.always_show is True
    assert model.show_past_limit == 400


def test_entry_model_with_alias():
    # Test that camelCase aliases work
    model = EntryModel(title="test", date=datetime(2024, 1, 1), alwaysShow=True, showPastLimit=365)
    assert model.always_show is True
    assert model.show_past_limit == 365
