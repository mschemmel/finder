import datetime 

class Colors:
	OK = "\033[92m"
	WARNING = "\033[93m"
	ERROR = "\033[91m"
	NC = "\033[0m"

  
def now() -> str:
  return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
