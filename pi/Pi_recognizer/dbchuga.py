import cv2
import numpy as np
import os
import pymysql
import time
from datetime import datetime,timedelta

connection=pymysql.connect(host='i3a207.p.ssafy.io',user='a207',password='a207',db='mydbtest',charset='utf8',autocommit=True)
cursor=connection.cursor()
print("DB access success")
id_user="SELECT blog_usergroup.id,eng_name,enter_at, out_at FROM blog_usergroup INNER JOIN blog_access ON blog_usergroup.ID=blog_access.user_pk_id ORDER BY enter_at ASC"
id__user_access={}
execute_user=cursor.execute(id_user)
for row in cursor:
    id__user_access.update({row[0]:{'name':row[1],'enter_at':row[2],'out_at':row[3]}})
print("Successfully gathered data from DB")
print(id__user_access)
for y in range(5):
    for x in range(1,6):
                nowtime=datetime.now()
                if ((id__user_access[x]["out_at"] is not None) and ((nowtime-id__user_access[x]["out_at"]).seconds>=3)):
                        id__user_access[x].update(enter_at = nowtime)
                        id__user_access[x].update(out_at=None)
                        print("1")
                        cursor.execute("INSERT blog_access SET user_pk_id= %s, enter_at = %s",(x,nowtime))
                elif((id__user_access[x]["out_at"] is None) and (nowtime-id__user_access[x]["enter_at"]).seconds>=3):
                        id__user_access[x].update(out_at = nowtime)
                        cursor.execute("UPDATE blog_access SET out_at = %s WHERE user_pk_id = %s ORDER BY enter_at DESC LIMIT 1",(nowtime,x))
                        print(nowtime)