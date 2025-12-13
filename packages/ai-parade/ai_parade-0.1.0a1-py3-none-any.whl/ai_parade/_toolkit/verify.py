from inspect import getmembers, isclass
from itertools import chain
from typing import Any, Callable, TypeVar

import numpy as np

from ai_parade._toolkit.data.output import ModelOutput

TType = TypeVar("TType")


def reduce_list(
	my_list: list,
	reduce_function: Callable[[TType, TType], TType],
	list_as_tuples: bool = False,
):
	my_list = my_list.copy()
	if len(my_list) < 2:
		return my_list
	i = 0
	for i in range(1, len(my_list)):
		my_list[i] = reduce_objects(
			my_list[i], my_list[i - 1], reduce_function, list_as_tuples
		)
	return my_list[i]


def reduce_objects(
	object1: Any,
	object2: Any,
	reduce_function: Callable[[TType, TType], TType],
	list_as_tuples: bool = True,
):
	if (
		getattr(object1, "__irreducible__", False)
		or getattr(object2, "__irreducible__", False)
	) or (
		isinstance(object1, (int, float, np.number))
		and isinstance(object2, (int, float, np.number))
	):
		return reduce_function(object1, object2)  # type: ignore
	if isinstance(object1, (list, tuple, np.ndarray)) and isinstance(
		object2, (list, tuple, np.ndarray)
	):
		if list_as_tuples:
			assert len(object1) == len(object2)
			return [
				reduce_objects(value1, value2, reduce_function, list_as_tuples)
				for value1, value2 in zip(object1, object2)
			]
		else:
			return [
				reduce_list(
					list(chain(object1, object2)), reduce_function, list_as_tuples
				)
			]
	elif isinstance(object1, dict) and isinstance(object2, dict):
		assert object1.keys() == object2.keys()
		return {
			key: reduce_objects(
				object1[key], object2[key], reduce_function, list_as_tuples
			)
			for key in object1.keys()
		}
	elif (type(object1) is type(object2)) and (isclass(object1) and isclass(object2)):
		return {
			key: reduce_objects(
				value1, getattr(object2, key), reduce_function, list_as_tuples
			)
			for key, value1 in getmembers(
				object1,
				lambda x: not callable(x[1]) and not x[0].startswith("__"),
			)
		}
	else:
		raise ValueError(f"Unsupported type: {type(object1)}")


def compute_statistics(
	output_list1: list[ModelOutput], output_list2: list[ModelOutput]
):
	diff_list = [
		reduce_objects(output1, output2, lambda x, y: abs(x - y))
		for output1, output2 in zip(output_list1, output_list2)
	]

	max_diff = reduce_list(diff_list, max)
	min_diff = reduce_list(diff_list, min)

	def sum_count(x: int | float | list[float], y: int | float | list[float]):
		if not isinstance(x, list):
			x = [x, 1]
		if not isinstance(y, list):
			y = [y, 1]
		return IrreducibleList([x[0] + y[0], x[1] + y[1]])

	sum_diff = reduce_list(diff_list, sum_count)
	mean_diff = reduce_objects(sum_diff, sum_diff, lambda x, y: x[0] / x[1])

	return {
		"max_difference": max_diff,
		"min_difference": min_diff,
		"mean_difference": mean_diff,
	}


def irreducible(cls: type):
	cls.__irreducible__ = True
	return cls


@irreducible
class IrreducibleList(list):
	pass
