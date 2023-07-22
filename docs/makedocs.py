"""Generate docsbrowser documentation

Classes and functions are generated directly to markdown files by the same
name. Globals are generates to files in the `globals` folders.  The main
module documents are generated to the `README.md` file.
"""

import os, sys
sys.path.append("..")
import olypen as target

def title(x):
	return x[0].upper() + x[1:].replace(' ','_') + ".md"

def write_readme(target):
	with open("README.md","wt") as fh:
		print(target.__doc__,file=fh)

def write_classes(target):
	classes = dict([(x,getattr(target,x)) for x in dir(target) 
		if not x.startswith('_') and type(getattr(target,x)) is type])
	for item,value in classes.items():
		with open("/dev/stderr","wt") as fh:#open(title(item),"wt") as fh:
			print(f"[[/{item}]] - {value.__doc__}",file=fh,end="\n\n")
			functions = dict([(x,getattr(value,x)) for x in dir(value) 
				if not x.startswith('_') and callable(getattr(value,x))])
			if functions:
				print("Functions\n---------\n",file=fh)
				for name,call in functions.items():
					if  "__code__" in dir(call):
						arglist = call.__code__.co_varnames[0:call.__code__.co_argcount]
						print(f"  {target.__name__}.{name}({','.join(arglist)})",file=fh,end="\n\n")
						print("\nParameters:",file=fh)
						for arg in arglist:
							print(f"    {arg} - ",file=fh)
							print(name,arg)

def write_functions(target):
	functions = dict([(x,getattr(target,x)) for x in dir(target) 
		if not x.startswith('_') and callable(getattr(target,x))])
	if functions:
		for item,value in functions.items():
			with open(title(item),"wt") as fh:
				print(f"[[/{item}]] - {value.__doc__}",file=fh)

def write_globals(target):
	variables = dict([(x,getattr(target,x)) for x in dir(target) 
		if not x.startswith('_') and not type(getattr(target,x)) in [type,type(sys)] and not callable(getattr(target,x))])
	if variables:
		os.makedirs("Globals",exist_ok=True)
		for item,value in variables.items():
			with open(os.path.join("Globals",item.replace(' ','_')+".md"),"wt") as fh:
				print(f"[[/Globals/{item}]] - Global variable",file=fh)
				default = f"'{value}'" if type(value) is str else value
				print("\n",file=fh)
				print(f"Type is `{type(value).__name__}`. Default is `{default}`.",file=fh)

if __name__ == "__main__":
	write_readme(target)
	write_classes(target)
	write_functions(target)
	write_globals(target)