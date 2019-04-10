#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 namah <namah@namah>
#
# Distributed under terms of the MIT license.

"""
Description: Base Web Driver
Author: NamahRecoSense
"""
# built-in imports

# to use selenium
from selenium import webdriver
# to go headless with chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# app imports
from . import driver_constants


# Base Web Driver Class
class BaseWebDriver:

    def __init__(self, driver_path, options, driver_type):
        self.driver_path = driver_path
        self.options = options
        self.driver = self.createDriver(driver_type)

    def createDriver(self, driver_type):
        if driver_type == driver_constants.CHROME_DRIVER:
            return webdriver.Chrome(
                executable_path=self.driver_path, chrome_options=self.options)
        elif driver_type == driver_constants.GECKO_DRIVER:
            return webdriver.Firefox(
                executable_path=self.driver_path, options=self.options)
