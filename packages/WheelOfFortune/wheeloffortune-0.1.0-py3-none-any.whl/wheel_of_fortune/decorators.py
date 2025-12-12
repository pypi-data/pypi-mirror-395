import time
from datetime import datetime
from functools import wraps

def timer(f):
    @wraps(f)
    def wrapper(*args):
        try:
            t0 = time.time()
            res = f(*args)
        except Exception as e:
            print("AAAAAAAAAAAAAAAA", e)
            pass
        finally:
            dt = int(time.time() - t0)
            print(f"Время выполнения: {dt//60} мин {dt%60} сек")
        return
    return wrapper

def log_error(f):
    @wraps(f)
    def wrapper(*args):
        d = '/'.join(__file__.split('\\')[:-1])
        with open(d + "/data/game.log", 'a', encoding='utf-8') as log:
            if f.__name__ == "game":
                log.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} новая игра\n')
            while 1:
                try:
                    now = datetime.now()
                    now = now.strftime("%Y-%m-%d %H:%M:%S") 
                    res = f(*args)
                    break
                except ValueError as e:
                    log.write(f'{now} {e}\n')
                    print("попробуйте снова:\n")
                except StopIteration as e:
                    log.write(f'{now} победа\n')
                    return res
                except Exception as e:
                    if str(e) == "!":
                        log.write("Игра завершена досрочно\n")
                        exit(0)
                    break
        if f.__name__ == "game":
            return res
        return False
    return wrapper

