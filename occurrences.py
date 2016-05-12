#  Josh Klaus
#  CS131A  Python
#  Assignment #3
#  Occurrences

# a program that prints out in alphabetical order any 
# unique command line arguments it receives, along with 
# the number of times each one occurred

import sys  # import sys module

command_line_args = set()  # variable for holding unique arguments

# Determining unique command line arguments 
for i in (sys.argv[1:]) :
	command_line_args.add(i)
	
# Printing argument and count of occurrences in command line
for argument in sorted(command_line_args):
	argument_count = len([True for arg in sys.argv if arg is argument in command_line_args])
	print('argument:', argument, 'count:', argument_count)
