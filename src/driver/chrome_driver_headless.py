#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 namah <namah@namah>
#
# Distributed under terms of the MIT license.

"""
Description: To create a headless chrome browser
Author: NamahRecoSense
"""
# built-in imports
from selenium.webdriver.chrome.options import Options

# app imports
from .base_driver import BaseWebDriver
from . import driver_constants


# Driver Class
class SeleniumWebDriver(BaseWebDriver):

    def __init__(self):
        options = self.getOptions()
        super().__init__(
            driver_constants.CHROME_DRIVER_PATH,
            options,
            driver_constants.CHROME_DRIVER
        )

    def getOptions(self):
        options = Options()
        options.add_argument('--headless')
        return options