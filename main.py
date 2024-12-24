
from listen.wakeup import run
# from listen.asr import start_listen_stream

def react():
    print("Wake up")
    # start_listen_stream()


if __name__ == '__main__':
    run(target=react)