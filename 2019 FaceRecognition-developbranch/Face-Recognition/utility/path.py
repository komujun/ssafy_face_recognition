import os

# 디렉토리 경로 반환
def getDirname(dir_str):
    return os.path.realpath(dir_str)