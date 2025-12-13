# Copyright (C) 2025  CEA, EDF
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

"""
Templated script to provide set of environment variables for SALOME:
- A positioning of the PYTHONPATH on lib/pythonX.Y/site-packages
- A positioning of the PATH on bin/salome
- A positioning of APPLI on bin/salome/appli/salome
- Clear LD_LIBRARY_PATH
"""

from pathlib import Path
import site

def init(context, root_dir):
    # To launch the tests
    # 
    p = Path(__file__).parents[2].absolute()
    context.addToPythonPath( f'{p.parents[1] / "bin" / "salome"}' )
    context.addToPath(f"{p}")
    context.addToLdLibraryPath(f'{p.parents[2] / "salome.kernel.libs"}')
    context.addToLdLibraryPath(f'{p.parents[2] / "salome.yacs.libs"}')
    context.setVariable(r"APPLI", f'{p.parents[1] / "bin" / "salome" / "appli" / "salome"}')
    # To prevent the tests failure
    for path in site.getsitepackages():
        context.addToPythonPath(path)
