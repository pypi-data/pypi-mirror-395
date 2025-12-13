import base64

from solidipes.loaders.file import File

from ..viewers.aladin_lite import AladinLite as AladinLiteViewer
from ..viewers.astrovisjs import AstroVisJs as AstroVisJsViewer


class FITS(File):
    """FITS file for astronomical data"""

    supported_mime_types = {"image/fits": "fits"}
    _compatible_viewers = [AladinLiteViewer, AstroVisJsViewer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [AladinLiteViewer, AstroVisJsViewer]

    @File.loadable
    def fits_data(self):
        try:
            with open(self.file_info.path, "rb") as file:
                file_content = file.read()
                base64_encoded = base64.b64encode(file_content)
        except Exception as e:
            print(f"Error: {e}")
            return None

        return base64_encoded.decode("utf-8")
