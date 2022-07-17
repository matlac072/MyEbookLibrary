from config import LOGFILE

# We re-create the logfile at each execution (to avoid infinite logfile)
with open(LOGFILE, "w") as f: pass

def to_log(stack_trace):
    with open(LOGFILE, "a") as f:
        f.write(stack_trace)
        f.write("\n\n")