# Copyright (C) 2025 Sawyer Rensel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# ---

# For the full text of the GNU General Public License v3.0, visit:
# https://www.gnu.org/licenses/gpl-3.0.txt

from mkdocs.config import config_options

class GraphConfig(config_options.Config):
    """
    Graph plugin configuration.
    """
    enabled = config_options.Type(bool, default=True)

    # Local graph settings (mini graph in sidebar)
    local_graph_depth = config_options.Type(int, default=1)

    # Global graph settings
    global_graph = config_options.Type(bool, default=True)

    # Physics simulation settings
    repel_force = config_options.Type(float, default=1.0)
    center_force = config_options.Type(float, default=0.2)
    link_distance = config_options.Type(int, default=50)

    # Visual settings
    scale = config_options.Type(float, default=1.1)
    font_size = config_options.Type(int, default=10)
    show_tags = config_options.Type(bool, default=False)

    # Interaction settings
    enable_drag = config_options.Type(bool, default=True)
    enable_zoom = config_options.Type(bool, default=True)
    focus_on_hover = config_options.Type(bool, default=True)
