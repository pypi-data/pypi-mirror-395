binary_tree = """
class TreeNode:
    def __init__(self, value):
        self.val = value
        self.left = None
        self.right = None


def array_to_tree(arr, index=0):
    if index >= len(arr) or arr[index] is None:
        return None
    root = TreeNode(arr[index])
    root.left = array_to_tree(arr, index * 2 + 1)
    root.right = array_to_tree(arr, index * 2 + 2)
    return root

def tree_to_array(root):
    # BFS
    result = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node:
            queue.append(node.left)
            queue.append(node.right)
            result.append(node.val)
        else:
            result.append(None)
    return result

"""
linked_list = """
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


def array_to_list(arr, i=0):
    if i >= len(arr):
        return None
    head = ListNode(arr[i])
    head.next = array_to_list(arr, i + 1)
    return head

def list_to_array(head):
    arr = []
    while head:
        arr.append(head.val)
        head = head.next
    return arr
"""
questions = {
    0: {
        "markdown": """
### Score tally
Given an array of scores e.g `[ '5', '2', 'C', 'D', '+', '+', 'C' ]`, calculate the total points where:
```
+  add the last two scores.
D  double the last score.
C  cancel the last score and remove it.
x  add the score
```
You're always guaranteed to have the last two scores for `+` and the previous score for `D`.
### Example
```
input: [ '5', '2', 'C', 'D', '+', '+', 'C' ]
output: 30
explanation:
    '5' - add 5 -> [5]
    '2' - add 2 -> [5, 2]
    'C' - cancel last score -> [5]
    'D' - double last score -> [5, 10]
    '+' - sum last two scores -> [5, 10, 15]
    '+' - sum last two scores -> [5, 10, 15, 25]
    'C' - cancel last score -> [5, 10, 15]
    return sum -> 30
```
""",
        "test_cases": """
test_cases = [
    [[["5", "2", "C", "D", "+", "+", "C"]], 30],
    [[["9", "C", "6", "D", "C", "C"]], 0],
    [[["3", "4", "9", "8"]], 24],
    [[["4", "D", "+", "C", "D"]], 28],
    [[["1", "C"]], 0],
    [[["1", "1", "+", "+", "+", "+", "+", "+", "+", "+"]], 143],
    [[["1", "D", "D", "D", "D", "D"]], 63],
    [[["1", "1"] + ["+"] * 1_00], 2427893228399975082452],
    [[["1", "1"] + ["D"] * 1_00], 2535301200456458802993406410752],
    [[["1", "1"] + ["D"] * 100_000 + ["C"] * 100_001], 1],
    [[["1", "1"] + ["+"] * 50 + ["C"] * 30 + ["+"] * 20], 701408732],
    [[["1", "1", "C", "D", "D", "+"] * 1000], 1300],
]
""",
        "title": "Score tally",
        "rank": "Easy",
    },
    1: {
        "markdown": """
### Repeated letters
Given a string k of lower-case letters. the letters can be repeated and
exist consecutively. A substring from k is considered valld if it contains
at least three consecutive identical letters.

An example: k = "abcdddeeeeaabbbed" has three valid substrings: "ddd",
"eeee" and "bbb".

You must order the pairs by the start index in ascending order
### Example
```
Input: "abcdddeeeeaabbbcd"
Output: [[3,5], [6,9], [12,15]]
```
""",
        "test_cases": """
test_cases = [
    [["abcdddeeeeaabbbb"], [[3, 5], [6, 9], [1azqa  1qwv                                         b2, 15]]],
    [["xxxcyyyyydkkkkkk"], [[0, 2], [4, 8], [10, 15]]],
    [
        ["abcdddeeeeaabbbb" * 6],
        [
            [3, 5],
            [6, 9],
            [12, 15],
            [19, 21],
            [22, 25],
            [28, 31],
            [35, 37],
            [38, 41],
            [44, 47],
            [51, 53],
            [54, 57],
            [60, 63],
            [67, 69],
            [70, 73],
            [76, 79],
            [83, 85],
            [86, 89],
            [92, 95],
        ],
    ],
    [["abcd"], []],
    [["aabbccdd"], []],
    [[""], []],
    [["abcdefffghijkl"], [[5, 7]]],
    [["abcdeffghijkl" * 100_000], []],
    [["abcdeffghijkl" * 100_000 + "kkk"], [[1_300_000, 1_300_002]]],
    [["kkk" + "abcdeffghijkl" * 100_000], [[0, 2]]],
    [["abcdefffghijkl" * 100_000], [[5 + i, 7 + i] for i in range(0, 100_000 * 14, 14)]],
]""",
        "title": "Repeated letters",
        "rank": "Easy",
    },
    2: {
        "markdown": """
### Valid matching brackets
Given a string of brackets that can either be `[]`, `()` or `{}`.
Check if the brackets are valid.

There no other characters in the string apart from '[', ']', '(', ')', '{'and '}'.

### Example
```
input: "[](){}"
output: True

input: "{{}}[][](()"
output: False

input: "[[[()]]]{}"
output: True
```
""",
        "test_cases": """
test_cases = [
    [["[](){}"], True],
    [["{{}}[][](()"], False],
    [["[[[()]]]{}"], True],
    [["[[[(((((((()))))))]]]{[{[{[{{({})}}]}]}]}"], False],
    [["[[[([[[[[[[[[[[[[[[()]]]]]]]]]]]]]]])]]]{}"], True],
    [["[[[()]]]{[](){}()[{[{{]}}]}]}"], False],
    [["[[[()]]]{[](){}()[{[{{[]]}}]}]}{}[]((()))"], False],
    [["[[[()]]]{}"], True],
    [["["], False],
    [["{}" * 50_000 + "()" * 50_000 + "[]"], True],
    [
        [
            "{{{{{{{{{{{{{{{{{{{{{{{{{{{{[[[[[[[[[[()]]]]]]]]]]}}}}}}}}}}}}}}}}}}}}}}}}}}}}"
        ],
        True,
    ],
    [["[" + "()" * 100_000 + ")"], False],
    [["[" + "()" * 100_000 + "]"], True],
]
""",
        "title": "Valid matching brackets",
        "rank": "Easy",
    },
    3: {
        "markdown": """
### Max sum sub array
Given an integer array nums, find a contiguous non-empty subarray within the array that has the largest sum,
and return the sum.

### Example
```
input: [-2, 0, -1]
output: 0

input: [2, 3, -2, 4]
output: 7
```
```
""",
        "test_cases": """
test_cases = [
    [[[-2, 0, -1]], 0],
    [[[-2, 0, -1] * 1000], 0],
    [[[2, 3, -2, 4]], 7],
    [[[2, 3, -2, 4] * 100_000], 700_000],
    [[[-2]], -2],
    [[[i for i in range(100_000)]], 4_999_950_000],
    [[[2] * 50_000 + [-2] * 50_000], 100_000],
    [[[2, -4, 8, 6, 9, -1, 3, -4, 12]], 33],
    [[[2, -4, 8, 0, 9, -1, 0, -4, 12]], 24],
    [[[2, -4, 8, 0, 9, -1, 0, -4, 12] * 10_000], 220_002],
]
""",
        "title": "Max sum sub array",
        "rank": "Easy",
    },
    4: {
        "markdown": """
### Max product sub array
Given an integer array nums, find a contiguous non-empty subarray within the array that has the largest product,
and return the product.

### Example
```
input: [-2, 0, -1]
output: 0

input: [2, 3, -2, 4]
output: 6
```
```
""",
        "test_cases": """
test_cases = [
    [[[-2, 0, -1]], 0],
    [[[2, 3, -2, 4]], 6],
    [[[-2, 0, -1, -3]], 3],
    [[[-2]], -2],
    [[[1 for _ in range(200_000)]], 1],
    [[[2, -4, 8, 6, 9, -1, 3, -4, 12]], 497664],
    [[[2, 0, 0, 0, 0, 0, 0, 0, 12]], 12],
    [[[2, -4, 1, -6, 0, -1, 3, 0, 12]], 48],
    [[[2, -4, 8, 0, 9, -1, 3, -4, 0]], 12],
    [[[2, -4, 0, 6, 9, 0, 3, -4, 12]], 54],
    [[[2, 0, 8, 6, 9, 0, 3, 0, 12]], 432],
    [[[1, -1, 1, 1, 1, -1, 1, -1, 1]], 1],
    [[[2, -1, -1, 1, 1, -1, 0, 2, 1]], 2],
    [[[2, -1, -1, 1, 1, -1, 0, 2, 1] * 100_000], 4],
]
""",
        "title": "Max product sub array",
        "rank": "Easy",
    },
    5: {
        "markdown": """
### Symmetric difference
Create a function that takes two or more arrays and returns a set of their symmetric difference. The returned array must contain only unique values (no duplicates).

The mathematical term symmetric difference (△ or ⊕) of two sets is the set of elements which are in either of the two sets but not in both.

### Example
```
input: [[1, 2, 3], [2, 3, 4]]
output: [1, 4]
```
""",
        "test_cases": """
test_cases = [
    [[[1, 2, 3], [2, 3, 4]], {1, 4}],
    [[[1, 2, 3, 3, 2]], {1, 2, 3}],
    [[[1], [2], [3], [4], [5], [6]], {1, 2, 3, 4, 5, 6}],
    [[[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]], {1, 7}],
    [[[1, 2, 4, 4], [0, 1, 6], [0, 1]], {2, 4, 6}],
    [[[i] for i in range(6)], {0, 1, 2, 3, 4, 5}],
    [[[-1], [], [], [0], [1]], {-1, 0, 1}],
    [
        [
            [9, -4, 8, 3, 12, 0, -4, 8],
            [3, 3, 8, 6, 7, 10],
            [11, 12, 10, 13],
            [5, 15, 3],
            [11, 15, 11, 11, 6, -2],
        ],
        {9, -4, 0, 7, 13, 5, -2},
    ],
    [[[2] * 50_000 + [-2] * 50_000], {2, -2}],
    [[[i for i in range(100_000)], [i for i in range(100_000)]], {}],
    [
        [[i for i in range(100_000)], [i for i in range(10, 100_000)]],
        {i for i in range(10)},
    ],
]
""",
        "title": "Symmetric difference",
        "rank": "Easy",
    },
    6: {
        "markdown": """
### Pairwise
Given an array `arr`, find element pairs whose sum equal the second argument `target` and return the sum of their indices.
e.g pairwise([7, 9, 11, 13, 15], 20) returns 6 and pairwise([0, 0, 0, 0, 1, 1], 1) returns 10.

Each element can only construct a single pair.

### Example
```
inputs:
    arr: [7, 9, 11, 13, 15]
    target: 20
output: 6
explanation:
    pairs 7 + 13 and 9 + 11, indices 0 + 3 and 1 + 2, total 6

inputs:
    arr: [0, 0, 0, 0, 1, 1]
    target: 1
output: 10
explanation: pairs 0 + 1 and 0 + 1, indices 0 + 4 and 1 + 5, total 10
```
""",
        "test_cases": """
test_cases = [
    [[[7, 9, 11, 13, 15], 20], 6],
    [[[0, 0, 0, 0, 1, 1], 1], 10],
    [[[-1, 6, 3, 2, 4, 1, 3, 3], 5], 15],
    [[[1, 6, 5], 6], 2],
    [[[1, 6, 5, 15, 13, 2, 11], 10], 0],
    [[[i for i in range(0, 100_000, 10)], 10], 1],
]
""",
        "title": "Pairwise",
        "rank": "Easy",
    },
    7: {
        "markdown": """
### Min length sub array
Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray whose sum is greater than or equal to target.

If there is no such subarray, return 0 instead.

### Example
```
inputs:
    arr: [2, 3, 1, 2, 4, 3],
    target: 7
output: 2
explanation: sub array [4, 3] has sum >= 7

inputs:
    arr: [1, 3, 6, 2, 1],
    target: 4
output: 1
explanation: sub array [6] has sum >= 4
```
""",
        "test_cases": """
test_cases = [
    [[[2, 3, 1, 2, 4, 3], 7], 2],
    [[[1, 3, 6, 2, 1], 4], 1],
    [[[i for i in range(500_000)], 3_000_000], 7],
    [[[i for i in range(-10, 10)], 60], 0],
]
""",
        "title": "Min length sub array",
        "rank": "Medium",
    },
    8: {
        "markdown": """
### Min in rotated array
Suppose an array of length n sorted in ascending order is rotated between 1 and n times.
For example, the array nums = [0, 1, 2, 4, 5, 6, 7] becomes [4, 5, 6, 7, 0, 1, 2] if it was rotated 4 times. [0, 1, 2, 4, 5, 6, 7] if it was rotated 7 times.

Given the sorted rotated array nums of unique elements, return the minimum element of this array.
You must write an algorithm that runs in O(log n) time.
### Example
```
input: arr: [4, 5, 6, 7, 0, 1, 2]
output: 0
```
""",
        "test_cases": """
test_cases = [
    [[[4, 5, 6, 7, 0, 1, 2]], 0],
    [[[16, 23, 43, 55, -7, -4, 3, 5, 9, 15]], -7],
    [[[i for i in range(36, 1_000_000, 10)]], 36],
    [
        [
            [i for i in range(-10, 1_000_000, 10)]
            + [i for i in range(-1_000_000, -10, 10)]
        ],
        -1_000_000,
    ],
    [[[2]], 2],
]
""",
        "title": "Min in rotated array",
        "rank": "Medium",
    },
    9: {
        "markdown": """
### Count primes
Given a positive integer `n`, write an algorithm to return the number of prime numbers in [0, n]
### Example
```
input: 1000
output: 168
explanation:
    There are 168 prime numbers between 0 and 1000 inclusive.
```
""",
        "test_cases": """
test_cases = [
    [[100], 25],
    [[1_000], 168],
    [[10_000], 1229],
    [[100_000], 9592],
    [[2], 1],
    [[3], 2],
    [[1], 0],
    [[1_000_000], 78498],
],
""",
        "title": "Count primes",
        "rank": "Medium",
    },
    10: {
        "markdown": """
### Permutations
Given an array nums of distinct integers, return all the possible permutations.
You can return the permutations in any order.

Can you do it without python's itertools?

### Example
```
input: [1, 2]
output: [[1, 2], [2, 1]]
```
""",
        "test_cases": """
test_cases = [
    [[[1, 2]], [[1, 2], [2, 1]]],
    [
        [[i for i in range(1, 5)]],
        [
            [1, 2, 3, 4],
            [1, 2, 4, 3],
            [1, 3, 2, 4],
            [1, 3, 4, 2],
            [1, 4, 2, 3],
            [1, 4, 3, 2],
            [2, 1, 3, 4],
            [2, 1, 4, 3],
            [2, 3, 1, 4],
            [2, 3, 4, 1],
            [2, 4, 1, 3],
            [2, 4, 3, 1],
            [3, 1, 2, 4],
            [3, 1, 4, 2],
            [3, 2, 1, 4],
            [3, 2, 4, 1],
            [3, 4, 1, 2],
            [3, 4, 2, 1],
            [4, 1, 2, 3],
            [4, 1, 3, 2],
            [4, 2, 1, 3],
            [4, 2, 3, 1],
            [4, 3, 1, 2],
            [4, 3, 2, 1],
        ],
    ],
    [[[1]], [[1]]],
]
""",
        "title": "Permutations",
        "rank": "Medium",
    },
    11: {
        "markdown": """
### Combinations
Given a string and a positive integer k, return all possible combinations of characters of size k.
You can return the combinations in any order.

Are your hands tied without python's itertools 😅?

### Example
```
input:
    string: "abcd",
    k: 3
output: 'abc', 'abd', 'acd', 'bcd'
```
""",
        "test_cases": """
test_cases = [
    [["abcd", 3], ["abc", "abd", "acd", "bcd"]],
    [
        ["combinations", 2],
        [
            "co",
            "cm",
            "cb",
            "ci",
            "cn",
            "ca",
            "ct",
            "ci",
            "co",
            "cn",
            "cs",
            "om",
            "ob",
            "oi",
            "on",
            "oa",
            "ot",
            "oi",
            "oo",
            "on",
            "os",
            "mb",
            "mi",
            "mn",
            "ma",
            "mt",
            "mi",
            "mo",
            "mn",
            "ms",
            "bi",
            "bn",
            "ba",
            "bt",
            "bi",
            "bo",
            "bn",
            "bs",
            "in",
            "ia",
            "it",
            "ii",
            "io",
            "in",
            "is",
            "na",
            "nt",
            "ni",
            "no",
            "nn",
            "ns",
            "at",
            "ai",
            "ao",
            "an",
            "as",
            "ti",
            "to",
            "tn",
            "ts",
            "io",
            "in",
            "is",
            "on",
            "os",
            "ns",
        ],
    ],
    [["rat", 3], ["rat"]],
    [["rat", 1], ["r", "a", "t"]],
    [["rat", 0], []],
]
""",
        "title": "Combinations",
        "rank": "Medium",
    },
    12: {
        "markdown": """
### Single number
Given a non-empty array of integers `nums`, every element appears twice except for one.

Find that single one.

### Example
```
input: [4, 1, 2, 1, 2]
output: 4
```
""",
        "test_cases": """
test_cases =  [
    [[[4, 1, 2, 1, 2]], 4],
    [[[2]], 2],
    [[[i for i in range(1, 500_000)] + [i for i in range(500_000)]], 0],
]
""",
        "title": "Single number",
        "rank": "Easy",
    },
    13: {
        "markdown": """
### Powers of 2
Given an integer `n`, find whether it is a power of `2`.

### Example
```
input: 64
output: True

input: 20
output: False
```
""",
        "test_cases": """
test_cases = [
    [[64], True],
    [[20], False],
    [[1024], True],
    [[2], True],
    [[0], False],
    [[1267650600228229401496703205376], True],
    [[1267650600228229401496703205377], False],
    [[-64], False],
]
""",
        "title": "Powers of 2",
        "rank": "Easy",
    },
    14: {
        "markdown": """
### Reverse Polish Notation
Evaluate the value of an arithmetic expression in Reverse Polish Notation. Valid operators are +, -, *, and /. Each operand may be an integer or another expression.

Note that division between two integers should truncate toward zero.
It is guaranteed that the given RPN expression is always valid.
That means the expression will always evaluate to a result, and there will not be any division by zero operation.

### Example
```
input: ["2", "1", "+", "3", "*"]
output: 9
explanation: ((2 + 1) * 3) = 9

input: ["4", "13", "5", "/", "+"]
output: 6
explanation: (4 + (13 / 5)) = 6
```
""",
        "test_cases": """
test_cases = [
    [[["2", "1", "+", "3", "*"]], 9],
    [[["4", "13", "5", "/", "+"]], 6],
    [
        [["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]],
        12,
    ],
]
""",
        "title": "Reverse polish notation",
        "rank": "Easy",
    },
    15: {
        "markdown": """
### Roman numerals
Convert a given integer, `n`,  to its equivalent roman numerals for 0 < `n` < 4000.

|Decimal | 1000 | 900 | 400 | 100 | 90 | 50 | 40 | 10 | 9 | 5 | 4 | 1 |
|--------|------|-----|-----|-----|----|----|----|----|---|---|---|---|
|Roman | M | CM | CD | C | XC | L | XL | X | IX | V | IV | I|


### Example
```
input: 4
output: 'IV'

input: 23
output: 'XXIII'
```
""",
        "title": "Roman numerals",
        "rank": "Medium",
        "test_cases": """
test_cases = [
    [[4], "IV"],
    [[23], "XXIII"],
    [[768], "DCCLXVIII"],
    [[1], "I"],
    [[3999], "MMMCMXCIX"],
    [[369], "CCCLXIX"],
    [[1318], "MCCCXVIII"],
    [[1089], "MLXXXIX"],
    [[2424], "MMCDXXIV"],
    [[999], "CMXCIX"],
]
""",
    },
    16: {
        "markdown": """
### Longest common substring (LCS)
Given two strings text1 and text2, return their longest common substring. If there is no common substring, return ''.

A substring of a string is a new string generated from the original string with adjacent characters.
For example, "rain" is a substring of "grain". A common substring of two strings is a substring that is common to both strings.

### Example
```
input:
    text1: "brain"
    text2: 'drain'
output: 'rain'
```
""",
        "title": "Longest common substring",
        "rank": "Medium",
        "test_cases": """
test_cases = [
    [["brain", "drain"], "rain"],
    [["math", "arithmetic"], "th"],
    [["blackmarket", "stagemarket"], "market"],
    [
        ["theoldmanoftheseaissowise", "sowisetheoldmanoftheseais"],
        "theoldmanoftheseais",
    ],
],
""",
    },
    17: {
        "markdown": """
### Happy number
Starting with any positive integer, replace the number by the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.

Those numbers for which this process ends in 1 are happy numbers, while those that do not end in 1 are unhappy numbers.

Implement a function that returns true if the number is happy, or false if not.
### Example
```
input: 2
output: False

input: 7
output: True
```
""",
        "title": "Happy number",
        "rank": "Easy",
        "test_cases": """
test_cases = [
    [["brain", "drain"], "rain"],
    [["math", "arithmetic"], "th"],
    [["blackmarket", "stagemarket"], "market"],
    [
        ["theoldmanoftheseaissowise", "sowisetheoldmanoftheseais"],
        "theoldmanoftheseais",
    ],
],
""",
    },
    18: {
        "markdown": """
### Trie/Prefix tree
In English, we have a concept called root, which can be followed by some other word to form another longer word - let's call this word derivative. For example, when the root "help" is followed by the word "ful", we can form a derivative "helpful".

Given a dictionary consisting of many roots and a sentence consisting of words separated by spaces, replace all the derivatives in the sentence with the root forming it. If a derivative can be replaced by more than one root, replace it with the root that has the shortest length.

Return the sentence after the replacement.

### Example
```
input:
    dictionary = ["cat", "bat", "rat"],
    sentence = "the cattle was rattled by the battery"
output: "the cat was rat by the bat"

input:
    dictionary = ["a", "b", "c"],
    sentence = "aadsfasf absbs bbab cadsfafs"
output: "a a b c"
```
""",
        "title": "Trie/Prefix tree",
        "rank": "Medium",
        "test_cases": """
test_cases = [
    [
        [["cat", "bat", "rat"], "the cattle was rattled by the battery"],
        "the cat was rat by the bat",
    ],
    [[["a", "b", "c"], "aadsfasf absbs bbab cadsfafs"], "a a b c"],
]
""",
    },
    19: {
        "markdown": """
### Fractional knapsack
Given a knapsack capacity and two arrays, the first one for weights and the second one for values. Add items to the knapsack to maximize the sum of the values of the items that can be added so that the sum of the weights is less than or equal to the knapsack capacity.

You are allowed to add a fraction of an item.

### Example
```
inputs:
  capacity = 50
  weights = [10, 20, 30]
  values = [60, 100, 120]
output: 240
```
""",
        "title": "Fractional knapsack",
        "rank": "Easy",
        "test_cases": """
test_cases = [
    [[50, [10, 20, 30], [60, 100, 120]], 240],
    [[60, [10, 20, 30], [60, 100, 120]], 280],
    [[5, [10, 20, 30], [60, 100, 120]], 30],
],
""",
    },
    20: {
        "markdown": """
### Subarrays with sum
Given an array and targetSum, return the total number of contigous subarrays inside the array whose sum is equal to targetSum

### Example
```
inputs:
  arr = [13, -1, 8, 12, 3, 9]
  target = 12
output: 3
explanation: [13, -1], [12] and [3, 9]
```
""",
        "title": "Subarrays with sum",
        "rank": "Easy",
        "test_cases": """
test_cases = [
    [[[13, -1, 8, 12, 3, 9], 12], 3],
    [[[13, -1, 8, 12, 3, 9], 2], 0],
    [[[13, -1, 8, 12, 3, 9], 10], 0],
    [[[13, -1, 8, 12, 3, 9, 7, 5, 9, 10], 75], 1],
    [[[13, -1, 8, 12, 3, 9] * 20_000, 12], 60_000],
    [[[13, -1, 8, 12, 3, 9, 7, 5, 9, 10] * 10_000, 24], 30_000],
],
""",
    },
    21: {
        "markdown": """
### Paths with sum
Given the root of a binary tree and an integer targetSum, return the number of paths where the sum of the values along the path equals targetSum.

The path does not need to start or end at the root or a leaf, but it must go downwards (i.e., traveling only from parent nodes to child nodes).
### Example
```
inputs:
  root = [10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]
  target = 8
output: 3
```
""",
        "test_cases": f"""
{binary_tree}
root1 = array_to_tree([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1])
root2 = array_to_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
test_cases = [
        [[root1, 8], 3],
        [[root2, 22], 3],
        [[root2, 20], 1],
]
""",
        "title": "Paths with sum",
        "rank": "Medium",
    },
    22: {
        "markdown": """
### Remove occurence
Given two strings s and part, perform the following operation on s until all occurrences of the substring part are removed:

Find the leftmost occurrence of the substring part and remove it from s. Return s after removing all occurrences of part.

A substring is a contiguous sequence of characters in a string.
### Example
```
inputs:
  s = "axeaxae"
  part = "ax"
output: 'eae'
```
""",
        "title": "Remove occurence",
        "rank": "Easy",
        "test_cases": """
test_cases = [
    [["axeaxae", "ax"], "eae"],
    [["axxxxyyyyb", "xy"], "ab"],
    [["daa-cbaa-c-c", "a-c"], "dab"],
    [["shesellsseashellsattheseashore", "sh"], "esellsseaellsattheseaore"],
]
""",
    },
    23: {
        "markdown": """
### Spinal case
Given a string. Convert it to spinal case

Spinal case is all-lowercase-words-joined-by-dashes.

### Example
```
input: "Hello World!"
output: "hello-world"
```
""",
        "title": "Spinal case",
        "rank": "Easy",
        "test_cases": """
test_cases = [
    [["Hello World!"], "hello-world"],
    [["The Greatest of All Time."], "the-greatest-of-all-time"],
    [["yes/no"], "yes-no"],
    [["...I-am_here lookingFor  You.See!!"], "i-am-here-looking-for-you-see"],
]
""",
    },
    24: {
        "markdown": """
### 0/1 knapsack
Given a knapsack capacity and two arrays, the first one for weights and the second one for values. Add items to the knapsack to maximize the sum of the values of the items that can be added so that the sum of the weights is less than or equal to the knapsack capacity.

You can only either include or not include an item. i.e you can't add a part of it.

Return a tuple of maximum value and selected items

### Example
```
inputs:
  capacity = 50
  weights = [10, 20, 30]
  values = [60, 100, 120]

output: (220, [0, 1, 1])
```
""",
        "title": "0/1 knapsack",
        "rank": "Easy",
        "test_cases": """
test_cases = [
    [[50, [10, 20, 30], [60, 100, 120]], (220, [0, 1, 1])],
    [[60, [10, 20, 30], [60, 100, 120]], (280, [1, 1, 1])],
    [[5, [10, 20, 30], [60, 100, 120]], (0, [0, 0, 0])],
]
""",
    },
    25: {
        "markdown": """
### Equal array partitions
Given an integer array nums, return true if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or false otherwise.

### Example
```
input: [1, 5, 11, 5]
output: True
explanation: [1, 5, 5] and [11]
```
""",
        "title": "Equal array partitions",
        "rank": "Medium",
        "test_cases": """
test_cases = [
    [[[1, 5, 11, 5]], True],
    [[[6]], False],
    [[[i for i in range(300)]], True],
    [[[1, 5, 13, 5]], False],
    [[[1, 5, 11, 5] * 100], True],
    [[[1, 5, 13, 5, 35, 92, 11, 17, 13, 53]], False],
    [[[i for i in range(1, 330, 2)]], False],
]
""",
    },
    26: {
        "markdown": """
### Fibonacci numbers
Given a positive interger `n`, return the n<sup>th</sup> fibonacci number

The first 6 fibonacci numbers are:
[0, 1, 1, 2, 3, 5]
### Example
```
input: 0
output: 0

input: 1
output: 1

input: 5
output: 5
```
""",
        "title": "Fibonacci numbers",
        "rank": "Easy",
        "test_cases": """
test_cases = [
    [[0], 0],
    [[1], 1],
    [[5], 5],
    [[10], 55],
    [[23], 28657],
    [[50], 12586269025],
    [[100], 354224848179261915075],
],
""",
    },
    27: {
        "markdown": """
### Climb stairs
You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

### Example
```
input: 0
output: 0
explanation: no stairs, no way to get to the top

input: 1
output: 1
explanation: 1 stair, one way to get to the top

input: 2
output: 2
explanation:
  2 ways to get to the top
    - climb stair 1 then stair 2
    - climb 2 steps to stair 2
```
""",
        "title": "Climb stairs",
        "rank": "Easy",
        "test_cases": """
test_cases = [
    [[0], 0],
    [[1], 1],
    [[2], 2],
    [[10], 89],
    [[36], 24157817],
],
""",
    },
    28: {
        "markdown": """
### Ways to make change
There are four types of common coins in US currency:
  - quarters (25 cents)
  - dimes (10 cents)
  - nickels (5 cents)
  - pennies (1 cent)

  There are six ways to make change for 15 cents:
    - A dime and a nickel
    - A dime and 5 pennies
    - 3 nickels
    - 2 nickels and 5 pennies
    - A nickel and 10 pennies
    - 15 pennies

Implement a function to determine how many ways there are to make change for a given input, `cents`, that represents an amount of US pennies using these common coins.

### Example
```
input: 15
output: 6
```
""",
        "title": "Ways to make change",
        "rank": "Medium",
        "test_cases": """
test_cases = [
    [[15], 6],
    [[10], 4],
    [[5], 2],
    [[55], 60],
    [[1000], 142511],
    [[10_000], 134235101],
],
""",
    },
    29: {
        "markdown": """
### Has path sum
Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.

A leaf is a node with no children.

### Example
```
input:
  root = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, None, None, 1]
  target = 18
output: True
```
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, None, None, 1])
t2 = array_to_tree([1, 2, 3, None, 4])
test_cases = [
    [[t1, 18], True],
]
""",
        "title": "Has path sum",
        "rank": "Medium",
    },
    30: {
        "markdown": """
### Merge sorted linked lists
Given two sorted linked lists, head1 and head2. Merge them into one sorted linked list.

### Example
```
input:
  l1 = [2, 4, 6, 6, 12, 22]
  l2 = [3, 7, 8, 9]
output: [2, 3, 4, 6, 6, 7, 8, 9, 12, 22]
```
""",
        "test_cases": f"""
{linked_list}
l1 = array_to_list([2, 4, 6, 6, 12, 22])
l2 = array_to_list([3, 7, 8, 9])
l3 = array_to_list([2, 3, 4, 6, 6, 7, 8, 9, 12, 22])
test_cases = [
    [[l1, l2], l3],
]
""",
        "title": "Merge sorted linked lists",
        "rank": "Medium",
    },
    31: {
        "markdown": """
### Has node BST
Given the root of a binary search tree and a value x, check whether x is in the tree and return `True` or `False`
### Example
```
input:
  root = [9, 8, 16]
  x = 5
output: False

input:
  root = [12, 3, 20]
  x = 3
output: True
```
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([9, 8, 16])
t2 = array_to_tree([9, 8, 16, 4])
t3 = array_to_tree([12, 3, 20])
t4 = array_to_tree([12, 3, 20, None, 5])
test_cases = [
    [[t1, 5], False],
    [[t3, 3], True],
    [[t2, 4], True],
    [[t4, 21], False],
]
""",
        "title": "Has node BST",
        "rank": "Medium",
    },
    32: {
        "markdown": """
### BST min
Given the root of a binary search tree find the minimum value and return it
### Example
```
input: [12, 3, 20]
output: 3
```
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([9, 8, 16])
t2 = array_to_tree([9, 8, 16, 4])
t3 = array_to_tree([12, 3, 20])
t4 = array_to_tree([12, 3, 20, None, 5])
test_cases = [
    [[t3], 3],
    [[t1], 8],
    [[t2], 4],
    [[t4], 3],
]
""",
        "title": "BST min",
        "rank": "Medium",
    },
    33: {
        "markdown": """
### Balanced tree
Given the root of a binary search tree, return `True` if it is balanced or `False` otherwise

A balanced tree is one whose difference between maximum height and minimum height is less than 2

### Example
```
input: [12, 8, 16, 4, 9, 13, 18, 11]
output: True

input: [4, None, 9, None, None, None, 12]
output: False
```
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([12, 8, 16, 4, 9, 13, 18, 11])
t2 = array_to_tree([4, None, 9, None, None, None, 12])
t3 = array_to_tree([12, 3, 20, None, 5])
test_cases = [
    [[t1], True],
    [[t2], False],
    [[t3], True],
]
""",
        "title": "Balanced tree",
        "rank": "Medium",
    },
    34: {
        "markdown": """
### Tree in-order traversal
Given the root of a binary search tree, traverse the tree in order and return the values as an array.

### Example
```
input: [12, 8, 16, 4, 9, 13, 18, 11]
output: [4, 8, 9, 11, 12, 13, 16, 18]
```
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([12, 8, 16, 4, 9, 13, 18, 11])
test_cases = [
    [[t1], [4, 8, 9, 11, 12, 13, 16, 18]],
]
""",
        "title": "Tree in-order traversal",
        "rank": "Medium",
    },
    35: {
        "markdown": """
### Tree pre-order traversal
Given the root of a binary search tree, traverse the tree using pre order traversal and return the values as an array.

### Example
```
input: [12, 8, 16, 4, 9, 13, 18, 11]
output: [12, 8, 4, 9, 11, 16, 13, 18]
```
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([12, 8, 16, 4, 9, 13, 18, 11])
test_cases = [
    [[t1], [12, 8, 4, 9, 11, 16, 13, 18]],
]
""",
        "title": "Tree pre-order traversal",
        "rank": "Medium",
    },
    36: {
        "markdown": """
### Tree post-order traversal
Given the root of a binary search tree, traverse the tree using post order traversal and return the values as an array.

### Example
```
input: [12, 8, 16, 4, 9, 13, 18, 11]
output: [4, 11, 9, 8, 13, 18, 16, 12]
```
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([12, 8, 16, 4, 9, 13, 18, 11])
test_cases = [
    [[t1], [4, 11, 9, 8, 13, 18, 16, 12]],
]
""",
        "title": "Tree post-order traversal",
        "rank": "Medium",
    },
    37: {
        "markdown": """
### Tree level-order traversal
Given the root of a binary search tree, traverse the tree using level order traversal and return the values as an array.

### Example
```
input: [12, 8, 16, 4, 9, 13, 18, 11]
output: [12, 8, 16, 4, 9, 13, 18, 11]
```
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([12, 8, 16, 4, 9, 13, 18, 11])
test_cases = [
    [[t1], [12, 8, 16, 4, 9, 13, 18, 11]],
]
""",
        "title": "Tree level-order traversal",
        "rank": "Medium",
    },
    38: {
        "markdown": """
### Tree leaves
Given the root of a binary search tree, return all the leaves as an array ordered from left to right.

### Example
```
input: [12, 8, 16, 4, 9, 13, 18, 11]
output: [4, 11, 13, 18]
```
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([12, 8, 16, 4, 9, 13, 18, 11])
test_cases = [
    [[t1], [4, 11, 13, 18]],
]
""",
        "title": "Tree leaves",
        "rank": "Medium",
    },
    39: {
        "markdown": """
### Sum right nodes
Given the root of a binary search tree, return the sum of all the right nodes

### Example
```
input: [12, 8, 16, 4, 9, 13, 18, 11]
output: 25
```
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([12, 8, 16, 4, 9, 13, 18, 11])
test_cases = [
    [[t1], 25],
]
""",
        "title": "Sum right nodes",
        "rank": "Medium",
    },
    40: {
        "markdown": """
### Value in array
Given an array of values sorted in a non decreasing order, and a target `y`. Return `True` if y is in the array or `False` otherwise

### Example
```
input:
  arr = [2, 4, 8, 9, 12, 13, 16, 18]
  y = 18
output: True
```
""",
        "test_cases": """
test_cases = [
    [[[2, 4, 8, 9, 12, 13, 16, 18], 18], True],
    [[[i for i in range(5_000_000)], 45], True],
    [[[i for i in range(5_000_000)], 5_000_000], False],
]
""",
        "title": "Value in array",
        "rank": "Easy",
    },
    41: {
        "markdown": """
### Merge sort
Given an array of integers, use merge sort algorithm to return an array of all the integers sorted in non decreasing order.

### Example
```
input: [8, 2, 4, 9, 12, 18, 16, 13]
output: [2, 4, 8, 9, 12, 13, 16, 18]
```
""",
        "test_cases": """
test_cases = [
    [[[8, 2, 4, 9, 12, 18, 16, 13]], [2, 4, 8, 9, 12, 13, 16, 18]],
    [[[i for i in range(100_000, -1, -1)]], [i for i in range(100_001)]],
]
""",
        "title": "Merge sort",
        "rank": "Easy",
    },
    42: {
        "markdown": """
### Heap sort
Given an array of integers, use heap sort algorithm to return an array of all the integers sorted in non decreasing order.

### Example
```
input: [8, 2, 4, 9, 12, 18, 16, 13]
output: [2, 4, 8, 9, 12, 13, 16, 18]
```
""",
        "test_cases": """
test_cases = [
    [[[8, 2, 4, 9, 12, 18, 16, 13]], [2, 4, 8, 9, 12, 13, 16, 18]],
    [[[i for i in range(100_000, -1, -1)]], [i for i in range(100_001)]],
]
""",
        "title": "Heap sort",
        "rank": "Easy",
    },
    43: {
        "markdown": """
### Quick sort
Given an array of integers, use quick sort algorithm to return an array of all the integers sorted in non decreasing order.

### Example
```
input: [8, 2, 4, 9, 12, 18, 16, 13]
output: [2, 4, 8, 9, 12, 13, 16, 18]
```
""",
        "test_cases": """
test_cases = [
    [[[8, 2, 4, 9, 12, 18, 16, 13]], [2, 4, 8, 9, 12, 13, 16, 18]],
    [[[i for i in range(100_000, -1, -1)]], [i for i in range(100_001)]],
]
""",
        "title": "Quick sort",
        "rank": "Easy",
    },
    44: {
        "markdown": """
### Bubble sort
Given an array of integers, use bubble sort algorithm to return an array of all the integers sorted in non decreasing order.

### Example
```
input: [8, 2, 4, 9, 12, 18, 16, 13]
output: [2, 4, 8, 9, 12, 13, 16, 18]
```
""",
        "test_cases": """
test_cases = [
    [[[8, 2, 4, 9, 12, 18, 16, 13]], [2, 4, 8, 9, 12, 13, 16, 18]],
    [[[i for i in range(100_000, -1, -1)]], [i for i in range(100_001)]],
]
""",
        "title": "Bubble sort",
        "rank": "Easy",
    },
    45: {
        "markdown": """
### Insertion sort
Given an array of integers, use insertion sort algorithm to return an array of all the integers sorted in non decreasing order.

### Example
```
input: [8, 2, 4, 9, 12, 18, 16, 13]
output: [2, 4, 8, 9, 12, 13, 16, 18]
```
""",
        "test_cases": """
test_cases = [
    [[[8, 2, 4, 9, 12, 18, 16, 13]], [2, 4, 8, 9, 12, 13, 16, 18]],
    [[[i for i in range(100_000, -1, -1)]], [i for i in range(100_001)]],
]
""",
        "title": "Insertion sort",
        "rank": "Easy",
    },
    46: {
        "markdown": """
### Selection sort
Given an array of integers, use selection sort algorithm to return an array of all the integers sorted in non decreasing order.

### Example
```
input: [8, 2, 4, 9, 12, 18, 16, 13]
output: [2, 4, 8, 9, 12, 13, 16, 18]
```
""",
        "test_cases": """
test_cases = [
    [[[8, 2, 4, 9, 12, 18, 16, 13]], [2, 4, 8, 9, 12, 13, 16, 18]],
    [[[i for i in range(100_000, -1, -1)]], [i for i in range(100_001)]],
]
""",
        "title": "Selection sort",
        "rank": "Easy",
    },
    47: {
        "markdown": """
### Smaller to the right
Given an integer array nums, return an integer array counts where counts[i] is the number of smaller elements to the right of nums[i].

### Example
```
input: [5, 2, 2, 6, 1]
output: [3, 1, 1, 1, 0]

input: [-1, -1]
output: [0, 0]
```
""",
        "test_cases": """
test_cases = [
    [[[5, 2, 2, 6, 1]], [3, 1, 1, 1, 0]],
    [[[-1, -1]], [0, 0]],
    [[[8, 2, 4, 9, 12, 18, 16]], [2, 0, 0, 0, 0, 1, 0]],
    [[[i for i in range(100_000, -1, -1)]], [0 for i in range(100_001)]],
]
""",
        "title": "Smaller to the right",
        "rank": "Hard",
    },
    48: {
        "markdown": """
### Majority element 
> Leetcode #169

Given an array nums of size n, return the majority element.
The majority element is the element that appears more than
⌊n / 2⌋ times.

You may assume that the majority element always
exists in the array.
### Example
```
Input: [3, 2, 3]
Output: 3
```
""",
        "test_cases": """
test_cases = [
    [[[3, 2, 3]], 3],
    [[[6] * 20], 6],
    [[[9] * 21 + [7] * 20], 9],
    [[[2]], 2],
    [[[]], None],
    [[[6] * 100_000 + [9] * 100_001], 9],
    [[[-2, -2, -4, -2, -4, -4, -4]], -4],

]""",
        "title": "Majority element",
        "rank": "Easy",
    },
    49: {
        "markdown": """
### Max profit
> Leetcode 121

You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

### Examples
Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

Example 2:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.

Constraints:

    1 <= prices.length <= 10^5
    0 <= prices[i] <= 10^4

You are given an array `prices` where `prices[i]` is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction.
If you cannot achieve any profit, return 0.
""",
        "test_cases": """
test_cases = [
    [[[7, 1, 5, 3, 6, 4]], 5],
    [[[7, 6, 4, 3, 1]], 0],
    [[[0, 0, 0, 0]], 0],
    [[[4] * 2_000 + [15] * 1_000], 11],
    [[[90] * 10_000 + [50] * 20_000], 0],
    [[[]], 0],
    [[[i for i in range(1, 100_000)]], 99_998],
]
""",
        "title": "Max profit",
        "rank": "Easy",
    },
    50: {
        "markdown": """
### Two sum 
> Leetcode #1

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

### Examples
Example 1:

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:

Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:

Input: nums = [3,3], target = 6
Output: [0,1]

Constraints:

    2 <= nums.length <= 104
    -109 <= nums[i] <= 109
    -109 <= target <= 109
    Only one valid answer exists.
""",
        "test_cases": """
test_cases = [
    [[[2, 7, 11, 15], 13], [1, 3]],
    [[[2, 4, 7, 14], 6], [1, 2]],
    [[[i for i in range(400_000)], 5], [1, 6]],
    [[[i for i in range(-10, 10)], -10], [1, 11]],
],
""",
        "title": "Single pair sum sorted list",
        "rank": "Easy",
    },
    51: {
        "markdown": """
### Longest common subsequence (LCS) 
> Leetcode #1143

Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

    For example, "ace" is a subsequence of "abcde".

A common subsequence of two strings is a subsequence that is common to both strings.


### Examples
Example 1:

Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: The longest common subsequence is "ace" and its length is 3.

Example 2:

Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.

Example 3:

Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.



Constraints:

    1 <= text1.length, text2.length <= 1000
    text1 and text2 consist of only lowercase English characters.
""",
        "title": "Longest common subsequence",
        "rank": "Medium",
        "test_cases": [
            [["math", "arithmetic"], "ath"],
            [["original", "origin"], "origin"],
            [["foo", "bar"], ""],
            [["", "arithmetic"], ""],
            [["shesellsseashellsattheseashore", "isawyouyesterday"], "saester"],
            [["@work3r", "m@rxkd35rt"], "@rk3r"],
        ],
    },
    52: {
        "markdown": """
### Jump game I 
> Leetcode #55

You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.

Return true if you can reach the last index, or false otherwise.

### Examples
Example 1:

Input: nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:

Input: nums = [3,2,1,0,4]
Output: false
Explanation: You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.

Constraints:

    1 <= nums.length <= 104
    0 <= nums[i] <= 105
""",
        "title": "Jump game I",
        "rank": "Medium",
        "test_cases": [
            [[[2, 3, 1, 1, 4]], True],
            [[[0]], True],
            [[[2, 1, 1, 0, 4]], False],
            [[[i for i in range(200_000)]], False],
            [[[1 for _ in range(200_000)]], True],
            [[[0, 0]], False],
            [[[200_000] + [0] * 200_000], True],
        ],
    },
    53: {
        "markdown": """
### Jump game II 
> Leetcode #45

You are given a 0-indexed array of integers nums of length n. You are initially positioned at nums[0].

Each element nums[i] represents the maximum length of a forward jump from index i. In other words, if you are at nums[i], you can jump to any nums[i + j] where:

    0 <= j <= nums[i] and
    i + j < n

Return the minimum number of jumps to reach nums[n - 1]. The test cases are generated such that you can reach nums[n - 1].

### Examples
Example 1:

Input: nums = [2,3,1,1,4]
Output: 2
Explanation: The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:

Input: nums = [2,3,0,1,4]
Output: 2

Constraints:

    1 <= nums.length <= 104
    0 <= nums[i] <= 1000
    It's guaranteed that you can reach nums[n - 1]
""",
        "title": "Jump game II",
        "rank": "Medium",
        "test_cases": [
            [[[2, 3, 1, 1, 4]], 2],
            [[[1]], 0],
            [[[1, 5]], 1],
            [[[1 for _ in range(200_000)]], 199_999],
            [[[200_000] + [0] * 200_000], 1],
        ],
    },
    54: {
        "markdown": """
### Jump game III
> Leetcode #1306

Given an array of non-negative integers arr, you are initially positioned at start index of the array. When you are at index i, you can jump to i + arr[i] or i - arr[i], check if you can reach any index with value 0.

Notice that you can not jump outside of the array at any time.

### Examples
Example 1:

Input: arr = [4,2,3,0,3,1,2], start = 5
Output: true
Explanation:
All possible ways to reach at index 3 with value 0 are:
index 5 -> index 4 -> index 1 -> index 3
index 5 -> index 6 -> index 4 -> index 1 -> index 3

Example 2:

Input: arr = [4,2,3,0,3,1,2], start = 0
Output: true
Explanation:
One possible way to reach at index 3 with value 0 is:
index 0 -> index 4 -> index 1 -> index 3

Example 3:

Input: arr = [3,0,2,1,2], start = 2
Output: false
Explanation: There is no way to reach at index 1 with value 0.

Constraints:

    1 <= arr.length <= 5 * 104
    0 <= arr[i] < arr.length
    0 <= start < arr.length
""",
        "title": "Jump game III",
        "rank": "Medium",
        "test_cases": [
            [[[4, 2, 3, 0, 3, 1, 2], 0], True],
            [[[3, 0, 2, 1, 2], 2], False],
            [[[4, 2, 3, 0, 3, 1, 2], 5], True],
        ],
    },
    55: {
        "markdown": """
### House robber I 
> Leetcode #198

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

### Examples
Example 1:

Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

Example 2:

Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.

Constraints:

    1 <= nums.length <= 100
    0 <= nums[i] <= 400
""",
        "title": "House robber I",
        "rank": "Medium",
        "test_cases": [
            [[[1, 2, 3, 1]], 4],
            [[[1, 7, 2, 1, 6]], 13],
            [[[1, 2]], 2],
            [[[3]], 3],
            [[[i for i in range(0, 100_000, 100)]], 25_000_000],
        ],
    },
    56: {
        "markdown": """
### House robber II
> Leetcode #213

ou are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

### Examples
Example 1:

Input: nums = [2,3,2]
Output: 3
Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2), because they are adjacent houses.

Example 2:

Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

Example 3:

Input: nums = [1,2,3]
Output: 3

Constraints:

    1 <= nums.length <= 100
    0 <= nums[i] <= 1000
""",
        "title": "House robber II",
        "rank": "Medium",
        "test_cases": [
            [[[1, 2, 3, 1]], 4],
            [[[1, 7, 2, 1, 6]], 13],
            [[[1, 2, 3]], 3],
            [[[i for i in range(0, 100_000, 100)]], 25_000_000],
        ],
    },
    57: {
        "markdown": """
### Course schedule 
> Leetcode #207

here are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

    For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return true if you can finish all courses. Otherwise, return false.

### Examples
Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0. So it is possible.

Example 2:

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

Constraints:

    1 <= numCourses <= 2000
    0 <= prerequisites.length <= 5000
    prerequisites[i].length == 2
    0 <= ai, bi < numCourses
    All the pairs prerequisites[i] are unique.
""",
        "title": "Course schedule",
        "rank": "Medium",
        "test_cases": [
            [[2, [[1, 0]]], [0, 1]],
            [[4, [[1, 0], [2, 0], [3, 1], [3, 2]]], [0, 1, 2, 3]],
            [[1, []], [0]],
        ],
    },
    58: {
        "markdown": """
### Minimum height trees (MHTs) 
> Leetcode #310

A tree is an undirected graph in which any two vertices are connected by exactly one path. In other words, any connected graph without simple cycles is a tree.

Given a tree of n nodes labelled from 0 to n - 1, and an array of n - 1 edges where edges[i] = [ai, bi] indicates that there is an undirected edge between the two nodes ai and bi in the tree, you can choose any node of the tree as the root. When you select a node x as the root, the result tree has height h. Among all possible rooted trees, those with minimum height (i.e. min(h))  are called minimum height trees (MHTs).

Return a list of all MHTs' root labels. You can return the answer in any order.

The height of a rooted tree is the number of edges on the longest downward path between the root and a leaf.

### Examples
Example 1:

Input: n = 4, edges = [[1,0],[1,2],[1,3]]
Output: [1]
Explanation: As shown, the height of the tree is 1 when the root is the node with label 1 which is the only MHT.

Example 2:

Input: n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
Output: [3,4]

Constraints:

    1 <= n <= 2 * 104
    edges.length == n - 1
    0 <= ai, bi < n
    ai != bi
    All the pairs (ai, bi) are distinct.
    The given input is guaranteed to be a tree and there will be no repeated edges.
""",
        "title": "Minimum height trees",
        "rank": "Medium",
        "test_cases": [
            [[4, [[1, 0], [1, 2], [1, 3]]], [1]],
            [[6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]], [3, 4]],
        ],
    },
    59: {
        "markdown": """
### Longest common prefix
> Leetcode #14

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".

### Examples
Example 1:

Input: strs = ["flower","flow","flight"]
Output: "fl"

Example 2:

Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.

Constraints:

    1 <= strs.length <= 200
    0 <= strs[i].length <= 200
    strs[i] consists of only lowercase English letters if it is non-empty.
""",
        "title": "Longest common prefix",
        "rank": "Medium",
        "test_cases": [
            [[["flower", "flow", "flight"]], "fl"],
            [[["dog", "racecar", "car"]], ""],
            [
                [
                    [
                        "algology",
                        "algologies",
                        "algologists",
                        "algometer",
                        "algometric",
                        "algometry",
                        "algophobia",
                        "algologically",
                        "algorithm",
                        "algorism",
                    ]
                ],
                "algo",
            ],
            [[["ORGANOMETALLICS", "ORGANOPHOSPHATE", "ORGANOTHERAPY "]], "ORGANO"],
            [[["lower", "low", "light"]], "l"],
            [
                [
                    [
                        "SYSTEMATISE",
                        "SYSTEMATISED",
                        "SYSTEMATISER",
                        "SYSTEMATISERS",
                        "SYSTEMATISES",
                        "SYSTEMATISING",
                        "SYSTEMATISM",
                        "SYSTEMATISMS",
                        "SYSTEMATIST",
                    ]
                ],
                "SYSTEMATIS",
            ],
            [[["garden", "gardener", "gardened", "gardenful", "gardenia"]], "garden"],
            [[["flytrap", "flyway", "flyweight", "flywheel"]], "fly"],
            [[["flower", "flow", ""]], ""],
        ],
    },
    60: {
        "markdown": """
### Cheapest flight within k stops
> Leetcode #787

There are n cities connected by some number of flights. You are given an array flights where flights[i] = [fromi, toi, pricei] indicates that there is a flight from city fromi to city toi with cost pricei.

You are also given three integers src, dst, and k, return the cheapest price from src to dst with at most k stops. If there is no such route, return -1.

### Examples
Example 1:

Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1
Output: 700
Explanation:
The graph is shown above.
The optimal path with at most 1 stop from city 0 to 3 is marked in red and has cost 100 + 600 = 700.
Note that the path through cities [0,1,2,3] is cheaper but is invalid because it uses 2 stops.

Example 2:

Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1
Output: 200
Explanation:
The graph is shown above.
The optimal path with at most 1 stop from city 0 to 2 is marked in red and has cost 100 + 100 = 200.

Example 3:

Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0
Output: 500
Explanation:
The graph is shown above.
The optimal path with no stops from city 0 to 2 is marked in red and has cost 500.

Constraints:

    1 <= n <= 100
    0 <= flights.length <= (n * (n - 1) / 2)
    flights[i].length == 3
    0 <= fromi, toi < n
    fromi != toi
    1 <= pricei <= 104
    There will not be any multiple flights between two cities.
    0 <= src, dst, k < n
    src != dst
""",
        "title": "Cheapest flight with at most k stops",
        "rank": "Medium",
        "test_cases": [
            [
                [
                    4,
                    [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]],
                    0,
                    3,
                    1,
                ],
                700,
            ],
            [
                [
                    4,
                    [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]],
                    0,
                    3,
                    2,
                ],
                400,
            ],
            [
                [
                    3,
                    [[0, 1, 100], [1, 2, 100], [0, 2, 500]],
                    0,
                    2,
                    1,
                ],
                200,
            ],
            [
                [
                    3,
                    [[0, 1, 100], [1, 2, 100], [0, 2, 500]],
                    0,
                    2,
                    0,
                ],
                500,
            ],
        ],
    },
    61: {
        "markdown": """
### Network delay time 
> Leetcode #743

You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.

### Examples
Example 1:

Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2

Example 2:

Input: times = [[1,2,1]], n = 2, k = 1
Output: 1

Example 3:

Input: times = [[1,2,1]], n = 2, k = 2
Output: -1

Constraints:

    1 <= k <= n <= 100
    1 <= times.length <= 6000
    times[i].length == 3
    1 <= ui, vi <= n
    ui != vi
    0 <= wi <= 100
    All the pairs (ui, vi) are unique. (i.e., no multiple edges.)
""",
        "title": "Network delay time",
        "rank": "Medium",
        "test_cases": [
            [[[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2], 2],
            [[[[1, 2, 1]], 2, 1], 1],
            [[[[1, 2, 1]], 4, 2], -1],
        ],
    },
    62: {
        "markdown": """
### Reachable cities
> Leetcode #1334

There are n cities numbered from 0 to n-1. Given the array edges where edges[i] = [fromi, toi, weighti] represents a bidirectional and weighted edge between cities fromi and toi, and given the integer distanceThreshold.

Return the city with the smallest number of cities that are reachable through some path and whose distance is at most distanceThreshold, If there are multiple such cities, return the city with the greatest number.

Notice that the distance of a path connecting cities i and j is equal to the sum of the edges' weights along that path.

### Examples
Example 1:

Input: n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4
Output: 3
Explanation: The figure above describes the graph.
The neighboring cities at a distanceThreshold = 4 for each city are:
City 0 -> [City 1, City 2]
City 1 -> [City 0, City 2, City 3]
City 2 -> [City 0, City 1, City 3]
City 3 -> [City 1, City 2]
Cities 0 and 3 have 2 neighboring cities at a distanceThreshold = 4, but we have to return city 3 since it has the greatest number.

Example 2:

Input: n = 5, edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]], distanceThreshold = 2
Output: 0
Explanation: The figure above describes the graph.
The neighboring cities at a distanceThreshold = 2 for each city are:
City 0 -> [City 1]
City 1 -> [City 0, City 4]
City 2 -> [City 3, City 4]
City 3 -> [City 2, City 4]
City 4 -> [City 1, City 2, City 3]
The city 0 has 1 neighboring city at a distanceThreshold = 2.

Constraints:

    2 <= n <= 100
    1 <= edges.length <= n * (n - 1) / 2
    edges[i].length == 3
    0 <= fromi < toi < n
    1 <= weighti, distanceThreshold <= 10^4
    All pairs (fromi, toi) are distinct.
""",
        "title": "Reachable cities",
        "rank": "Medium",
        "test_cases": [
            [[4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4], 3],
            [
                [
                    5,
                    [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]],
                    2,
                ],
                0,
            ],
        ],
    },
    63: {
        "markdown": """
### Minimum spanning trees 
> Leetcode #1135

There are n cities labeled from 1 to n. You are given the integer n and an array connections where connections[i] = [xi, yi, costi] indicates that the cost of connecting city xi and city yi (bidirectional connection) is costi.

Return the minimum cost to connect all the n cities such that there is at least one path between each pair of cities. If it is impossible to connect all the n cities, return -1.

The cost is the sum of the connections’ costs used.

### Example
```
inputs:
    n = 3,
    connections = [[1, 2, 5], [1, 3, 6], [2, 3, 1]]
output: 6

inputs:
    n = 4,
    connections = [[1, 2, 3], [3, 4, 4]]
output: -1
```
""",
        "title": "Minimum spanning trees",
        "rank": "Medium",
        "test_cases": [
            [[3, [[1, 2, 5], [1, 3, 6], [2, 3, 1]]], 6],
            [[4, [[1, 2, 3], [3, 4, 4]]], -1],
        ],
    },
    64: {
        "markdown": """
### Critical connections
> Leetcode #1192

There are n servers numbered from 0 to n - 1 connected by undirected server-to-server connections forming a network where connections[i] = [ai, bi] represents a connection between servers ai and bi. Any server can reach other servers directly or indirectly through the network.

A critical connection is a connection that, if removed, will make some servers unable to reach some other server.

Return all critical connections in the network in any order.


### Examples
Example 1:

Input: n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]
Output: [[1,3]]
Explanation: [[3,1]] is also accepted.

Example 2:

Input: n = 2, connections = [[0,1]]
Output: [[0,1]]

Constraints:

    2 <= n <= 105
    n - 1 <= connections.length <= 105
    0 <= ai, bi <= n - 1
    ai != bi
    There are no repeated connections.
""",
        "title": "Critical connections",
        "rank": "Hard",
        "test_cases": [
            [[4, [[0, 1], [1, 2], [2, 0], [1, 3]]], [[1, 3]]],
            [
                [7, [[0, 1], [1, 2], [2, 0], [1, 3], [1, 4], [4, 5], [5, 6]]],
                [[1, 3], [5, 6], [4, 5], [1, 4]],
            ],
            [
                [7, [[0, 1], [1, 2], [2, 0], [1, 3], [1, 4], [4, 5], [5, 6], [2, 6]]],
                [[1, 3]],
            ],
        ],
    },
    65: {
        "markdown": """
### Job scheduling
> Leetcode #1235

We have n jobs, where every job is scheduled to be done from startTime[i] to endTime[i], obtaining a profit of profit[i].

You're given the startTime, endTime and profit arrays, return the maximum profit you can take such that there are no two jobs in the subset with overlapping time range.

If you choose a job that ends at time X you will be able to start another job that starts at time X.

### Examples
Example 1:

Input: startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
Output: 120
Explanation: The subset chosen is the first and fourth job.
Time range [1-3]+[3-6] , we get profit of 120 = 50 + 70.

Example 2:

Input: startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]
Output: 150
Explanation: The subset chosen is the first, fourth and fifth job.
Profit obtained 150 = 20 + 70 + 60.

Example 3:

Input: startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]
Output: 6

Constraints:

    1 <= startTime.length == endTime.length == profit.length <= 5 * 104
    1 <= startTime[i] < endTime[i] <= 109
    1 <= profit[i] <= 104
""",
        "title": "Job scheduling",
        "rank": "Easy",
        "test_cases": [
            [[[1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]], 120],
            [[[1, 1, 1], [2, 3, 4], [5, 6, 4]], 6],
        ],
    },
    66: {
        "markdown": """
### Coin change I 
> Leetcode #322

You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

### Examples
Example 1:

Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Example 2:

Input: coins = [2], amount = 3
Output: -1

Example 3:

Input: coins = [1], amount = 0
Output: 0

Constraints:

    1 <= coins.length <= 12
    1 <= coins[i] <= 231 - 1
    0 <= amount <= 104
""",
        "title": "Coin change I",
        "rank": "Medium",
        "test_cases": [
            [[[1, 2, 5], 11], 3],
            [[[1, 2, 5, 10], 11], 2],
            [[[1, 2, 5, 10, 20], 11], 2],
            [[[1, 2, 5, 10, 20], 110], 6],
            [[[1, 2, 5, 10, 20], 63], 5],
            [[[1, 2, 5, 10, 20, 50], 16], 3],
            [[[1, 2, 5, 10, 20, 50], 28], 4],
            [[[1, 2, 5, 10, 20, 50], 77], 4],
        ],
    },
    67: {
        "markdown": """
### Min cost tickets
> Leetcode #983

You have planned some train traveling one year in advance. The days of the year in which you will travel are given as an integer array days. Each day is an integer from 1 to 365.

Train tickets are sold in three different ways:

    a 1-day pass is sold for costs[0] dollars,
    a 7-day pass is sold for costs[1] dollars, and
    a 30-day pass is sold for costs[2] dollars.

The passes allow that many days of consecutive travel.

    For example, if we get a 7-day pass on day 2, then we can travel for 7 days: 2, 3, 4, 5, 6, 7, and 8.

Return the minimum number of dollars you need to travel every day in the given list of days.

### Examples
Example 1:

Input: days = [1,4,6,7,8,20], costs = [2,7,15]
Output: 11
Explanation: For example, here is one way to buy passes that lets you travel your travel plan:
On day 1, you bought a 1-day pass for costs[0] = $2, which covered day 1.
On day 3, you bought a 7-day pass for costs[1] = $7, which covered days 3, 4, ..., 9.
On day 20, you bought a 1-day pass for costs[0] = $2, which covered day 20.
In total, you spent $11 and covered all the days of your travel.

Example 2:

Input: days = [1,2,3,4,5,6,7,8,9,10,30,31], costs = [2,7,15]
Output: 17
Explanation: For example, here is one way to buy passes that lets you travel your travel plan:
On day 1, you bought a 30-day pass for costs[2] = $15 which covered days 1, 2, ..., 30.
On day 31, you bought a 1-day pass for costs[0] = $2 which covered day 31.
In total, you spent $17 and covered all the days of your travel.

Constraints:

    1 <= days.length <= 365
    1 <= days[i] <= 365
    days is in strictly increasing order.
    costs.length == 3
    1 <= costs[i] <= 1000
""",
        "title": "Min cost tickets",
        "rank": "Medium",
        "test_cases": [
            [[[1, 4, 6, 7, 8, 20], [2, 7, 15]], 11],
            [[[1, 2, 3, 4, 5, 6, 7], [2, 7, 15]], 7],
            [[[i for i in range(1, 31)], [2, 7, 15]], 15],
            [[[1, 4, 6], [2, 7, 15]], 6],
            [[[5, 6, 7, 8, 9, 10, 11], [2, 7, 15]], 7],
            [[[5, 6, 7, 8, 9, 10, 11, 210, 211, 212, 213, 365], [2, 7, 15]], 16],
            [[[i for i in range(1, 366)], [2, 7, 15]], 190],
        ],
    },
    68: {
        "markdown": """
### House robber III 
> Leetcode #337

The thief has found himself a new place for his thievery again. There is only one entrance to this area, called root.

Besides the root, each house has one and only one parent house. After a tour, the smart thief realized that all houses in this place form a binary tree. It will automatically contact the police if two directly-linked houses were broken into on the same night.

Given the root of the binary tree, return the maximum amount of money the thief can rob without alerting the police.

### Examples
Example 1:

Input: root = [3,2,3,null,3,null,1]
Output: 7
Explanation: Maximum amount of money the thief can rob = 3 + 3 + 1 = 7.

Example 2:

Input: root = [3,4,5,1,3,null,1]
Output: 9
Explanation: Maximum amount of money the thief can rob = 4 + 5 = 9.

Constraints:

    The number of nodes in the tree is in the range [1, 104].
    0 <= Node.val <= 104
""",
        "test_cases": f"""
{binary_tree}
root = array_to_tree([6, 3, 9, None, 5, 4, 9])
test_cases = [
    [[root], 24],
]
""",
        "title": "House robber III",
        "rank": "Medium",
    },
    69: {
        "markdown": """
### Lowest common ancestor 
> Leetcode #236

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”

### Examples
Example 1:

Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
Explanation: The LCA of nodes 5 and 1 is 3.

Example 2:

Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself according to the LCA definition.

Example 3:

Input: root = [1,2], p = 1, q = 2
Output: 1

Constraints:

    The number of nodes in the tree is in the range [2, 105].
    -109 <= Node.val <= 109
    All Node.val are unique.
    p != q
    p and q will exist in the tree.
""",
        "test_cases": f"""
{binary_tree}
root1 = array_to_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
root2 = array_to_tree([1, 2])
test_cases = [
    [[root1, 5, 1], 3],
    [[root1, 5, 4], 5],
    [[root2, 1, 2], 1],
]
""",
        "title": "Lowest common ancestor",
        "rank": "Medium",
    },
    70: {
        "markdown": """
### Sum linked lists
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit.

Add the two numbers and return the sum as a linked list. You may assume the two numbers do not contain any leading zero, except the number 0 itself.

### Example
```
input:
  l1 = [2, 4, 3]
  l2 = [5, 6, 4]
output: [7, 0, 8]
explanation: 342 + 465 = 807
```
""",
        "test_cases": f"""
{linked_list}
l1 = array_to_list([2, 4, 3])
l2 = array_to_list([5, 6, 4])
l3 = array_to_list([9, 9, 9, 9, 9, 9, 9])
l4 = array_to_list([9, 9, 9, 9])
l12 = array_to_list([7, 0, 8])
l34 = array_to_list([8, 9, 9, 9, 0, 0, 0, 1])
test_cases = [
    [[l1, l2], l12],
    [[l3, l4], l34],
]
""",
        "title": "Sum linked lists",
        "rank": "Medium",
    },
    71: {
        "markdown": """
### Same binary tree 
> Leetcode #100

Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

### Examples
Example 1:

Input: p = [1,2,3], q = [1,2,3]
Output: true

Example 2:

Input: p = [1,2], q = [1,null,2]
Output: false

Example 3:

Input: p = [1,2,1], q = [1,1,2]
Output: false

Constraints:

    The number of nodes in both trees is in the range [0, 100].
    -104 <= Node.val <= 104
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([6, 3, 9, None, 5, 4, 9])
t2 = array_to_tree([6, 3, 9, None, 5, 4, 9])
t3 = array_to_tree([6, 3, 9, 6, 5, 4, 9])
t4 = array_to_tree([])
t5 = array_to_tree([])
test_cases = [
    [[t1, t2], True],
    [[t2, t3], False],
    [[t4, t5], True],
]
""",
        "title": "Same binary tree",
        "rank": "Easy",
    },
    72: {
        "markdown": """
### Boolean tree 
> Leetcode #2331

You are given the root of a full binary tree with the following properties:

    Leaf nodes have either the value 0 or 1, where 0 represents False and 1 represents True.
    Non-leaf nodes have either the value 2 or 3, where 2 represents the boolean OR and 3 represents the boolean AND.

The evaluation of a node is as follows:

    If the node is a leaf node, the evaluation is the value of the node, i.e. True or False.
    Otherwise, evaluate the node's two children and apply the boolean operation of its value with the children's evaluations.

Return the boolean result of evaluating the root node.

A full binary tree is a binary tree where each node has either 0 or 2 children.

A leaf node is a node that has zero children.

### Examples
Example 1:

Input: root = [2,1,3,null,null,0,1]
Output: true
Explanation: The above diagram illustrates the evaluation process.
The AND node evaluates to False AND True = False.
The OR node evaluates to True OR False = True.
The root node evaluates to True, so we return true.

Example 2:

Input: root = [0]
Output: false
Explanation: The root node is a leaf node and it evaluates to false, so we return false.

Constraints:

    The number of nodes in the tree is in the range [1, 1000].
    0 <= Node.val <= 3
    Every node has either 0 or 2 children.
    Leaf nodes have a value of 0 or 1.
    Non-leaf nodes have a value of 2 or 3.
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([2, 1, 3, None, None, 0, 1])
t2 = array_to_tree([0])
test_cases = [
    [[t1], True],
    [[t2], False],
]
""",
        "title": "Boolean binary tree",
        "rank": "Easy",
    },
    73: {
        "markdown": """
### Cousins in a binary tree 
> Leetcode #993

Given the root of a binary tree with unique values and the values of two different nodes of the tree x and y, return true if the nodes corresponding to the values x and y in the tree are cousins, or false otherwise.

Two nodes of a binary tree are cousins if they have the same depth with different parents.

Note that in a binary tree, the root node is at the depth 0, and children of each depth k node are at the depth k + 1.

### Examples
Example 1:

Input: root = [1,2,3,4], x = 4, y = 3
Output: false

Example 2:

Input: root = [1,2,3,null,4,null,5], x = 5, y = 4
Output: true

Example 3:

Input: root = [1,2,3,null,4], x = 2, y = 3
Output: false

Constraints:

    The number of nodes in the tree is in the range [2, 100].
    1 <= Node.val <= 100
    Each node has a unique value.
    x != y
    x and y are exist in the tree.
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([1, 2, 3, None, 4, None, 5])
t2 = array_to_tree([1, 2, 3, None, 4])
test_cases = [
    [[t1, 5, 4], True],
    [[t2, 2, 3], False],
]
""",
        "title": "Cousins",
        "rank": "Medium",
    },
    74: {
        "markdown": """
### Invert binary tree
> Leetcode #226

Given the root of a binary tree, invert the
tree, and return its root.

### Examples
Example 1:

Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]

Example 2:

Input: root = [2,1,3]
Output: [2,3,1]

Example 3:

Input: root = []
Output: []

Constraints:

    The number of nodes in the tree is in the range [0, 100].
    -100 <= Node.val <= 100
""",
        "test_cases": f"""
{binary_tree}
t1 = array_to_tree([4, 2, 7, 1, 3, 6, 9])
t2 = array_to_tree([4, 7, 2, 9, 6, 3, 1])
test_cases = [
    [[t1], t2],
]
""",
        "title": "Invert binary tree",
        "rank": "Medium",
    },
    75: {
        "markdown": """
### Reverse a linked list
Given the head of a linked list, reverse the list, and return its head

### Example
```
input: [1, 2, 3, 4, 5, 6]
output: [6, 5, 4, 3, 2, 1]
```
""",
        "test_cases": f"""
{linked_list}
l1 = array_to_list([1, 2, 3, 4, 5, 6])
l2 = array_to_list([6, 5, 4, 3, 2, 1])
test_cases = [
    [[l1], l2],
]
""",
        "title": "Reverse linked list",
        "rank": "Medium",
    },
    76: {
        "markdown": """
### Calendar book event
> Leetcode 
You are implementing a program to use as your calendar. We can add a new event if adding the event will not cause a double booking. A double booking happens when two events have some non-empty intersection (i.e., some moment is common to both events.).

The event can be represented as a pair of integers start and end that represents a booking on the half-open interval [start, end), the range of real numbers x such that start <= x < end.

Implement the MyCalendar class:

> MyCalendar() Initializes the calendar object.
> boolean book(int start, int end) Returns true if the event can be added to the calendar successfully without causing a double booking. Otherwise, return false and do not add the event to the calendar.

### Example
```python
calendar = MyCalendar()
calendar.book(10, 20)  # True
calendar.book(10, 20)  # False - already booked
calendar.book(15, 25)  # False - overlapping with [10, 20)
calendar.book(20, 30)  # True  
```
""",
        "test_cases": f"""
calendar = MyCalendar()
test_cases = [
    [[calendar.book(10, 20)], True],
    [[calendar.book(10, 20)], False],
    [[calendar.book(15, 25)], False],
    [[calendar.book(20, 30)], True],
    [[calendar.book(30, 31)], True],
    [[calendar.book(100, 2000)], True],
    [[calendar.book(2_000, 6_000_000)], True],
    [[calendar.book(3_000, 50_000)], False],
    [[calendar.book(10_000, 20_000)], False],
    [[calendar.book(0, 6_000_000)], False],
    [[calendar.book(55_556, 3_000_000)], False],
    [[calendar.book(2000, 2020)], False],
    [[calendar.book(5_999_999, 6_000_001)], False],
    [[calendar.book(100_000, 200_000)], False],
    [[calendar.book(31, 41)], True],
    [[calendar.book(42, 50)], True],
    [[calendar.book(50, 60)], True],
    [[calendar.book(60, 70)], True],
    [[calendar.book(70, 80)], True],
    [[calendar.book(80, 90)], True],
    [[calendar.book(90, 100)], True],
]
""",
        "title": "Calendar book event",
        "rank": "Medium",
    },
    77: {
        "markdown": """
### Range frequency query 
> Leetcode 
Design a data structure to find the frequency of a given value in a given subarray. The frequency of a value in a subarray is the number of occurrences of that value in the subarray. Implement the RangeFreqQuery class
```
# Constructs an instance of the classwith the given 0-indexed integer array arr. 
RangeFreqQuery(int[] arr)      
# Returns the frequency of value in the subarray arr[left...right]. 
int query(int left, int right, int value)  
```
A subarray is a contiguous sequence of elements within an array. arr[left...right] denotes the subarray that contains the elements of nums between indices left and right (inclusive).

### Example
```
arr = [1, 3, 7, 7, 7, 3, 4, 1, 7]
rf = RangeFreq(arr)

input: 
  left = 2, right = 5, value = 7
  rf.query(2, 5, 7) 
output:
  3
explanation:
  7 appears 3 times between indices 1 and 6


rf.query(2, 4, 7)  # 3
rf.query(0, 8, 1)  # 2
rf.query(4, 7, 4)  # 1
```
""",
        "test_cases": f"""
arr = [1, 3, 7, 7, 7, 3, 4, 1, 7]
rf1 = RangeFreq(arr)
arr2 = [i for i in range(100_000)]
rf2 = RangeFreq(arr2)
arr3 = [i for i in range(1, 100_000)] + [22] * 50_000 + [-15] * 100_000
rf3 = RangeFreq(arr3)
test_cases = [
    [[rf1.query(2, 4, 7)], 3],
    [[rf1.query(0, 8, 1)], 2],
    [[rf1.query(4, 7, 4)], 1],
    [[rf1.query(2, 4, 9)], 0],
    [[rf1.query(8, 8, 7)], 1],
    [[rf2.query(0, 100_000, 897)], 1],
    [[rf2.query(0, 100_000, 0)], 1],
    [[rf2.query(0, 100_000, 99_999)], 1],
    [[rf2.query(0, 10, 7)], 1],
    [[rf2.query(50_000, 50_000, 50_000)], 1],
    [[rf3.query(0, 250_000, 0)], 1],
    [[rf3.query(0, 250_000, 22)], 50_001],
    [[rf3.query(0, 250_000, -5)], 100_000],
    [[rf3.query(100_000, 150_000, 22)], 50_000],
    [[rf3.query(100_000, 150_005, -15)], 5],
]
""",
        "title": "Range frequency query",
        "rank": "Medium",
    },
}
