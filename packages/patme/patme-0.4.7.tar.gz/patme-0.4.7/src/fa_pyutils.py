# Copyright (C) 2020 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                             patme                          #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
Top-level compatibility interface for former fa-pyutils as a standalone python package.

@note: patme
Created on 19.11.2024

@version: 1.0
----------------------------------------------------------------------------------------------
@requires:
       -

@change:
       -

@author: garb_ma                                                     [DLR-SY,STM Braunschweig]
----------------------------------------------------------------------------------------------
"""

## @package patme
# Top-level compatibility interface for patme defining a new alias as a python package.
## @authors
# Marc Garbade
## @date
# 19.11.2024

import os
import pkgutil
import sys

# List of all attributes and modules available during wild import
__all__ = []

# Create a valid package name
__package__ = os.path.splitext(os.path.basename(__file__))[0]

# Import deprecated module. Create an alias.
import patme

sys.modules[__package__] = patme

# Create a valid path identifier
__path__ = [__file__]

## Iterate through all modules at runtime
# Source: https://stackoverflow.com/questions/3365740/how-to-import-all-submodules
for loader, module_name, is_pkg in pkgutil.walk_packages(patme.__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module

if __name__ == "__main__":
    sys.exit()
    pass
