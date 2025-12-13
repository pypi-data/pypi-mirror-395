import itertools
import random

import pytest

from ai_parade._toolkit.metadata.size import parse_model_size


@pytest.mark.parametrize(
	"expected_order",
	[
		pytest.param(p, id=name)
		for name, p in [
			("Known sizes", [["test", "small"], ["test", "medium"], ["test", "large"]]),
			("Numeric values", [["test", "1"], ["test", "2"], ["test", "3"]]),
			("prefixed numbers", [["test", "b1"], ["test", "b2"], ["test", "b3"]]),
			(
				"Mixed case sizes",
				[["test", "Small"], ["test", "MEDIUM"], ["test", "Large"]],
			),
			(
				"Tricky columns",
				[["large", "small"], ["medium", "medium"], ["small", "large"]],
			),
		]
	],
)
def test_parse_sizes_correct_order(expected_order):
	random.seed(42)
	items = expected_order.copy()
	random.shuffle(items)

	result, unknown = parse_model_size(items, column=1)

	# Sort both lists
	result = sorted(result, key=lambda x: x[1])
	flattened = list(itertools.chain(*[group for key, size, group in result]))
	assert flattened == expected_order
	assert len(unknown) == 0


@pytest.mark.parametrize(
	"items",
	[
		pytest.param(p, id=name)
		for name, p in [
			("Version numbers", [["test", "v1"], ["test", "v2"], ["test", "v3"]]),
			("Invalid input (empty strings)", [["test", ""], ["test", ""]]),
			(
				"numbers, all same",
				[["test", "2", "a"], ["test", "2", "b"], ["test", "2", "c"]],
			),
			(
				"Prefixed numbers, all same",
				[
					["test", "small2", "a"],
					["test", "small2", "b"],
					["test", "small2", "c"],
				],
			),
			(
				"Wrong column",
				[["small", "test"], ["medium", "test"], ["large", "test"]],
			),
			(
				"Just invalid values",
				[["test", "2small"], ["test", "invalid"], ["test", "large2x"]],
			),
		]
	],
)
def test_parse_sizes_unknown_values(items):
	result, unknown = parse_model_size(items, column=1)
	assert len(result) == 0
	assert len(unknown) == len(items)
	assert unknown == items


# todo: test multiple values with same size
# todo: test column/max_column parameters


def test_parse_sizes_with_empty_input():
	items = []
	result, unknown = parse_model_size(items)
	assert len(result) == 0
	assert len(unknown) == 0
