import sys

if __name__ == "__main__":
    if len(sys.argv) - 1:
        if(sys.argv[1] == '-d' or sys.argv[1] == '--download'):
            print('다운로드 시작')
        else:
            print('명령 인자를 바르게 입력해주세요')

    else:
        print('명령 인자를 바르게 입력해주세요')