import logging
from typing import List, cast, Type

from pptx import Presentation
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile
from tempfile import SpooledTemporaryFile
from pyconverters_pypowerpoint.pptx2md.outputter import MarkdownFormatter
from pyconverters_pypowerpoint.pptx2md.parser import parse
from pyconverters_pypowerpoint.pptx2md.types import ConversionConfig

logger = logging.getLogger("pymultirole")


class PyPowerPointParameters(ConverterParameters):
    one_segment_per_powerpoint_page: bool = Field(False, description="""Create one segment per PowerPoint page""")
    include_image_base64_as_links: bool = Field(
        False, extra="advanced",
        description="""To include the image data as base64 links `![img-0.jpeg](data:image/jpeg;base64,`"""
    )
    include_image_base64_as_altTexts: bool = Field(
        False, extra="advanced",
        description="""To include the image data as base64 altTexts"""
    )


class PyPowerPointConverter(ConverterBase):
    """Convert PPTX to Markdown using [python-pptx](https://github.com/scanny/python-pptx)
    """

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: PyPowerPointParameters = \
            cast(PyPowerPointParameters, parameters)
        doc: Document = None
        try:
            input_file = source.file._file if isinstance(source.file, SpooledTemporaryFile) else source.file
            prs = Presentation(input_file)
            config = ConversionConfig(disable_image=not(params.include_image_base64_as_links or params.include_image_base64_as_altTexts), enable_slides=params.one_segment_per_powerpoint_page)
            ast = parse(config, prs)
            out = MarkdownFormatter(config, params.include_image_base64_as_links, params.include_image_base64_as_altTexts)
            doc = out.output(ast, identifier=source.filename)
        except BaseException:
            logger.warning(
                f"Cannot convert PDF from file {source.filename}: ignoring",
                exc_info=True,
            )
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return PyPowerPointParameters
