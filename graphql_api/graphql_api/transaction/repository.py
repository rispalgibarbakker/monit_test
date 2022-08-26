from datetime import datetime
from dateutil.relativedelta import relativedelta

class transform():
  def transform_type(self, presetRange):
        types = {"years":1000}
        if presetRange == "LAST_7_DAYS":
            types = {"days":7}
        elif presetRange == "LAST_7_MONTHS":
            types = {"months":7}
        elif presetRange == "LAST_7_WEEK":
            types = {"weeks":7}
        filter_date = datetime.now()-relativedelta(**types)
        return filter_date.strftime("%Y-%m-%d")