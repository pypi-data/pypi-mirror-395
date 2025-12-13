# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2024  CEA, EDF
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

__version__ = "cf9dcce-dirty"

# ==========================================================================
# the wheel should not require any environment variables to be set

# set YACS_ROOT_DIR to the root dir of the salome.yacs module, where we copied the /share directory
os.environ.setdefault("YACS_ROOT_DIR", os.path.dirname(os.path.dirname(__file__)))

# same for PATH, we copied the /bin directory to the root dir of salome.yacs
os.environ["PATH"] += ":" + os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin", "salome")
