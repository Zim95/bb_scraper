#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 namah <namah@namah>
#
# Distributed under terms of the MIT license.

"""
Description: Constants for web drivers
Author: NamahRecoSense
"""

import os


DRIVER_BASE_PATH = '{}/driver/drivers/'.format(
        os.path.abspath('.')
    )

CHROME_DRIVER = 'chrome'
CHROME_DRIVER_PATH = r'{}/chromedriver'.format(
            DRIVER_BASE_PATH
        )

GECKO_DRIVER = 'firefox'
GECKO_DRIVER_PATH = r'{}/geckodriver'.format(
            DRIVER_BASE_PATH
        )


