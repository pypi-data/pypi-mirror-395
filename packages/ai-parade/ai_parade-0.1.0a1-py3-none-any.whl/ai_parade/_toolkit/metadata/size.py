import re
from itertools import groupby

sizes = [
	# small metric
	"yocto",
	"zepto",
	"atto",
	"femto",
	"pico",
	"nano",
	"micro",
	"milli",
	# small whatever
	"tiny",
	"mini",
	# x smalls
	"xxxs",
	"xxxsmall",
	"xxs",
	"xxsmall",
	"xs",
	"xsmall",
	"s",
	"small",
	# base
	"b",
	"base",
	"m",
	"medium",
	# x larges
	"l",
	"large",
	"x",
	"xl",
	"xlarge",
	"xxl",
	"xxlarge",
	"xxxl",
	"xxxlarge",
	# large whatever
	"huge",
	"giant",
]


def parse_model_size(
	items: list[list[str]], column: int = 0, max_column: int = 1
) -> tuple[list[tuple[list[str], float | int, list[list[str]]]], list[list[str]]]:
	"""
	Try to parse splitted model names to find the model size.
	Looks only on columns (indexes) between column <= here < max_column

	It tests columns against this heuristics to find the size, first found is used:
		- if column is in the size list (case insensitive), use its index as a size
		- if column doesn't have the same value for all items:
			- if column is numeric, use it as a size
			- if column has a common prefix and then a number, use it as a size

	See tests for examples.

	Args:
		items: list of models each model is a lists of strings
		column: first column (index) to try to extract the size from
		max_column: last column (index) to try to extract the size from

	Returns:
		list of tuples of size (common prefix, size, models) and list of models with unknown size
	"""
	sizes_map: list[tuple[list[str], float | int, list[list[str]]]] = []
	unknown_list: list[list[str]] = []
	maybe_known: list[tuple[tuple[str, str], list[str]]] = []

	# lets work only on prefixes:
	for k, group in groupby(items, lambda x: x[column] if len(x) > column else ""):
		size = None
		group = list(group)
		name = group[0][:column]
		try:
			# no numbers: try to find it in sizes
			if k.isalpha():
				size = sizes.index(k.lower())
			# if not same for all items
			elif len(group) != len(items):
				# its number: use it
				if k.isnumeric():
					size = float(k)
				else:
					# it ends with a number, we will see if other groups also ends with a number (different), if so we will use it
					result = re.search(r"\d+$", k)
					if result is not None:
						index = result.start()
						if k[:index] != "v":
							maybe_known.extend(
								[((k[:index], k[index:]), item) for item in group]
							)
							continue
			if size is not None:
				sizes_map.append((name, size, group))
		except ValueError:
			pass
		if size is None:
			# lets try next column if possible
			if len(group) > 1 and column + 1 < max_column:
				parsed, unknown = parse_model_size(group, column + 1)
				sizes_map += parsed
				unknown_list += unknown
			else:
				unknown_list += group

	# here we regroup the items that ends with a number, first group them by the alpha part
	for key, group in groupby(maybe_known, lambda x: x[0][0]):
		group = list(group)
		name = group[0][1][:column] + [key]
		# here we group them by the number part
		for key, number_group in groupby(group, lambda x: x[0][1]):
			number_group = list(number_group)
			number_group_items = [item[1] for item in number_group]

			# if there are multiple different numbers
			if len(number_group) != len(group):
				sizes_map.append((name, float(key), number_group_items))
			else:
				unknown_list += number_group_items

	return sizes_map, unknown_list
