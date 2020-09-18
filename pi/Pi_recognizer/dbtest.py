import pymysql
from datetime import datetime, timedelta
import time
connection=pymysql.connect(host='i3a207.p.ssafy.io',user='a207',password='a207',db='mydbtest',charset='utf8',autocommit=True)
cursor=connection.cursor()
id_user="SELECT blog_usergroup.id,eng_name,enter_at, out_at FROM blog_usergroup INNER JOIN blog_access ON blog_usergroup.ID=blog_access.user_pk_id ORDER BY enter_at ASC"
id__user_access={}
execute_user=cursor.execute(id_user)
for row in cursor:
    id__user_access.update({row[0]:{'name':row[1],'enter_at':row[2],'out_at':row[3]}})
print(id__user_access)
while True:
    time.sleep(2)
    nowtime=datetime.now()
    if id__user_access[1]["out_at"] is not None:
            id__user_access[1].update(enter_at = nowtime)
            id__user_access[1].update(out_at=None)
            cursor.execute("INSERT blog_access SET user_pk_id= %s, enter_at = %s",(1,nowtime))
    elif((nowtime-id__user_access[1]["enter_at"]).seconds>=3):
            id__user_access[1].update(out_at = nowtime)
            cursor.execute("UPDATE blog_access SET out_at = %s WHERE user_pk_id = %s AND (TIME_TO_SEC(TIMEDIFF(%s,blog_access.enter_at)) > 1)",(nowtime,id,id__user_access[1]["enter_at"]))
            print("updated")
