import io

from benedict import benedict
from lxml import etree

from aecg.models import AnnotatedECG


def _remove_namespace(root: etree._Element) -> etree._Element:
    # Iterate through all XML elements.
    for elem in root.getiterator():
        # Skip comments and processing instructions,
        # because they do not have names.
        if not (
            isinstance(elem, etree._Comment)
            or isinstance(elem, etree._ProcessingInstruction)
        ):
            # Remove a namespace URI in the element's name.
            elem.tag = etree.QName(elem).localname

    # Remove unused namespace declarations.
    etree.cleanup_namespaces(root)


def read(file) -> AnnotatedECG:
    """
    Read XML HL7 aECG file.
    """
    tree = etree.parse(file)
    root = tree.getroot()

    # Observed aECG files can have different namespaces
    # ("urn:hl7-org:v1", "urn:hl7-org:v2", "urn:hl7-org:v3", etc.)
    # and sometimes none at all.
    # Here, we ignore any namespace and parse them indifferently.
    _remove_namespace(root)

    aecg_o = AnnotatedECG.from_xml_tree(root)

    if isinstance(file, str):
        aecg_o._raw = benedict(file, format="xml")
    elif isinstance(file, io.IOBase):
        aecg_o._raw = benedict(file.getvalue().decode("utf-8"), format="xml")
    else:
        aecg_o._raw = benedict(file.decode("utf-8"), format="xml")

    aecg_o._root = root

    return aecg_o
