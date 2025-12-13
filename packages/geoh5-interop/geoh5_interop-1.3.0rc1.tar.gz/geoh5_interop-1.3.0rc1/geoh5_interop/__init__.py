# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Copyright (c) 2024-2025 Mira Geoscience Ltd.                                   '
#                                                                                 '
#  This file is part of geoh5-interop meta-package.                               '
#                                                                                 '
#  geoh5-interop is distributed under the terms and conditions of the MIT License '
#  (see LICENSE file at the root of this source code package).                    '
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from __future__ import annotations


try:
    from ._version import __version__
except ModuleNotFoundError:
    from datetime import datetime

    __date_str = datetime.today().strftime("%Y%m%d")
    __version__ = "0.0.0.dev0+" + __date_str
