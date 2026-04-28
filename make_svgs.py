"""Make SVGs of the solutions."""

import json
from a_paper import a
import os

if not os.path.isdir("output"):
    os.system("mkdir output")
if not os.path.isdir("output/json"):
    raise RuntimeError("Please generate json solutions first by running `python a_solver_simpler.py`")
if not os.path.isdir("output/svg"):
    os.system("mkdir output/svg")

scale = 5

large_color = "#999999"
small_color = "#FFFFFF"


for file in os.listdir("output/json"):
    if file.endswith(".json"):
        with open(f"output/json/{file}") as f:
            rectangles = json.load(f)
        fname = file[:-5]
        print(fname)

        large = int(fname.split("-")[0][1:])
        size = a[large]
        padding = max(2, max(size) // 20)
        line_width = max(1, max(size) // 300 * scale)

        svg = f'<svg version="1.1" viewBox="{-padding*scale} {-padding*scale} {(size[1] + 2*padding)*scale} {(size[0] + 2*padding)*scale}" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">\n'
        svg += f'<rect x="0" y="0" width="{size[1]*scale}" height="{size[0]*scale}" style="fill:{large_color};stroke:#000000;stroke-width:{line_width};stroke-linecap:round;stroke-linejoin:round" />\n'

        for (x0, y0), (x1, y1) in rectangles:
            svg += f'<rect x="{x0*scale}" y="{y0*scale}" width="{(x1-x0)*scale}" height="{(y1-y0)*scale}" style="fill:{small_color};stroke:#000000;stroke-width:{line_width};stroke-linecap:round;stroke-linejoin:round" />\n'

        svg += "</svg>\n"

        with open(f"output/svg/{fname}.svg", "w") as f:
            f.write(svg)
