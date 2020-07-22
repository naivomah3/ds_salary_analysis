#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 00:01:04 2020

@author: zero
"""

import gd_scraper as gs
import pandas as pd


# =============================================================================
driver_path = "/usr/local/bin/chromedriver"
df = gs.get_jobs('data scientist', 'Canada', 10, False, driver_path, 15)
# =============================================================================


df