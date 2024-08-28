from dataclasses import dataclass
from typing import Any

import pandas as pd
import streamlit as st
from pandas.api.types import is_numeric_dtype


@dataclass
class Channel:
    name: str
    log: bool = False
    abs: bool = False  # TODO: absolute valuee (numeric)
    std: bool = False  # TODO: number of std deviations from the mean (numeric)

    @classmethod
    def from_ui(
        cls,
        df: pd.DataFrame,
        label: str,
        columns: list[str] | None = None,
        default: str | None = None,
    ):
        if columns is None:
            columns = list(df.columns)

        # Might have to set the default this way – streamlit bug??
        _default = st.session_state.get(f"{label}_channel", default)
        index = columns.index(_default) if _default is not None else 0

        def set_session_value(key: str, value: Any) -> None:
            col = st.session_state.get(f"{label}_channel")
            if col is not None and not is_numeric_dtype(df[col]):
                st.session_state[key] = value

        left, right = st.columns((2, 1))
        with left:
            col = st.selectbox(
                f"{label} channel",
                options=columns,
                label_visibility="collapsed",
                key=f"{label}_channel",
                on_change=set_session_value(f"log_{label}", False),
                index=index,
            )
            col = str(col)
        with right.popover(label, use_container_width=True):
            log = st.checkbox(
                "log",
                key=f"log_{label}",
                disabled=not is_numeric_dtype(df[col]),
            )
            # TODO: reverse
            # TODO: abs
            # TODO: sigma clip?
        return cls(name=col, log=log)
