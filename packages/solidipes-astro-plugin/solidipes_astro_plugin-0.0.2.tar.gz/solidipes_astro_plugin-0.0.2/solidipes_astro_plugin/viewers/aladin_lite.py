import streamlit.components.v1 as components
from solidipes.viewers import backends as viewer_backends
from solidipes.viewers.viewer import Viewer


class AladinLite(Viewer):
    """Viewer for image HDU from FITS file"""

    def __init__(self, data=None):
        super().__init__(data)

    def add(self, data_container):
        self.fits_data = data_container.fits_data

    def show(self):
        if viewer_backends.current_backend == "jupyter notebook":
            pass

        elif viewer_backends.current_backend == "streamlit":
            components.html(
                f"""
<div id="aladin-lite-div" style="width:100%;height:400px;"></div>
<script type="text/javascript" src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js"
                charset="utf-8"></script>
<script type="text/javascript">

    let aladin;
    let fileUrl = '';

    initializeAladinLite();

    function initializeAladinLite() {{

        const base64Content = "{self.fits_data}";
        const mimeType = "image/fits";

        const binaryString = atob(base64Content);

        const byteArray = Uint8Array.from(binaryString, char => char.charCodeAt(0));

        const blob = new Blob([byteArray], {{ type: mimeType }});

        const blobUrl = URL.createObjectURL(blob);

        A.init.then(() => {{
            aladin = A.aladin('#aladin-lite-div', {{showCooGridControl: true}});
            aladin.displayFITS(blobUrl)
            aladin.showCooGrid(true);
        }});
    }}
</script>""",
                height=600,
            )

        else:
            pass
