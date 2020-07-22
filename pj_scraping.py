# -*- coding: utf-8 -*-

import pj_scraper as pj
import pandas as pd

pd.set_option('display.max_columns', None)

# =============================================================================
driver_path = "/usr/local/bin/chromedriver"
contact_list = pj.get_company_contacts(False, driver_path, 15)

df_contact = pd.DataFrame(contact_list)

df_contact
# =============================================================================

