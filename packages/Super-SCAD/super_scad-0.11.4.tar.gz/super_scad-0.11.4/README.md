# SuperSCAD

<table>
<thead>
<tr>
<th>Legal</th>
<th>Docs</th>
<th>Release</th>
<th>Code</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<a href="https://pypi.org/project/Super-SCAD/" target="_blank"><img alt="PyPI - License" src="https://img.shields.io/pypi/l/Super-SCAD"></a>
</td>
<td>
<a href='https://superscad.readthedocs.io/en/latest/?badge=latest'> <img src='https://readthedocs.org/projects/superscad/badge/?version=latest' alt='Documentation Status'/></a>
</td>
<td>
<a href="https://badge.fury.io/py/Super-SCAD" target="_blank"><img src="https://badge.fury.io/py/Super-SCAD.svg" alt="Latest Stable Version"/></a><br/>
</td>
<td>
<a href="https://codecov.io/gh/SuperSCAD/SuperSCAD" target="_blank"><img src="https://codecov.io/gh/SuperSCAD/SuperSCAD/graph/badge.svg?token=7D8V8RRY11" alt="Code Coverage"/></a>
<a href="https://github.com/SuperSCAD/SuperSCAD/actions/workflows/unit.yml"><img src="https://github.com/SuperSCAD/SuperSCAD/actions/workflows/unit.yml/badge.svg" alt="unit Tests"/></a>
</td>
</tr>
</tbody>
</table>

## The OO Programmers Solid 3D CAD Modeller

SuperSCAD is an advanced application/library for generating 2D and 3D models in [OpenSCAD](https://openscad.org) in
Python. SuperSCAD is based, among others, on the factory pattern and delivers to you as 2D and 3D modeler the
superpowers of Python.

## Documentation

The full documentation is available at https://superscad.readthedocs.io.

## Getting Started and Installing SuperSCAD

We advise to create a Python virtual environment in a project folder:

```shell
cd awsesome-project

python -m venv .venv
. .venv/bin/activate
pip install super-scad
```

Using your favorite editor, copy-paste the code from the demo in the next section and save the file under
`openscad-logo.py`.

```shell
vi openscad-logo.py  
```

Run python and open the generated `openscad-logo.scad` in openscad.

```shell
python openscad-logo.py
openscad openscad-logo.scad
```

Congratulations, you just finished your first SuperSCAD project.

## Demo

Below is an example of SuperSCAD utilizing the factory pattern.

```python3
from super_scad.boolean.Difference import Difference
from super_scad.d3.Cylinder import Cylinder
from super_scad.d3.Sphere import Sphere
from super_scad.other.Modify import Modify
from super_scad.scad.Context import Context
from super_scad.scad.Scad import Scad
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.scad.Unit import Unit
from super_scad.transformation.Rotate3D import Rotate3D


class Logo(ScadWidget):
    """
    SuperSCAD widget for generating OpenSCAD logo.
    """

    def build(self, context: Context):
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        size: float = 50.0
        hole: float = size / 2.0
        height: float = 1.25 * size

        cylinder = Cylinder(height=height, diameter=hole, center=True, fn4n=True)
        sphere = Sphere(diameter=size, fn4n=True)

        return Difference(children=[sphere,
                                    cylinder,
                                    Modify(highlight=True, child=Rotate3D(angle_x=90.0, child=cylinder)),
                                    Rotate3D(angle_y=90.0, child=cylinder)])


if __name__ == '__main__':
    scad = Scad(context=Context(fn=360))
    logo = Logo()
    scad.run_super_scad(logo, 'logo.scad')
```

The example generates the logo of OpenSCAD.

![OpenSCAD Logo](openscad-logo.png)

# Links

* [OpenSCAD SheetSheet](https://openscad.org/cheatsheet/index.html)

# License

This project is licensed under the terms of the [MIT license](LICENSE).
