from pathlib import Path
from typing import List
from pyconverters_pypowerpoint.pypowerpoint import PyPowerPointConverter, PyPowerPointParameters
from pymultirole_plugins.v1.schema import Document, DocumentList
from starlette.datastructures import UploadFile


def test_pypowerpoint():
    testdir = Path(__file__).parent
    converter = PyPowerPointConverter()
    parameters = PyPowerPointParameters(one_segment_per_powerpoint_page=True)
    source = Path(testdir, 'data/CaaS---Onboarding-document.pptx')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'application/octet-stream'), parameters)
        assert len(docs) == 1
        assert docs[0].identifier
        assert docs[0].text
    json_file = source.with_suffix(".md1.json")
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)

    parameters = PyPowerPointParameters(one_segment_per_powerpoint_page=True, include_image_base64_as_altTexts=True)
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'application/octet-stream'), parameters)
        assert len(docs) == 1
        assert docs[0].identifier
        assert docs[0].text
    json_file = source.with_suffix(".md2.json")
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
