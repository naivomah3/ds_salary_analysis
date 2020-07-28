import gd_scrap_engine as gs
import pandas as pd


# =============================================================================
driver_path = "/usr/local/bin/chromedriver"
df = gs.get_jobs('data scientist', 'Canada', 10, False, driver_path, 15)
# =============================================================================

df