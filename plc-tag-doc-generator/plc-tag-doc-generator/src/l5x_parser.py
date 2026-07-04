"""
l5x_parser.py
---------------
Parses Rockwell Automation / Allen-Bradley L5X export files (the XML
export format produced by Studio 5000 via File > Save As > L5X, or
right-click export on a controller/program) and extracts:

  - Controller-level tags (name, data type, tag type, external access,
    description)
  - User-Defined Types / DataTypes (name, description, members)
  - Programs and their routines (name, type, description)

L5X is plain XML, so this uses only Python's standard library
(xml.etree.ElementTree) - no external dependencies required to parse.

Note: this parser focuses on documentation-relevant fields. It does not
attempt to parse ladder rung logic (RLL content) itself, only routine
metadata (name, type, description).
"""

import xml.etree.ElementTree as ET


class L5XParseError(Exception):
    pass


class ParsedProgram:
    """Holds the results of parsing one L5X file."""

    def __init__(self):
        self.controller_name = ""
        self.software_revision = ""
        self.tags = []       # list of dict: name, data_type, tag_type, access, description
        self.data_types = []  # list of dict: name, description, members(list of dict)
        self.routines = []   # list of dict: program, name, type, description

    def summary_counts(self):
        return {
            "tags": len(self.tags),
            "data_types": len(self.data_types),
            "routines": len(self.routines),
        }


def _text_or_empty(element, path):
    """Fetch a nested element's text (used for <Description><![CDATA[...]]></Description>)."""
    child = element.find(path)
    if child is not None and child.text:
        return child.text.strip()
    return ""


def parse_l5x_file(filepath):
    """
    Parses an L5X file and returns a ParsedProgram instance.
    Raises L5XParseError with a friendly message on malformed XML or
    missing expected structure.
    """
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as exc:
        raise L5XParseError(f"The file is not valid XML: {exc}")

    root = tree.getroot()
    if root.tag != "RSLogix5000Content":
        raise L5XParseError(
            "This does not look like an L5X export "
            "(expected root element <RSLogix5000Content>)."
        )

    controller = root.find("Controller")
    if controller is None:
        raise L5XParseError("No <Controller> element found in this L5X file.")

    result = ParsedProgram()
    result.controller_name = controller.get("Name", "Unknown")
    result.software_revision = root.get("SoftwareRevision", "")

    _parse_data_types(controller, result)
    _parse_tags(controller, result)
    _parse_programs(controller, result)

    return result


def _parse_data_types(controller, result):
    data_types_el = controller.find("DataTypes")
    if data_types_el is None:
        return
    for dt in data_types_el.findall("DataType"):
        members = []
        members_el = dt.find("Members")
        if members_el is not None:
            for member in members_el.findall("Member"):
                # Skip hidden bit/array housekeeping members if present
                if member.get("Hidden") == "true":
                    continue
                members.append({
                    "name": member.get("Name", ""),
                    "data_type": member.get("DataType", ""),
                    "dimension": member.get("Dimension", "0"),
                    "external_access": member.get("ExternalAccess", ""),
                    "description": _text_or_empty(member, "Description"),
                })
        result.data_types.append({
            "name": dt.get("Name", ""),
            "family": dt.get("Family", ""),
            "description": _text_or_empty(dt, "Description"),
            "members": members,
        })


def _parse_tags(controller, result):
    tags_el = controller.find("Tags")
    if tags_el is None:
        return
    for tag in tags_el.findall("Tag"):
        result.tags.append({
            "name": tag.get("Name", ""),
            "tag_type": tag.get("TagType", ""),
            "data_type": tag.get("DataType", ""),
            "external_access": tag.get("ExternalAccess", ""),
            "description": _text_or_empty(tag, "Description"),
        })


def _parse_programs(controller, result):
    programs_el = controller.find("Programs")
    if programs_el is None:
        return
    for program in programs_el.findall("Program"):
        program_name = program.get("Name", "")
        routines_el = program.find("Routines")
        if routines_el is None:
            continue
        for routine in routines_el.findall("Routine"):
            result.routines.append({
                "program": program_name,
                "name": routine.get("Name", ""),
                "type": routine.get("Type", ""),
                "description": _text_or_empty(routine, "Description"),
            })
