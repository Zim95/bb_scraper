#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 namah <namah@namah>
#
# Distributed under terms of the MIT license.

"""
Description: Main Task Runner
Author: NamahRecoSense
"""

# app imports
from driver import firefox_driver_headless


def main():
    driver = firefox_driver_headless.SeleniumWebDriver()
    driver.driver.get("https://google.com/")
    print("Headless Firefox Initialized")
    driver.driver.quit()


if __name__ == "__main__":
    main()