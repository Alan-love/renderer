"""Preprocess the Damaged Helmet model

The model is available for download from
    https://github.com/KhronosGroup/glTF-Sample-Models/archive/master.zip

The Python Imaging Library is required
    pip install pillow
"""

from __future__ import print_function

import json
import os
import zipfile
from PIL import Image
import utils

SRC_FILENAME = "glTF-Sample-Models-master.zip"
DST_DIRECTORY = "../assets/helmet"
OBJ_FILENAME = "helmet.obj"

INPUT_DIR = "glTF-Sample-Models-master/2.0/DamagedHelmet/glTF/"
GLTF_FILEPATH = INPUT_DIR + "DamagedHelmet.gltf"
BUFFER_FILEPATH = INPUT_DIR + "DamagedHelmet.bin"
BASECOLOR_FILEPATH = INPUT_DIR + "Default_albedo.jpg"
PACKED_FILEPATH = INPUT_DIR + "Default_metalRoughness.jpg"
OCCLUSION_FILEPATH = INPUT_DIR + "Default_AO.jpg"
EMISSIVE_FILEPATH = INPUT_DIR + "Default_emissive.jpg"


def process_mesh(zip_file):
    gltf = json.loads(zip_file.read(GLTF_FILEPATH))
    buffer = zip_file.read(BUFFER_FILEPATH)

    mesh = utils.load_gltf_mesh(gltf, buffer, gltf["meshes"][0])
    obj_data, _ = utils.dump_mesh_data(mesh)
    filepath = os.path.join(DST_DIRECTORY, OBJ_FILENAME)
    with open(filepath, "w") as f:
        f.write(obj_data)


def load_rgb_image(zip_file, filename):
    with zip_file.open(filename) as f:
        image = Image.open(f)
        bands = image.split()
        image = Image.merge("RGB", bands[:3])
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image = image.resize((512, 512), Image.LANCZOS)
        return image


def process_images(zip_file):
    basecolor_image = load_rgb_image(zip_file, BASECOLOR_FILEPATH)
    basecolor_filepath = os.path.join(DST_DIRECTORY, "basecolor.tga")
    basecolor_image.save(basecolor_filepath, rle=True)

    packed_image = load_rgb_image(zip_file, PACKED_FILEPATH)
    _, roughness_image, metallic_image = packed_image.split()
    metallic_filepath = os.path.join(DST_DIRECTORY, "metallic.tga")
    metallic_image.save(metallic_filepath, rle=True)
    roughness_filepath = os.path.join(DST_DIRECTORY, "roughness.tga")
    roughness_image.save(roughness_filepath, rle=True)

    occlusion_image = load_rgb_image(zip_file, OCCLUSION_FILEPATH)
    occlusion_image, _, _ = occlusion_image.split()
    occlusion_filepath = os.path.join(DST_DIRECTORY, "occlusion.tga")
    occlusion_image.save(occlusion_filepath, rle=True)

    emissive_image = load_rgb_image(zip_file, EMISSIVE_FILEPATH)
    emissive_filepath = os.path.join(DST_DIRECTORY, "emissive.tga")
    emissive_image.save(emissive_filepath, rle=True)


def main():
    if not os.path.exists(DST_DIRECTORY):
        os.makedirs(DST_DIRECTORY)

    with zipfile.ZipFile(SRC_FILENAME) as zip_file:
        process_mesh(zip_file)
        process_images(zip_file)


if __name__ == "__main__":
    main()
