import sys, os
if sys.platform != "win32": import termios, tty
else: import msvcrt

def pause():
	if sys.platform == "win32": msvcrt.getch(); return
	try: fd = os.open("/dev/tty", os.O_RDONLY)
	except: fd = sys.stdin.fileno()
	OldAttrs = termios.tcgetattr(fd)
	try: tty.setcbreak(fd); os.read(fd,1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, OldAttrs)
		if isinstance(fd, int) and fd != sys.stdin.fileno():
			try: os.close(fd)
			except: pass
#	else:
#		TerminalSettings = termios.tcgetattr(sys.stdin.fileno())
#		try: tty.setraw(sys.stdin.fileno()); sys.stdin.read(1)
#		finally: termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, TerminalSettings)