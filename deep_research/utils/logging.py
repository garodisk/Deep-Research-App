RESET = "\x1b[0m"
BOLD  = "\x1b[1m"
DIM   = "\x1b[2m"
CYAN  = "\x1b[36m"
GREEN = "\x1b[32m"
YELL  = "\x1b[33m"
MAG   = "\x1b[35m"

def info(msg: str):  print(f"{CYAN}ℹ️  {msg}{RESET}")

def step(msg: str):  print(f"{GREEN}✅ {msg}{RESET}")

def warn(msg: str):  print(f"{YELL}⚠️  {msg}{RESET}")

def doing(msg: str): print(f"{MAG}🔎 {msg}{RESET}")