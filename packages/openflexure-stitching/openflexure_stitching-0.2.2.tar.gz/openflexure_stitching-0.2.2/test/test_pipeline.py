import os
from openflexure_stitching.pipeline import choose_final_filename_prefix


def test_final_filename_prefix():
    """Test the examples copied from the docstring, and an extra one to check
    it works if you are running it from the directory you are in."""

    # Change working dir so we know the name of the current directory for relative
    # test/
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
    os.chdir(THIS_DIR)
    examples = [
        {
            "images_folder": "/home/name/files/scans/my_pretty_scan/",
            "output_image": "my_pretty_scan_stitched.jpg",
        },
        {
            "images_folder": "/home/name/files/scans/my_scan/images",
            "output_image": "my_scan_stitched.jpg",
        },
        {
            "images_folder": "/home/name/files/scans/another_scan/use/images",
            "output_image": "another_scan_stitched.jpg",
        },
        {
            "images_folder": "/images/use/images/use/use/use/images/use/images/",
            "output_image": "scan_stitched.jpg",
        },
        {
            "images_folder": ".",
            "output_image": "test_stitched.jpg",
        },
    ]
    for example in examples:
        prefix = choose_final_filename_prefix(example["images_folder"])
        assert prefix + "_stitched.jpg" == example["output_image"]
