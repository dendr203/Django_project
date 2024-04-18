# import packages
from datetime import date
from dateutil.relativedelta import relativedelta

# adding months to a particular date
today = date.today()
print('date : ' + str(today))
new_date = today + relativedelta(months=1)
print('new date is : ' + str(new_date))