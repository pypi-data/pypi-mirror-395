from typing import Literal
import datetime

def log(
    tp: Literal["INF", "WRN", "ERR"],
    msg: str, level: Literal[0, 1, 2, 3] = 0,
    print_time: bool = False
) -> str:
    """Prints simple message error with level log

    Print simple message error with level log and future we can print
    on file.

    Args:
            tp (str): Type of message can be INF, WRN or ERR. Error not raise
                    exception.
            msg (str): Message of log.
            level (int, optional): Log level can be 0 or 3.
                    If level == 1 will print message error.
                    If level == 2 will print message error + warning
                    If level == 3 will print message error + warning + info
                    Defaults is 0.
            print_time (bool, optional): Print time if True
    Example:
            log('INF','rol > 0.02 taked 0.02',1)
    """
    if tp == "INF":
        tp_str = "INF"
    elif tp == "WRN":
        tp_str = "WRN ->"
    elif tp == "ERR":
        tp_str = "ERR --->"
    else:
        tp_str = "---"

    if level not in [0, 1, 2, 3]:
        raise ValueError("log level must be 0, 1, 2 or 3 !!!")

    time_stamp = ""
    if print_time:
        time_stamp = str(datetime.datetime.now().strftime("%d/%b/%Y-%H:%M:%S")) + '|'
    outMsg = f"|{tp_str}|{time_stamp} {msg}"

    if level == 1:
        if tp == "ERR":
            print(outMsg, flush=True)
    elif level == 2:
        if tp == "ERR" or tp == "WRN":
            print(outMsg, flush=True)
    elif level == 3:
        if tp == "ERR" or tp == "WRN" or tp == "INF":
            print(outMsg, flush=True)

    return outMsg
