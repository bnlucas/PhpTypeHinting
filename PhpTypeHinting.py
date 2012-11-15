import re

import sublime, sublime_plugin


def parseParameters(paramstring):
	
	params = []

	for param in paramstring.split(", "):
		name    = param.split(":")[0]
		type    = "mixed" if param.split(":")[1] == "*" else param.split(":")[1]
		default = "#"

		if "=" in type:
			chunks  = type.split(" = ")
			type    = "mixed" if chunks[0] == "*" else chunks[0]
			default = chunks[1]

		type = "float" if type == "Number" else type
		type = type.lower() if type in ["String", "Array", "Object"] else type

		if "#" == default[0]:
			params.append({"name": name, "type": type})
		else:
			params.append({"name": name, "type": type,
				"default": default})

	return params

def docblockParams(parameters):

	out = ""

	for param in parameters:
		out += "\n\t * @param " + param['type'] + " " + param['name']

	return out

def docblockMethod(name, access, returns, parameters=[]):

	parameters = docblockParams(parameters) if len(parameters) != 0 else ""
		

	if "static" in access:
		access  = access.replace(" static", "")
		access += "\n\t * @static"

	docblock = """	/**
	 * {0}
	 *
	 * @access {1}{3}
	 * @return {2}
	 */
"""

	return docblock.format(name, access, returns, parameters)

def docblockProperty(name, access, type):

	if "static" in access:
		access  = access.replace(" static", "")
		access += "\n\t * @static"

	docblock = """	/**
	 * @access {0}
	 * @var {1} {2}
	 */
"""

	return docblock.format(access, type, name)

def typehint(region, view):

	line    = view.substr(region)
	regex   = "(p[a-z]*|p[a-z]*\sstatic)\sfunction\s([a-z_0-9]*)\((.*)\):([a-z]*);"
	pattern = re.compile(regex, re.I);
	match   = pattern.match(line.replace("\t", "").strip())

	if match:

		mod    = match.group(1)
		name   = match.group(2)
		type   = "mixed" if match.group(4) == "*" else match.group(4).lower()
		params = []
		types  = []

		if match.group(3):
		
			for param in parseParameters(match.group(3)):
			
				if "default" in param:
					params.append(param['name'] + " = " + param['default'])
				else:
					params.append(param['name'])

				types.append(param['type'])

			ntypes = ["string", "int", "float", "bool", "resource", "mixed"]

			for i in range(len(params)):
				if not types[i] in ntypes:
					params[i] = types[i] + " " + params[i]
				ntypes.extend(["object", "array"])
				if not types[i] in ntypes:
					types[i] = "object"

			params  = ", ".join(params)
			types   = '", "'.join(types)

			method  = docblockMethod(name, mod, type,
				parseParameters(match.group(3)))
			method += "\t" + mod + " function " + name + "(" + params + ") {\n"
			method += "\t\tTypeCheck::check(\"" + types + "\");\n\t\t\n\t}"

		else:

			method  = docblockMethod(name, mod, type)
			method += "\t" + mod + " function " + name + "() {\n\t\t\n\t}"

		return method

	regex   = "(p[a-z]*|p[a-z]*\sstatic)\s(\$[a-z_0-9]*):([a-z]*);"
	pattern = re.compile(regex, re.I);
	match   = pattern.match(line.replace("\t", "").strip())

	if match:

		mod   = match.group(1)
		name  = match.group(2)
		type  = "mixed" if match.group(3) == "*" else match.group(3).lower()

		prop  = docblockProperty(name, mod, type)
		prop += "\t" + mod + " " + name + ";"

		return prop

	return line

class PhpTypeHintingCommand(sublime_plugin.TextCommand):

	def run(self, view):

		regions  = []
		newlines = []

		for region in [sublime.Region(0, self.view.size())]:
			lines = self.view.split_by_newlines(region)

			for line in lines:
				region = self.view.line(line)
				newlines.append(typehint(region, self.view))

		self.view.sel().clear()

		try:
			edit = self.view.begin_edit("php_type_hinting")
			self.view.replace(edit, sublime.Region(0, self.view.size()), "")
			self.view.insert(edit, 0, "\n".join(newlines).lstrip("\n"))
		finally:
			self.view.end_edit(edit)