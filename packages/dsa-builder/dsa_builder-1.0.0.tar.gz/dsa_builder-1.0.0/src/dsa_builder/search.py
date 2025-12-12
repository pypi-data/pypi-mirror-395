# ds/search.py
from __future__ import annotations
from typing import Optional, Sequence, TypeVar

T = TypeVar("T")
K = TypeVar("K")


def linear_search(seq: Sequence[T], target: T) -> int:
    """
    Return index of first occurrence of target in seq, or -1 if not found.
    Works for any sequence (list, tuple). O(n).
    """
    for i, v in enumerate(seq):
        if v == target:
            return i
    return -1


def binary_search_iterative(sorted_seq: Sequence[T], target: T) -> int:
    """
    Standard binary search on a sorted sequence.
    Returns index of target or -1 if not found.
    Preconditions: sorted_seq must be sorted ascending with respect to `==` and `<`.
    """
    lo, hi = 0, len(sorted_seq) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = sorted_seq[mid]
        if val == target:
            return mid
        if val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def binary_search_recursive(sorted_seq: Sequence[T], target: T, lo: int = 0, hi: Optional[int] = None) -> int:
    """
    Recursive binary search wrapper. Returns index or -1.
    """
    if hi is None:
        hi = len(sorted_seq) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    val = sorted_seq[mid]
    if val == target:
        return mid
    if val < target:
        return binary_search_recursive(sorted_seq, target, mid + 1, hi)
    return binary_search_recursive(sorted_seq, target, lo, mid - 1)


def lower_bound(sorted_seq: Sequence[T], target: T) -> int:
    """
    First index i where sorted_seq[i] >= target.
    If all elements < target, returns len(sorted_seq).
    Useful as insertion point (like bisect_left).
    """
    lo, hi = 0, len(sorted_seq)
    while lo < hi:
        mid = (lo + hi) // 2
        if sorted_seq[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(sorted_seq: Sequence[T], target: T) -> int:
    """
    First index i where sorted_seq[i] > target.
    If all elements <= target, returns len(sorted_seq).
    """
    lo, hi = 0, len(sorted_seq)
    while lo < hi:
        mid = (lo + hi) // 2
        if sorted_seq[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def find_first_last(sorted_seq: Sequence[T], target: T) -> tuple[int, int]:
    """
    Return (first_index, last_index) of target in sorted_seq.
    If not found, returns (-1, -1).
    Uses lower_bound and upper_bound. O(log n).
    """
    lo = lower_bound(sorted_seq, target)
    if lo == len(sorted_seq) or sorted_seq[lo] != target:
        return -1, -1
    hi = upper_bound(sorted_seq, target) - 1
    return lo, hi


def search_in_rotated_array(nums: Sequence[T], target: T) -> int:
    """
    Search target in rotated sorted array (no duplicates).
    E.g., [4,5,6,7,0,1,2] rotated at pivot. Returns index or -1.
    Standard modified binary search O(log n).
    """
    if not nums:
        return -1
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        # Left half sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # Right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
