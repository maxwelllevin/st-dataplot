from dataclasses import dataclass, field
from typing import Any

import plotly.express as px
import plotly.graph_objects as go


@dataclass
class Template:
    layout: go.Layout
    marker_settings: dict[str, Any] = field(default_factory=dict)


basic = Template(layout=go.Layout(), marker_settings=dict(colorbar_title_side="right"))
formal = Template(
    layout=go.Layout(
        font=dict(family="Times New Roman, serif", size=10),
        xaxis=dict(
            showline=True,
            linecolor="black",
            linewidth=4,
            ticks="outside",
            tickfont=dict(size=18),
            title=dict(font=dict(size=20)),
            mirror=True,
        ),
        xaxis2=dict(
            showline=True, linecolor="black", linewidth=4, mirror=True, ticks="outside"
        ),
        yaxis=dict(
            showline=True,
            linecolor="black",
            linewidth=4,
            ticks="outside",
            tickfont=dict(size=18),
            title=dict(font=dict(size=20)),
            mirror=True,
        ),
        hoverlabel=dict(
            bgcolor="rgba(0, 0, 0, 0.05)",  # Adjust the opacity here (0.8 for 80% opacity)
            font_size=14,
            font_family="Times New Roman, serif",
        ),
        margin=dict(l=60, r=0, t=25, b=60),
    ),
    marker_settings=dict(
        colorbar_title_side="right",
        colorbar_title_font_size=20,
        colorbar_tickfont_size=18,
        colorbar_tickfont_family="Times New Roman, serif",
    ),
)

Templates = dict(
    basic=basic,
    formal=formal,
)


colormaps = {
    # cmocean:
    "algae": px.colors.cmocean.algae,
    "algae_r": px.colors.cmocean.algae_r,
    "balance": px.colors.cmocean.balance,
    "balance_r": px.colors.cmocean.balance_r,
    "curl": px.colors.cmocean.curl,
    "curl_r": px.colors.cmocean.curl_r,
    "deep": px.colors.cmocean.deep,
    "deep_r": px.colors.cmocean.deep_r,
    "matter": px.colors.cmocean.matter,
    "matter_r": px.colors.cmocean.matter_r,
    "ice": px.colors.cmocean.ice,
    "ice_r": px.colors.cmocean.ice_r,
    "oxy": px.colors.cmocean.oxy,
    "oxy_r": px.colors.cmocean.oxy_r,
    # "solar": px.colors.cmocean.solar,
    # "solar_r": px.colors.cmocean.solar_r,
    "thermal": px.colors.cmocean.thermal,
    "thermal_r": px.colors.cmocean.thermal_r,
    # diverging:
    # "diverging: Earth": px.colors.diverging.Earth,
    # "diverging: Earth_r": px.colors.diverging.Earth_r,
    # "diverging: Portland": px.colors.diverging.Portland,
    # "diverging: Portland_r": px.colors.diverging.Portland_r,
    # "diverging: RdBu": px.colors.diverging.RdBu,
    # "diverging: RdBu_r": px.colors.diverging.RdBu_r,
    # "diverging: RdYlBu": px.colors.diverging.RdYlBu,
    # "diverging: RdYlBu_r": px.colors.diverging.RdYlBu_r,
    "diverging: Tropic": px.colors.diverging.Tropic,
    "diverging: Tropic_r": px.colors.diverging.Tropic_r,
    # carto
    # "bold": px.colors.carto.Bold,
    # "bold_r": px.colors.carto.Bold_r,
    "temps": px.colors.carto.Temps,
    "temps_r": px.colors.carto.Temps_r,
    "burg": px.colors.carto.Burg,
    "burg_r": px.colors.carto.Burg_r,
    # "burgyl": px.colors.carto.Burgyl,
    # "burgyl_r": px.colors.carto.Burgyl_r,
    "darkmint": px.colors.carto.Darkmint,
    "darkmint_r": px.colors.carto.Darkmint_r,
    # "prism": px.colors.carto.Prism,
    # "prism_r": px.colors.carto.Prism_r,
    # "sunset": px.colors.carto.Sunset,
    # "sunset_r": px.colors.carto.Sunset_r,
    "sunsetdark": px.colors.carto.Sunsetdark,
    "sunsetdark_r": px.colors.carto.Sunsetdark_r,
    # cyclic
    # "cyclic: Twilight": px.colors.cyclical.Twilight,
    # "cyclic: Twilight_r": px.colors.cyclical.Twilight_r,
}
