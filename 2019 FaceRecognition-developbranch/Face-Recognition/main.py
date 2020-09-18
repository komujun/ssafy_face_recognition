import sys
import time
from picture_menu import local_main, reset, web_main

if __name__ == "__main__":
    if len(sys.argv) - 1:
        # 경로 /image 에 이미지 파일을 집어넣고, 데이터를 늘리고 싶을 때 [초기 설정시, 2번 실행]
        if(sys.argv[1] == '-d' or sys.argv[1] == '--download'):
            try:
                local_main.local_play()
            except:
                pass

        # 모든 pickle, web 초기화를 시키고 싶을 때
        elif(sys.argv[1] == '-r' or sys.argv[1] == '--reset'):
            reset.init()
            reset.remove_file()

        # 웹 페이지에서 사진을 다운받아 저장하고 싶을 때
        elif(sys.argv[1] == '-w' or sys.argv[1] == '--web'):
            while(True):
                try:
                    web_main.web_play()
                except:
                    pass
                time.sleep(5)
                
        else:
            print('명령 인자를 바르게 입력해주세요')

    else:
        print('명령 인자를 바르게 입력해주세요')