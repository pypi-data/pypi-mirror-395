from uuid import UUID

import aecg
import aecg.parser


def test_read_example_file():
    file_path = r"tests/data/Example aECG.xml"
    aecg_o = aecg.parser.read(file_path)

    assert aecg_o.id == UUID("61d1a24f-b47e-41aa-ae95-f8ac302f4eeb")
