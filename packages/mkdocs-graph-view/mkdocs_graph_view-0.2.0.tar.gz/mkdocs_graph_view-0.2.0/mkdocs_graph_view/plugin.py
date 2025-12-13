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

import os
import json
import logging
import shutil
from html.parser import HTMLParser
from urllib.parse import urljoin

from mkdocs import utils
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from .config import GraphConfig

log = logging.getLogger("mkdocs.material.plugins.graph")

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.links.append(value)

class GraphPlugin(BasePlugin[GraphConfig]):
    def __init__(self):
        self.nodes = {}  # Use dict to avoid duplicates
        self.links = []
        self.page_tags = {}  # Store tags for each page if available
        self.tags_index_url = None  # URL of the tags index page

    def on_page_content(self, html, page, config, files):
        # Check if this page is the tags index
        # Material for MkDocs tags plugin uses this marker
        if '<!-- material/tags -->' in html:
            self.tags_index_url = page.url
            log.info(f"Graph plugin: Tags index marker found in HTML for page: {page.url}")

        # Also check the raw markdown file content
        if hasattr(page, 'file') and hasattr(page.file, 'src_path'):
            src_path = os.path.join(config['docs_dir'], page.file.src_path)
            try:
                with open(src_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '<!-- material/tags -->' in content:
                        self.tags_index_url = page.url
                        log.info(f"Graph plugin: Tags index marker found in source for page: {page.url}")
            except Exception as e:
                log.debug(f"Graph plugin: Could not read source file {src_path}: {e}")

        # Check if graph should be hidden on this page
        if hasattr(page, 'meta') and 'hide' in page.meta:
            hide_list = page.meta.get('hide', [])
            if isinstance(hide_list, str):
                hide_list = [hide_list]
            if 'graph' in hide_list:
                # Skip graph injection for this page
                return html

        # Extract links
        parser = LinkParser()
        parser.feed(html)

        # Extract tags if available (from page metadata)
        tags = []
        if hasattr(page, 'meta') and 'tags' in page.meta:
            tags = page.meta.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]

        # Add node (using dict to avoid duplicates)
        self.nodes[page.url] = {
            "id": page.url,
            "title": page.title,
            "tags": tags,
            "group": 1
        }

        # Process links
        for link in parser.links:
            # Ignore external links, anchors, mailto
            if link.startswith(("http", "https", "mailto", "tel", "#")):
                continue

            # Remove anchor
            url = link.split("#")[0]
            if not url:
                continue

            # Resolve relative URL
            target = urljoin(page.url, url)

            self.links.append({
                "source": page.url,
                "target": target,
                "value": 1
            })

        # Inject base url and config for graph
        rel_root = utils.get_relative_url(".", page.url)
        if rel_root != "." and not rel_root.endswith("/"):
             rel_root += "/"
        elif rel_root == ".":
             rel_root = ""

        # Pass configuration to frontend
        graph_config = {
            "local_graph_depth": self.config.local_graph_depth,
            "global_graph": self.config.global_graph,
            "repel_force": self.config.repel_force,
            "center_force": self.config.center_force,
            "link_distance": self.config.link_distance,
            "scale": self.config.scale,
            "font_size": self.config.font_size,
            "show_tags": self.config.show_tags,
            "enable_drag": self.config.enable_drag,
            "enable_zoom": self.config.enable_zoom,
            "focus_on_hover": self.config.focus_on_hover
        }

        script = f'''<script>
var graph_base_url = "{rel_root}";
var graph_current_page = "{page.url}";
var graph_config = {json.dumps(graph_config)};
</script>'''
        return script + html

    def on_post_build(self, config):
        # Convert nodes dict to list
        nodes_list = list(self.nodes.values())

        # If show_tags is enabled, create tag nodes and links
        if self.config.show_tags:
            tag_nodes = {}  # Dict to track unique tags
            tag_links = []  # Links from pages to tags

            if self.tags_index_url:
                log.info(f"Graph plugin: Tags index detected at {self.tags_index_url}")
            else:
                log.info("Graph plugin: No tags index detected")

            # Collect all tags and create tag nodes
            for node in nodes_list:
                if node.get("tags"):
                    for tag in node["tags"]:
                        # Create a unique ID for the tag node
                        tag_id = f"tag:{tag}"

                        # Add tag node if not already present
                        if tag_id not in tag_nodes:
                            # Create URL for tag (points to tags index with anchor)
                            tag_url = None
                            if self.tags_index_url:
                                # Material for MkDocs uses "tag:{slug}" format for anchors
                                tag_slug = tag.lower().replace(' ', '-')
                                tag_url = f"{self.tags_index_url}#tag:{tag_slug}"
                                log.info(f"Graph plugin: Created tag node '{tag}' with URL: {tag_url}")

                            tag_nodes[tag_id] = {
                                "id": tag_id,
                                "title": f"#{tag}",
                                "tags": [],
                                "group": 2,  # Different group for tags
                                "url": tag_url  # URL to tags index anchor
                            }

                        # Create link from page to tag
                        tag_links.append({
                            "source": node["id"],
                            "target": tag_id,
                            "value": 1
                        })

            # Add tag nodes to the nodes list
            nodes_list.extend(tag_nodes.values())

            # Add tag links to the links list
            self.links.extend(tag_links)

        # Filter links to ensure target exists in nodes
        node_ids = set(node["id"] for node in nodes_list)
        valid_links = [l for l in self.links if l["target"] in node_ids]

        # Remove self-loops
        valid_links = [l for l in valid_links if l["source"] != l["target"]]

        # Count link frequencies for weight
        link_counts = {}
        for link in valid_links:
            key = (link["source"], link["target"])
            link_counts[key] = link_counts.get(key, 0) + 1

        # Deduplicate links and add weights
        unique_links = []
        seen = set()
        for link in valid_links:
            key = (link["source"], link["target"])
            if key not in seen:
                seen.add(key)
                unique_links.append({
                    "source": link["source"],
                    "target": link["target"],
                    "value": link_counts[key]
                })

        graph_data = {
            "nodes": nodes_list,
            "links": unique_links
        }

        # Write graph.json
        output_path = os.path.join(config["site_dir"], "graph.json")
        with open(output_path, "w") as f:
            json.dump(graph_data, f, indent=2)

        log.info(f"Graph plugin: Generated graph with {len(nodes_list)} nodes and {len(unique_links)} links")

        # Copy assets
        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_src = os.path.join(base_path, "assets")
        assets_dst = os.path.join(config["site_dir"], "assets")

        js_dst = os.path.join(assets_dst, "javascripts", "graph.js")
        css_dst = os.path.join(assets_dst, "stylesheets", "graph.css")

        os.makedirs(os.path.dirname(js_dst), exist_ok=True)
        os.makedirs(os.path.dirname(css_dst), exist_ok=True)

        shutil.copy(os.path.join(assets_src, "javascripts", "graph.js"), js_dst)
        shutil.copy(os.path.join(assets_src, "stylesheets", "graph.css"), css_dst)

    def on_config(self, config):
        if not self.config.enabled:
            return
            
        config["extra_javascript"].append("https://d3js.org/d3.v7.min.js")
        config["extra_javascript"].append("assets/javascripts/graph.js")
        config["extra_css"].append("assets/stylesheets/graph.css")
