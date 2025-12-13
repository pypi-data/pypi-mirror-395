import streamlit.components.v1 as components
from solidipes.viewers import backends as viewer_backends
from solidipes.viewers.viewer import Viewer


class AstroVisJs(Viewer):
    """Viewer for table and binary table HDU from FITS file"""

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
<script type="text/javascript"
        src="https://unpkg.com/astrovisjs@latest/dist/astrovis/astrovis.js"
        charset="utf-8"></script>
<div id="astrovisdiv">
</div>
<script type="text/javascript">

    const base64Content = "{self.fits_data}";
    const mimeType = "image/fits";

    const binaryString = atob(base64Content);

    const byteArray = Uint8Array.from(binaryString, char => char.charCodeAt(0));

    const blob = new Blob([byteArray], {{ type: mimeType }});

    const blobUrl = URL.createObjectURL(blob);

    /*
    fetch(URL.createObjectURL(blob))
        .then(response => response.blob())
        .then(fileBlob => {{
            const file = new File([fileBlob], "file.fits", {{ type: mimeType }});
            Astrovis.init('astrovisdiv', file);
        }})
        .catch(error => console.error("Error loading file:", error));
    */

    const dataUrl = `data:${{mimeType}};base64,${{base64Content}}`;

    document.addEventListener('DOMContentLoaded', () => {{
        Astrovis.init('astrovisdiv', blobUrl);
    }});
</script>""",
                height=9000,
            )

        else:
            pass
