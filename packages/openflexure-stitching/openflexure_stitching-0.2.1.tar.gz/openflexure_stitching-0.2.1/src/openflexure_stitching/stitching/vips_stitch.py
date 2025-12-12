"""
Produce stitched images using pyVips, which has a lower memory requirement (when
used carefully) than stitching in something like opencv. Can produce a JPEG, DZI
and pyramidal TIFF, based on a folder of "tiles" - small images chopped from the
geometry of the planned huge stitch.
"""

from typing import Optional
import os
import re

import pyvips

# By default, pyvips caches any images it opens in case they're needed again.
# As this file stitches images sequentially, they are not reused, and so
# specify to not cache images.
pyvips.cache_set_max(0)


def produce_stitched_image(
    tile_folder: str,
):
    """Produce a pyvips image from a folder of tiles from that image with locations"""
    matches = [re.match(r"(\d+)_(\d+).jpeg", f) for f in os.listdir(tile_folder)]
    tile_fpaths = [os.path.join(tile_folder, m.group(0)) for m in matches if m]
    positions = [(int(m.group(1)), int(m.group(2))) for m in matches if m]
    stitched_img = pyvips.Image.black(1, 1, bands=3)
    for (y, x), fname in zip(positions, tile_fpaths):
        tile = interleaved_tile(fname)
        stitched_img = stitched_img.insert(tile, x, y, expand=1, background=[0])
    return stitched_img


def convert_tiles_to_jpeg(
    tile_folder: str,
    output_filepath: str,
) -> None:
    """Turn a folder of small images belonging to a huge stitch into the formats
    requested using pyvips

    :param tile_folder: The path of the folder of images
    :param output_filepath: The path of the image to create.
    """
    stitched_img = produce_stitched_image(tile_folder)

    save_jpeg(stitched_img, output_filepath)


def convert_jpeg_to_pyramidal_image(
    jpeg_filepath: str,
    stitch_dzi: bool = True,
    stitch_tiff: bool = False,
    pixel_size_um: Optional[float] = None,
) -> None:
    """Load a JPEG image into vips and export as a Pyramidal TIFF or DZI

    :param jpeg_filepath: The path to the jpeg file.
    :param stitch_dzi: Set to true to create a DZI (Default True)
    :param stitch_tiff: Set to true to create a Pyramidal TIFF (Default False)
    :param pixel_size_um: The side of a pixel in um, set to None if not know.
    """
    if not (stitch_dzi or stitch_tiff):
        # Nothing to do!
        return

    jpeg_path_wo_ext = os.path.splitext(jpeg_filepath)[0]

    stitched_img = pyvips.Image.new_from_file(jpeg_filepath)
    if stitch_dzi:
        stitched_img.dzsave(jpeg_path_wo_ext)
    if stitch_tiff:
        if pixel_size_um is None or pixel_size_um <= 0:
            print("WARNING: no pixel size information. Scale bars will be incorrect.", flush=True)
            pixel_size_um = 1
        tiff_file_path = jpeg_path_wo_ext + ".ome.tiff"
        save_ometiff(stitched_img, tiff_file_path, pixel_size=pixel_size_um)


def interleaved_tile(filepath: str):
    """Load the specified image as a pyvips image to be placed into the tiled image"""

    # Sequential access allows much lower memory requirements, as only the required images
    # are opened and streamed into the final image, from top-to-bottom of the final image

    # Only works for stitching a JPEG, as other formats (DZI, TIFF) have layers, meaning
    # images are read out of order
    tile = pyvips.Image.new_from_file(filepath, access="sequential")
    return tile


def save_ometiff(stitched_img: pyvips.Image, outfile: str, pixel_size: float):
    """Produce an ome pyramidal TIFF file from the stitched_img

    :param stitched_img: a pyvips Image of the stitched image
    :param outfile: a filepath to save the TIFF
    :param pixel_size: the size of one pixel in microns"""
    # collect image dimension needed for OME-XML before separating image planes
    width = stitched_img.width
    height = stitched_img.height
    bands = stitched_img.bands

    # split to separate image planes and stack vertically for OME-TIFF
    stitched_img = pyvips.Image.arrayjoin(stitched_img.bandsplit(), across=1)
    res = 10**3 / pixel_size
    pixel_size /= 10**3
    # Set tiff tags necessary for OME-TIFF
    stitched_img = stitched_img.copy(xres=res, yres=res)

    # build minimal OME metadata. TODO: get calibration and channel names
    stitched_img.set_type(
        pyvips.GValue.gstr_type,
        "image-description",
        f"""<?xml version="1.0" encoding="UTF-8"?>
    <OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.openmicroscopy.org/Schemas/OME/2016-06 http://www.openmicroscopy.org/Schemas/OME/2016-06/ome.xsd">
        <Image ID="Image:0">
            <!-- Minimum required fields about image dimensions -->
            <Pixels DimensionOrder="XYCZT"
                    ID="Pixels:0"
                    PhysicalSizeX= "{pixel_size}"
                    PhysicalSizeY= "{pixel_size}"
                    PhysicalSizeXUnit= "mm"
                    PhysicalSizeYUnit= "mm"
                    SizeC="{bands}"
                    SizeT="1"
                    SizeX="{width}"
                    SizeY="{height}"
                    SizeZ="1"
                    Type="float">
            </Pixels>
        </Image>
    </OME>""",
    )

    stitched_img.set_type(pyvips.GValue.gint_type, "page-height", height)
    stitched_img.write_to_file(
        outfile,
        compression="jpeg",
        Q=95,
        tile=True,
        tile_width=512,
        tile_height=512,
        pyramid=True,
        subifd=False,
        bigtiff=True,
    )


def save_jpeg(stitched_img: pyvips.Image, outfile: str):
    """Produce a large area JPEG file from the stitched_img

    :param stitched_img: a pyvips Image of the stitched image, which should be
    generated with `access="sequential"` for memory efficiency
    :param outfile: a filepath to save the JPEG
    """

    stitched_img.write_to_file(
        outfile,
        Q=95,
    )
