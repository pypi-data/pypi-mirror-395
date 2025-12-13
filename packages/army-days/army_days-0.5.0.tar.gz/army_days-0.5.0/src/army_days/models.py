from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

DisplayFormat = Literal["days", "weeks", "months", "years", "auto"]


class ConfigModel(BaseModel):
    model_config = {"populate_by_name": True}

    use_army_butt_days: bool = Field(default=False, alias="useArmyButtDays")
    show_completed: bool = Field(default=False, alias="showCompleted")
    default_display_format: DisplayFormat = Field(default="days", alias="defaultDisplayFormat")
    max_days_future: int | None = Field(default=None, alias="maxDaysFuture")


class EntryModel(BaseModel):
    model_config = {"populate_by_name": True}

    title: str
    date: datetime
    always_show: bool = Field(default=False, alias="alwaysShow")
    show_past_limit: int | None = Field(default=None, alias="showPastLimit")
    display_format: DisplayFormat | None = Field(default=None, alias="displayFormat")


class DaysModel(BaseModel):
    config: ConfigModel
    entries: list[EntryModel]


class ComputedEventModel(EntryModel):
    days: float
    display_format_resolved: DisplayFormat
