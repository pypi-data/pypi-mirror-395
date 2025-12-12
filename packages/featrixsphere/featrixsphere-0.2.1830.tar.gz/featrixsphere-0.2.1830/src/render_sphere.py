#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

# Render our ES projections to a PNG for previews, etc.
import os
import json

from PIL import Image, ImageDraw
import math

# Parameters
width, height = 300, 300
background_color = (255, 255, 255)
point_radius = 2

# Define camera settings
camera = {
    "position": {"x": 0, "y": 0, "z": 3},
    "fov": 60,
    "aspect": width / height,
    "near": 0.1,
    "far": 1000
}

# Define the color palette
kColorTable = [
    0xe6194b, 0x3cb44b, 0xffe119, 0x4363d8, 0xf58231, 0x911eb4, 0x46f0f0,
    0xf032e6, 0xbcf60c, 0xfabebe, 0x008080, 0xe6beff, 0x9a6324, 0xfffac8,
    0x800000, 0xaaffc3, 0x808000, 0xffd8b1, 0x999999, 0x0000ff, 0x00ff00,
    0xffcccc
]

# Convert hex color to (R, G, B)
def uint32_to_rgb(hex_value):
    return ((hex_value >> 16) & 255, (hex_value >> 8) & 255, hex_value & 255)

# Perspective projection function
def project_point(point, camera):
    # x, y, z = point[0], point[1], point[2]
    x, y, z = point["0"], point["1"], point["2"]
    position = camera["position"]

    # Translate points based on camera position
    translated = {
        "x": x - position["x"],
        "y": y - position["y"],
        "z": z - position["z"]
    }

    # Simple perspective projection
    f = 1 / math.tan((camera["fov"] / 2) * (math.pi / 180))  # Perspective factor

    if translated["z"] == 0:
        return None  # Avoid division by zero

    sx = (translated["x"] * f) / translated["z"] * camera["aspect"]
    sy = (translated["y"] * f) / translated["z"]

    # Convert to screen coordinates
    return {
        "x": int((width / 2) + sx * (width / 2)),
        "y": int((height / 2) - sy * (height / 2))  # Flip y-axis for correct rendering
    }

# Function to get color based on cluster
def get_color(pt, pt_index, colorTableInput=None):
    if "cluster_pre" in pt:
        idx = pt["cluster_pre"]
        if idx < len(kColorTable):
            return uint32_to_rgb(kColorTable[idx])
        return (255, 0, 0)  # Default red
    elif colorTableInput is not None:
        return uint32_to_rgb(colorTableInput[pt_index])
    return (255, 0, 0)  # Default red



def write_preview_image(path_to_projections_json, path_to_png_file):
    if not os.path.exists(path_to_projections_json):
        raise FileNotFoundError()

    with open(path_to_projections_json, "r") as fp:
        js = json.load(fp)
    
    points = js['coords']

    # Create an image buffer
    img = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Draw projected points
    for i, point in enumerate(points):
        projected = project_point(point, camera)
        if projected:
            color = get_color(point, i)
            draw.ellipse(
                (projected["x"] - point_radius, projected["y"] - point_radius,
                projected["x"] + point_radius, projected["y"] + point_radius),
                fill=color, outline=color
            )

    # Save the image
    img.save(path_to_png_file) #"sphere_projection.png")
    print(f"Image saved as {path_to_png_file}")
    return
