"""Generate docsbrowser documentation

Classes and functions are generated directly to markdown files by the same
name. Globals are generates to files in the `globals` folders.  The main
module documents are generated to the `README.md` file.
"""

import os, sys
sys.path.append("..")
import olypen

def title(x):
	return x[0].upper() + x[1:].replace(' ','_') + ".md"

with open("README.md","wt") as fh:
	print(olypen.__doc__,file=fh)

classes = dict([(x,getattr(olypen,x)) for x in dir(olypen) 
	if not x.startswith('_') and type(getattr(olypen,x)) is type])
for item,value in classes.items():
	with open(title(item),"wt") as fh:
		print(f"[[/{item}]] - {value.__doc__}",file=fh,end="\n\n")
		functions = dict([(x,getattr(value,x)) for x in dir(value) 
			if not x.startswith('_') and callable(getattr(value,x))])
		print(item,functions)
		if functions:
			print("Functions\n---------\n",file=fh)
			for function,call in functions.items():
				print(function,"\n",'-'*len(function),file=fh,end="\n\n")

functions = dict([(x,getattr(olypen,x)) for x in dir(olypen) 
	if not x.startswith('_') and callable(getattr(olypen,x))])
if functions:
	for item,value in functions.items():
		with open(title(item),"wt") as fh:
			print(f"[[/{item}]] - {value.__doc__}",file=fh)

variables = dict([(x,getattr(olypen,x)) for x in dir(olypen) 
	if not x.startswith('_') and not type(getattr(olypen,x)) in [type,type(sys)] and not callable(getattr(olypen,x))])
if variables:
	os.makedirs("Globals",exist_ok=True)
	for item,value in variables.items():
		with open(os.path.join("Globals",item.replace(' ','_')+".md"),"wt") as fh:
			print(f"[[/Globals/{item}]] - Global variable",file=fh)
			default = f"'{value}'" if type(value) is str else value
			print("\n",file=fh)
			print(f"Type is `{type(value).__name__}`. Default is `{default}`.",file=fh)