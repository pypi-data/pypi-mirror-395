"""
This file contains sphinx directives for rendering a 122 or a 214 spec given it's filename root.
"""
from typing import Dict, List
from collections import defaultdict

from docutils import nodes, statemachine
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import ListTable
from sphinx.util.nodes import nested_parse_with_titles

from dkist_fits_specifications.dataset_extras import (
    load_full_dataset_extra,
    load_raw_dataset_extra,
)
from dkist_fits_specifications.spec122 import load_spec122
from dkist_fits_specifications.spec214 import load_full_spec214, load_raw_spec214


class BaseSpecTable(ListTable):
    """
    Given a pre-loaded representation of a spec table render it.
    """

    option_spec = {"header-level": directives.single_char_or_unicode}

    # Stolen from https://github.com/sphinx-doc/sphinx/issues/8039
    # A method which takes an arbitary rst string and converts it to Nodes
    def convert_rst_to_nodes(self, rst_source: str) -> List[nodes.Node]:
        """Turn an RST string into a node that can be used in the document."""
        node = nodes.Element()
        node.document = self.state.document
        nested_parse_with_titles(
            state=self.state,
            content=statemachine.ViewList(
                statemachine.string2lines(rst_source),
                # The following line isn't used but it sometimes reported in error messages
                source=f"[Custom rst preamble for {self.arguments[0]} table]",
            ),
            node=node,
        )
        return node.children

    def build_table_data(self, spec_table, colnames) -> List[List[nodes.Node]]:
        """
        Generate a representation of the table in a format compatible with the input to ListTable.build_table_from_list.

        This means that all the text elements need to be manually parsed into
        docutils "nodes" which are the intermediate format between rst and html
        (or other output) in docutils.

        The output is a list of rows, each element in a row being a ``Node`` to be rendered in that cell.
        """
        table_rows = [
            [nodes.paragraph(text="Key"), *[nodes.paragraph(text=col) for col in colnames.values()]]
        ]
        for key, info in spec_table.items():
            row = [nodes.literal(text=key)]
            for col in colnames.keys():
                value = info.get(col, "")
                if isinstance(value, list):
                    node = nodes.bullet_list(bullet="*")
                    # Add a css class to this list so we can handle it in the theme
                    node["classes"].append("spec-table-ul")
                    for item in value:
                        li = nodes.list_item()
                        li.append(nodes.paragraph(text=item))
                        node.append(li)
                else:
                    node = nodes.paragraph(text=value)
                row.append(node)
            table_rows.append(row)

        return table_rows

    def get_list_table_extra(self, table_data):
        """
        Generate the keyword arguments for ListTable.build_table_from_list.

        In a method so it can be overriden.
        """
        num_cols = len(table_data[0])
        col_widths = self.get_column_widths(num_cols)
        header_rows = self.options.get("header-rows", 1)
        stub_columns = self.options.get("stub-columns", 0)
        return {
            "col_widths": col_widths,
            "header_rows": header_rows,
            "stub_columns": stub_columns,
        }

    def generate_table_node(self, table_data):
        """
        Convert the table_data format into a ``nodes.table``.
        """
        table_node = self.build_table_from_list(table_data, **self.get_list_table_extra(table_data))

        if "colwidths-given" in table_node:
            table_node["classes"].remove("colwidths-given")
        if "colwidths-auto" not in table_node:
            table_node["classes"] += ["colwidths-auto"]

        return table_node

    def run(self):
        """
        This method is the entry point for the Directive.

        As much as possible is done here by calling other methods so the 214
        and 122 subclasses can override the individual components they need.
        """
        preamble = self.get_preamble()
        preamble_nodes = self.convert_rst_to_nodes(preamble) if preamble else []
        spec_table = self.get_spec_table()
        spec_table = {key: dict(spec) for key, spec in spec_table.items()}
        spec_table = self.prep_table(spec_table)
        table_data = self.build_table_data(spec_table, self.get_colnames(spec_table))
        table_node = self.generate_table_node(table_data)
        return preamble_nodes + [table_node]

    def get_colnames(self, spec_table):
        """
        Get the column names to be displayed.

        By default this is any field for each key in the header.
        Override this method to add custom filtering of the keys.
        """
        all_keys = list(
            set.union(*[set(keys) for keys in [info.keys() for info in spec_table.values()]])
        )
        return dict((zip(all_keys, all_keys)))

    def get_preamble(self):
        """
        Get a rst block which will be placed before the table.
        """
        return ""

    def get_spec_table(self) -> Dict[str, Dict[str, str]]:
        """
        Get the spec_table as defined in `dkist_fits_specifications`.

        The format of the return is a dict with a key matching the FITS header
        key and the value a dict containing all the data about that key.

        Each element of this dict is converted to a row in the table.
        """
        raise NotImplementedError("Subclasses must implement get_spec_table")

    def prep_table(self, spec_table):
        """
        Perform any desired pre-processing on the spec_table before converting it into a table.
        """
        return spec_table


class Spec214Table(BaseSpecTable):
    """
    Generate a spec table from the 214 specs.
    """

    required_arguments = 1

    def get_colnames(self, spec_table):
        key_map = {
            "type": "Type",
            "description": "Description",
            "fitsreference": "Reference to FITS 4.0",
            "units": "Unit",
            "values": "Allowed Values",
        }

        # If a column is empty then don't use it.
        columns = defaultdict(list)
        for key, info in spec_table.items():
            for col, value in info.items():
                columns[col].append(value)
        for col in list(key_map.keys()):
            if all([not v for v in columns[col]]):
                key_map.pop(col)
        return key_map

    def get_spec_table(self):
        spec_table = load_full_spec214(self.arguments[0])
        return spec_table[self.arguments[0]]

    def get_preamble(self):
        spec_header = load_raw_spec214(self.arguments[0])
        spec_header = spec_header[self.arguments[0]][0]["spec214"]
        title = spec_header["title"] + " Keywords"
        header_level = self.options.get("header-level", "#")
        lines = [
            title,
            header_level * len(title),
            "",
            spec_header.get("summary", ""),
            "",
            spec_header.get("long_description", ""),
        ]
        return "\n".join(lines)

    def prep_table(self, spec_table):
        type_lookup = {
            "str": "string",
            "bool": "boolean",
            "int": "integer",
            "float": "float",
        }

        for key, info in spec_table.items():
            if info["units"] is None:
                del info["units"]
            info["type"] = type_lookup[info["type"]]
            if info.get("format"):
                info["format"] = "time" if info["format"] == "isot" else info["format"]
                info["type"] = f'{info["type"]} ({info["format"]})'
        return spec_table


class Spec122Table(BaseSpecTable):
    """
    Generate a spec table from the 122 specs.
    """

    required_arguments = 1

    def get_colnames(self, spec_table):
        return {
            "type": "Type",
            "comment": "FITS Comment",
            "required": "Required by the Data center",
            "expected": "Expected to always be present",
        }

    def get_spec_table(self):
        spec_table = load_spec122(self.arguments[0])
        return spec_table[self.arguments[0]]


class DatasetExtraTable(BaseSpecTable):
    """
    Generate a spec table from the dataset extra specs.
    """

    required_arguments = 1

    def get_colnames(self, spec_table):
        key_map = {
            "type": "Type",
            "description": "Description",
            "units": "Unit",
        }

        # If a column is empty then don't use it.
        columns = defaultdict(list)
        for key, info in spec_table.items():
            for col, value in info.items():
                columns[col].append(value)
        for col in list(key_map.keys()):
            if all([not v for v in columns[col]]):
                key_map.pop(col)
        return key_map

    def get_spec_table(self):
        spec_table = load_full_dataset_extra(self.arguments[0])
        return spec_table[self.arguments[0]]

    def get_preamble(self):
        spec_header = load_raw_dataset_extra(self.arguments[0])
        spec_header = spec_header[self.arguments[0]][0]["dsextra"]
        title = spec_header["title"] + " Keywords"
        header_level = self.options.get("header-level", "#")
        lines = [
            title,
            header_level * len(title),
            "",
            spec_header.get("summary", ""),
            "",
            spec_header.get("long_description", ""),
        ]
        return "\n".join(lines)

    def prep_table(self, spec_table):
        type_lookup = {
            "str": "string",
            "bool": "boolean",
            "int": "integer",
            "float": "float",
        }

        for key, info in spec_table.items():
            if info["units"] is None:
                del info["units"]
            info["type"] = type_lookup[info["type"]]
            if info.get("format"):
                info["format"] = "time" if info["format"] == "isot" else info["format"]
                info["type"] = f'{info["type"]} ({info["format"]})'
        return spec_table


def setup(app):
    app.add_directive("spec-214-table", Spec214Table)
    app.add_directive("spec-122-table", Spec122Table)
    app.add_directive("dataset-extra-table", DatasetExtraTable)

    return {"parallel_read_safe": True, "parallel_write_safe": True}
