from datetime import datetime, timedelta

time_3after = datetime.now() + timedelta(seconds=3)

while True:
    time_now = datetime.now()
    if((datetime.now()-time_3after).seconds>=3):
        time_3after = datetime.now()
    print(((datetime.now()-time_3after)).seconds)