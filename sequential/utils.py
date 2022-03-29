# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

from typing import Union, NoReturn, List, Tuple
import statistics

# from sequential.seq2pat import _Constraint, _BaseConstraint

Num = Union[int, float]


def check_true(expression: bool, exception: Exception) -> NoReturn:
    """
    Checks that given expression is true, otherwise raises the given exception.
    """
    if not expression:
        raise exception


def check_false(expression: bool, exception: Exception) -> NoReturn:
    """
        Checks that given expression is false, otherwise raises the given exception.
        """
    if expression:
        raise exception


def read_data(source: str, is_scientific: bool = False) -> List[list]:
    """
    Utility function to read in numeric data from files
    :param source: file path of file to be to be read in
    :param is_scientific: flag to indicate if input file contains values in scientific notation
    :return: a list of list containing values in source
    """
    # Read all rows at once
    with open(source, 'r') as input_file:
        all_rows = input_file.read().splitlines()

    # Automatically detect input type
    if all_rows[0].split()[0].isnumeric() or is_scientific:
        # For each row, split into list and convert to integer
        return [(list(map(float, row.split()))) for row in all_rows]

    # For each row, split into list and convert to string
    return [(list(map(str, row.split()))) for row in all_rows]


def string_to_int(mapping: map, items: List[List[int]]) -> List[list]:
    """
    Utility function to transform string input to int input to be used by sequential library
    :param mapping: map[str, int]
    :param items: a list of ints or a list of ints
    :return: a list of strings where each string is replaced by an integer 'id'
    """
    return [[mapping[i] for i in item] for item in items]


def int_to_string(mapping: map, results: List[List[int]]) -> List[list]:
    """
    Utility function to transform sequential pattern results into original string pattern while retaining the number of
    times each pattern was found
    :param mapping: map[int, str]
    :param results: the output of sequential library
    :return:  list of list in the form [str, str, ... int] where the strings represent a pattern and the int represents
    the number of time the pattern was found
    """
    return [[mapping[item[i]] if i < (len(item) - 1) else item[i] for i in range(len(item))] for item in results]


def get_max_column_size(items: List[List[int]]) -> int:
    """
    Finds and returns the longest row
    :param items: a list of list of ints
    :return: length of the longest row
    """
    return max(list(map(len, items)))


def check_sequence_feature_same_length(items: List[List[int]], attribute: List[List[int]]) -> bool:
    """
    Verifies attributes added to sequential that events in sequences in map one to one for values in attributes
    ie for each row len(items[i] == len(attribute[i])
    :param items: a list of sequences consisting of events
    :param attribute: a list of integer attributes
    :return: true if attributes satisfies requirements false otherwise
    """
    return list(map(len, items)) == list(map(len, attribute))


def check_attributes_int(attribute: List[List[int]]) -> bool:
    """
    Verifies attributes added to sequential are integer values
    :param attribute: a list of integer attributes
    :return: true if attributes satisfies requirements false otherwise
    """
    return all(all(isinstance(a, int) for a in seq) for seq in attribute)


def get_max_value(items: List[List[int]]) -> int:
    """
    Finds and returns maximum value in items
    :param items: a list of list of ints
    :return: max value in items
    """
    return max(list(map(max, items)))


def get_min_value(items: List[List[int]]) -> int:
    """
    Finds and returns minimun value in items
    :param items: a list of list of ints
    :return: max value in items
    """
    return min(list(map(min, items)))


def attr_min(attrs: List[List[int]]) -> list:
    """
    For each attribute: List[int]  in attributes: List finds the minimum value respectively
    :param attrs: A list of list of ints representing attributes
    :return: list where the value of index i is the minimum value for attribute i
    """
    return [min(list(map(min, att))) for att in attrs]


def attr_max(attrs: List[List[int]]) -> list:
    """
    For each attribute: List[int]  in attributes: List finds the maximum value respectively
    :param attrs: A list of list of ints representing attributes
    :return: list where the value of index i is the maximum value for attribute i
    """
    return [max(list(map(max, att))) for att in attrs]


def item_map(items: List[List[str]]) -> (dict, dict):
    """
    Creates a one to one mapping 'str_to_int' to translate list of list of string to list of list of int and another
    mapping 'int_to_str' to translate a list of list converted with 'str_to_int' back to its original
    string representation.
    :param items: List of list of strings
    :return: a maping from string to ints and the reverse mapping from int to string
    """
    # list[list[events]] -> set[events] Unpack all the events in items into a single list and remove duplicates
    # Fix the order of items for creating a deterministic item-ID map
    flat_set = sorted(set([item for sublist in items for item in sublist]))
    # map each event to a unique int ID
    str_to_int = dict([(y, x) for x, y in enumerate(flat_set, start=1)])
    # reverse dictionary where each int ID is mapped to its string representation
    int_to_string = dict([(value, key) for key, value in str_to_int.items()])

    return str_to_int, int_to_string


def compare_results(a: List[list], b: List[list]) -> (List[list], List[list]):
    """
    Compare results from sequential
    :param a: The result from calling sequential
    :param b: The result from calling sequential
    :return: Patterns found in a but not in b and sequences found in b but not in a
    """
    a_filtered = [[items[i] for i in range(len(items)) if i < (len(items) - 1)] for items in a]
    b_filtered = [[items[i] for i in range(len(items)) if i < (len(items) - 1)] for items in b]
    a_result = [item for item in a if item[:-1] not in b_filtered]
    b_result = [item for item in b if item[:-1] not in a_filtered]

    return a_result, b_result


def sort_pattern(patterns: List[list]) -> List[list]:
    """
    Sort sequential results
    :param patterns: The result from calling sequential
    :return: Patterns in descending order by frequency
    """
    # Fix the order of patterns without frequency
    patterns = sorted(patterns, key=lambda x: x[:-1])

    # Return the patterns in descending order by frequency
    return sorted(patterns, key=lambda x: x[-1], reverse=True)


def write_items(file_name: str, items: List[list]) -> NoReturn:
    """
    Simple utility function to write items, attributes, results, or any List[list] to file,
    optimized for very large inputs
    :param file_name: file name as a string should include format as no default is assumed
    :param items: A list of lists of any type
    """
    open_file = open(file_name, 'w')
    open_file.writelines([" ".join([(str(item[i])) if i < (len(item) - 1) else str(item[i]) + "\n"
                                    for i in range(len(item))]) for item in items])
    open_file.close()


def calc_average(result: List[list]) -> list:
    patterns = [row[:-1] for row in result]
    temp = list(map(statistics.mean, patterns))
    return temp


def calc_median(result: List[list]) -> list:
    patterns = [row[:-1] for row in result]
    temp = list(map(statistics.median, patterns))
    return temp


def calc_span(result: List[list]) -> list:
    patterns = [row[:-1] for row in result]
    return []


def drop_frequency(result: List[list]) -> list:
    return list(map(lambda x: x[:-1], result))


def is_subsequence(list1: list, list2: list) -> bool:
    """
    Check if list1 is a subsequence of list2.

    """
    len_list1 = len(list1)
    len_list2 = len(list2)
    index_list1 = 0
    index_list2 = 0

    # Traverse both list1 and list2
    while index_list1 < len_list1 and index_list2 < len_list2:
        # Compare current element of list2 with list1
        if list1[index_list1] == list2[index_list2]:
            # If matched, then move to next element in list1
            index_list1 = index_list1 + 1
        index_list2 = index_list2 + 1
    return index_list1 == len_list1


def is_subsequence_in_rolling(list1: list, list2: list, rolling_window_size: int) -> bool:
    """
    Check if list1 is a subsequence of list2, within a rolling_window of list2.

    """
    res = False

    if len(list1) > len(list2):
        return False

    if len(list2) <= rolling_window_size:
        return is_subsequence(list1, list2)

    else:
        num_iters = len(list2) - rolling_window_size
        for i in range(num_iters + 1):
            if is_subsequence(list1, list2[i:i + rolling_window_size]):
                res = True
                break
    return res


def get_matched_subsequences(seq: list, pattern: list) -> Tuple[list, list]:
    """
    Find all possible subsequences of a sequence in a recursive way.
    For every element in the list, there are two choices, either to include it in the subsequence or not include it.
    Apply this for every element in the list, find the subsequences for the two cases separately.

    """
    res_seq = []
    res_ind = []
    indices = list(range(len(seq)))

    def get_subsequence(subsequence, output, ind_subsequence, ind_output):
        # Base Case
        # if the input is empty, append the output list
        if len(subsequence) == 0:
            if output == pattern:
                res_seq.append(output)
                res_ind.append(ind_output)
            return

        # output is passed with including the
        # 1st element of input list
        get_subsequence(subsequence[1:], output + [subsequence[0]],
                        ind_subsequence[1:], ind_output + [ind_subsequence[0]])

        # output is passed without including the
        # 1st element of input list
        get_subsequence(subsequence[1:], output,
                        ind_subsequence[1:], ind_output)

    get_subsequence(seq, [], indices, [])

    return res_seq, res_ind


def get_average_one_seq(seq):
    return statistics.mean(seq)


def get_median_one_seq(seq):
    return statistics.median(seq)


def get_gap_one_seq(seq):
    return [i - j for i, j in zip(seq[1:], seq[:-1])]


def get_span_one_seq(seq):
    return max(seq) - min(seq)
