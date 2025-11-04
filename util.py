from time import sleep


def red_text(str2bRed) -> str:
    return f"\033[31m{str2bRed}\033[0m"

def sleepprint(string: str = '\n',
               wait_time = 0.8) -> None:
    
    sleep(wait_time)
    print(string)



if __name__ == '__main__':
    import os
    print(f"\n\nSuccessfully ran {os.path.basename(__file__)}")