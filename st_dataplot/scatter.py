from dataclasses import dataclass, field
from typing import Any, Callable, Literal, cast

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_string_dtype,
)

from .channel import Channel
from .plotly_templates import Templates, colormaps


@dataclass
class ScatterPlot:
    x: Channel
    y: Channel
    s: Channel
    c: Channel
    z: str | None = None
    z_reverse: bool = False
    opacity: float = 1
    grid: Literal["", "both", "x", "y"] = "both"
    title_col: str | None = "pl_name"  # TODO
    colormap: Any = field(default_factory=lambda: colormaps["burg"])

    template: str = "basic"
    width: int = 800
    height: int = 800

    format: Callable[[str], str] | None = None
    hover_cols: list[str] | None = None

    @classmethod
    def from_ui(
        cls,
        df: pd.DataFrame,
        label_format_func: Callable[[str], str] | None = None,
        default_x: str | None = None,
        default_y: str | None = None,
        default_s: str | None = None,
        default_c: str | None = None,
        popover_label: str = "plot settings",
        title_col: str | None = None,
    ):
        plottable_cols = cls._get_plottable_cols(df)
        df = df[plottable_cols]

        numeric_cols = [c for c in df.columns if is_numeric_dtype(df[c])]
        x_settings = Channel.from_ui(df, "x", default=default_x)
        y_settings = Channel.from_ui(df, "y", default=default_y)
        s_settings = Channel.from_ui(df[numeric_cols], "s", default=default_s)
        c_settings = Channel.from_ui(df[numeric_cols], "c", default=default_c)
        # TODO: Shape -- boolean/categorical channels only (maybe binned numerical??)

        with st.popover(popover_label, use_container_width=True):
            _cmaps = [c for c in colormaps.keys() if not c.endswith("_r")]

            opacity = int(st.slider("opacity", 1, 100, 85)) / 100

            left, right = st.columns(2)
            with left:
                z = st.selectbox("z_order", [""] + plottable_cols)
                z_asc = st.checkbox("reversed", key="z_reverse", disabled=not z)
            with right:
                cmap = st.selectbox("colormap", _cmaps, index=_cmaps.index("curl"))
                cmap = str(cmap) + "_r" if right.checkbox("reversed", True) else cmap

            st.divider()

            left, right = st.columns(2)
            with left:
                template = str(st.selectbox("style template", Templates.keys()))
                width = st.number_input("width", 200, 3000, 800, step=50)
            with right:
                grids = str(st.selectbox("gridlines", ["", "both", "x", "y"], 1))
                height = st.number_input("height", 200, 3000, 600, step=50)

            hover_cols = st.multiselect("hover cols", df.columns)

            # TODO
            # hover columns
            # cycle axes
            # st.download_button()

        config = cls(
            x=x_settings,
            y=y_settings,
            s=s_settings,
            c=c_settings,
            z=z,
            z_reverse=z_asc,
            template=template,
            grid=cast(Literal["", "both", "x", "y"], grids),
            colormap=colormaps[str(cmap)],
            opacity=opacity,
            format=label_format_func,
            width=int(width),
            height=int(height),
            title_col=title_col or plottable_cols[0],
            hover_cols=hover_cols,
        )
        return config

    # @staticmethod
    # def set_defaults(
    #     x_channel: str | None = None,
    #     y_channel: str | None = None,
    #     s_channel: str | None = None,
    #     c_channel: str | None = None,
    # ):
    #     dict()
    #     ...

    def make_fig(self, df: pd.DataFrame) -> go.Figure:
        if self.z:
            df = df.sort_values(self.z, ascending=not self.z_reverse)

        x_data = df[self.x.name]
        y_data = df[self.y.name]

        x_title = self.format(self.x.name) if self.format is not None else self.x.name
        y_title = self.format(self.y.name) if self.format is not None else self.y.name
        c_title = self.format(self.c.name) if self.format is not None else self.c.name
        if self.c.log:
            c_title = f"{c_title} (scaled)"

        hover_template, hover_data = self.get_hover_info(df)

        # TODO: Hover data for size/color should never be logged. Log should be applied to
        # size and color *values* instead.

        extra_marker_settings = {}
        if self.template == "formal":
            extra_marker_settings.update(
                colorbar_title_side="right",
                colorbar_title_font_size=20,
                colorbar_tickfont_size=18,
                colorbar_tickfont_family="Times New Roman, serif",
            )

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x_data,
                y=y_data,
                mode="markers+text",
                marker=dict(
                    size=self.normalize_size(df, self.s),
                    color=self.normalize_color(df, self.c),
                    colorbar_title_text=c_title,
                    colorscale=self.colormap,
                    opacity=self.opacity,
                    **Templates[self.template].marker_settings,
                ),
                hoverinfo="text",
                hovertemplate=hover_template,
                customdata=hover_data,
                name="",
            )
        )
        fig.update_xaxes(
            type="log" if self.x.log else None,
            title_text=x_title,
            showgrid=bool(self.grid in ["x", "both"]),
        )
        fig.update_yaxes(
            type="log" if self.y.log else None,
            title_text=y_title,
            showgrid=bool(self.grid in ["y", "both"]),
        )
        fig.update_layout(**Templates[self.template].layout._props)
        fig.update_layout(width=self.width, height=self.height)
        return fig

    def display(self, fig: go.Figure, filename: str, **kwargs: Any) -> Any:
        """Wrapper around st.plotly chart that handles theming appropriately."""
        theme = "streamlit" if self.template == "basic" else None
        config = dict(
            toImageButtonOptions={
                "format": "png",
                "filename": filename,
                "width": self.width,
                "height": self.height,
                "scale": 5,
            },
        )
        return st.plotly_chart(
            fig, use_container_width=True, theme=theme, config=config, **kwargs
        )

    @staticmethod
    def download_button(
        fig: go.Figure,
        filename: str,
        label: str = "save plot",
        format: str = "png",
        **kwargs: Any,
    ) -> bool:
        """Wrapper around st.download_button that handles theming appropriately."""
        img_bytes = fig.to_image(format=format, scale=5)
        return st.download_button(
            label,
            data=img_bytes,
            file_name=filename,
            use_container_width=True,
            **kwargs,
        )

    def get_hover_info(self, df: pd.DataFrame):
        hovertemplate = (
            "<b><span style='font-size: 1.8em;'>%{customdata[0]}</span></b><br>"
            f"<b>{self.x.name}:</b> %{{customdata[1]:.4g}}<br>"
            f"<b>{self.y.name}:</b> %{{customdata[2]:.4g}}<br>"
        )
        hover_cols = [
            self.title_col,
            self.x.name,
            self.y.name,
            self.s.name,
            self.c.name,
            *(self.hover_cols if self.hover_cols is not None else []),
        ]
        hover_cols = self.remove_duplicates(hover_cols)

        # TODO: Handle missing values more elegantly
        custom_data = df[hover_cols]
        for i, column in enumerate(hover_cols[3:]):
            # custom_data[column] = custom_data[column].apply(format_value)
            hovertemplate += f"<b>{column}:</b>"
            hovertemplate += " %{customdata[" + str(3 + i) + "]"
            if pd.api.types.is_float_dtype(df[column]):
                hovertemplate += ":.4g"
            hovertemplate += "}<br>"
        return hovertemplate, custom_data

    @staticmethod
    def _get_plottable_cols(df: pd.DataFrame) -> list[str]:
        """Returns only the columns that can be set as x, y, size, or color channels."""

        return list(
            filter(
                lambda col: (
                    is_numeric_dtype(df[col])
                    or is_bool_dtype(df[col])
                    or is_datetime64_any_dtype(df[col])
                    or is_string_dtype(df[col])
                ),
                df.columns,
            )
        )

    @staticmethod
    def normalize_size(df: pd.DataFrame, channel: Channel) -> pd.Series:
        size = df[channel.name]
        if channel.log:
            min_val = size.min()
            size = size - min_val + np.abs(min_val)
            size = np.log(size)
            size = (size - size.min()) / (size.max() - size.min())
            min_size, max_size = 10, 50
            size = size * (max_size - min_size) + min_size
        else:
            size = (size - size.min()) / (size.max() - size.min())
            min_size, max_size = 4, 50
            size = size * (max_size - min_size) + min_size
        size = size.fillna(size.median())
        return size

    @staticmethod
    def normalize_color(df: pd.DataFrame, channel: Channel) -> pd.Series:
        color = df[channel.name]
        if is_bool_dtype(color):
            color = color.map({False: 0, True: 1}).astype(int)
        elif channel.log and is_numeric_dtype(color):
            min_val = color.min()
            color = color - min_val + np.abs(min_val)
            color = np.log10(color)
        return color

    @staticmethod
    def remove_duplicates(cols: list[str]) -> list[str]:
        new_cols = []
        for col in cols:
            if col not in new_cols:
                new_cols.append(col)
        return new_cols
