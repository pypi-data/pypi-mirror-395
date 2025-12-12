from typing import Callable, List, TypeVar, Optional

T = TypeVar("T")
K = TypeVar("K")

# -------------------------
# Key helper
# -------------------------
def _get_key_func(key: Optional[Callable[[T], K]]):
    return (lambda x: x) if key is None else key


# ============================================================
# BASIC, CLEAN, CONSISTENT SORTING ALGORITHMS
# (Aligned with divide_conquer.py)
# ============================================================

# ------------------------------------------------------------
# Selection Sort (simple, not stable)
# ------------------------------------------------------------
def selection_sort(arr: List[T], key: Optional[Callable[[T], K]] = None) -> List[T]:
    a = arr[:]
    kf = _get_key_func(key)

    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if kf(a[j]) < kf(a[min_idx]):
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]

    return a


# ------------------------------------------------------------
# Bubble Sort (stable)
# ------------------------------------------------------------
def bubble_sort(arr: List[T], key: Optional[Callable[[T], K]] = None) -> List[T]:
    a = arr[:]
    kf = _get_key_func(key)

    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if kf(a[j]) > kf(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


# ------------------------------------------------------------
# Insertion Sort (stable)
# ------------------------------------------------------------
def insertion_sort(arr: List[T], key: Optional[Callable[[T], K]] = None) -> List[T]:
    a = arr[:]
    kf = _get_key_func(key)

    for i in range(1, len(a)):
        cur = a[i]
        j = i - 1
        while j >= 0 and kf(a[j]) > kf(cur):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = cur

    return a


# ------------------------------------------------------------
# Merge Sort (stable, like divide_conquer.mergesort)
# ------------------------------------------------------------
def merge_sort(arr: List[T], key: Optional[Callable[[T], K]] = None) -> List[T]:
    a = arr[:]
    kf = _get_key_func(key)

    if len(a) <= 1:
        return a

    mid = len(a) // 2
    left = merge_sort(a[:mid], key)
    right = merge_sort(a[mid:], key)

    # inline merge logic (no helpers)
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if kf(left[i]) <= kf(right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1

    out.extend(left[i:])
    out.extend(right[j:])
    return out


# ------------------------------------------------------------
# Functional Quicksort (like divide_conquer.quicksort)
# ------------------------------------------------------------


def quick_sort(arr: List[T], key: Optional[Callable[[T], K]] = None) -> List[T]:
    import random
    a = arr[:]
    kf = _get_key_func(key)

    if len(a) <= 1:
        return a

    pivot = a[random.randrange(len(a))]
    pv = kf(pivot)

    left = [x for x in a if kf(x) < pv]
    mid  = [x for x in a if kf(x) == pv]
    right= [x for x in a if kf(x) > pv]

    return quick_sort(left, key) + mid + quick_sort(right, key)


# ------------------------------------------------------------
# Heap Sort (classical, not stable)
# ------------------------------------------------------------
def heap_sort(arr: List[T], key: Optional[Callable[[T], K]] = None) -> List[T]:
    a = arr[:]
    kf = _get_key_func(key)
    n = len(a)

    def heapify(i, size):
        largest = i
        l = 2*i + 1
        r = 2*i + 2

        if l < size and kf(a[l]) > kf(a[largest]):
            largest = l
        if r < size and kf(a[r]) > kf(a[largest]):
            largest = r

        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            heapify(largest, size)

    # build max heap
    for i in range(n//2 - 1, -1, -1):
        heapify(i, n)

    # extract
    for i in range(n-1, 0, -1):
        a[0], a[i] = a[i], a[0]
        heapify(0, i)

    return a


# ------------------------------------------------------------
# Counting Sort (for non-negative ints)
# ------------------------------------------------------------
def counting_sort(arr: List[int]) -> List[int]:
    if not arr:
        return []

    maxv = max(arr)
    count = [0] * (maxv + 1)

    for x in arr:
        count[x] += 1

    out = []
    for val, c in enumerate(count):
        out.extend([val] * c)

    return out


# ------------------------------------------------------------
# Shell Sort
# ------------------------------------------------------------
def shell_sort(arr: List[T], key: Optional[Callable[[T], K]] = None) -> List[T]:
    a = arr[:]
    kf = _get_key_func(key)
    n = len(a)

    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and kf(a[j-gap]) > kf(temp):
                a[j] = a[j-gap]
                j -= gap
            a[j] = temp
        gap //= 2

    return a


# ------------------------------------------------------------
# Radix Sort (non-negative integers)
# ------------------------------------------------------------
def radix_sort(arr: List[int]) -> List[int]:
    if not arr:
        return []

    a = arr[:]
    maxv = max(a)
    exp = 1

    while maxv // exp > 0:
        buckets = [[] for _ in range(10)]
        for num in a:
            buckets[(num // exp) % 10].append(num)
        a = [x for bucket in buckets for x in bucket]
        exp *= 10

    return a


# ------------------------------------------------------------
# Bucket Sort (floats in [0,1))
# ------------------------------------------------------------
def bucket_sort(arr: List[float]) -> List[float]:
    if not arr:
        return []

    n = len(arr)
    buckets = [[] for _ in range(n)]

    for x in arr:
        idx = min(int(x * n), n - 1)
        buckets[idx].append(x)

    # insertion sort each bucket
    for b in buckets:
        for i in range(1, len(b)):
            cur = b[i]
            j = i - 1
            while j >= 0 and b[j] > cur:
                b[j+1] = b[j]
                j -= 1
            b[j+1] = cur

    return [x for b in buckets for x in b]


# ------------------------------------------------------------
# Simple TimSort (not full CPython version)
# ------------------------------------------------------------
def tim_sort(arr: List[T], key: Optional[Callable[[T], K]] = None) -> List[T]:
    a = arr[:]
    kf = _get_key_func(key)
    n = len(a)
    RUN = 32

    # small-run insertion sort
    for start in range(0, n, RUN):
        end = min(start + RUN, n)
        for i in range(start + 1, end):
            cur = a[i]
            j = i - 1
            while j >= start and kf(a[j]) > kf(cur):
                a[j+1] = a[j]
                j -= 1
            a[j+1] = cur

    # merge runs
    size = RUN
    while size < n:
        for left in range(0, n, 2*size):
            mid = min(left + size, n)
            right = min(left + 2*size, n)

            merged = []
            i, j = left, mid
            while i < mid and j < right:
                if kf(a[i]) <= kf(a[j]):
                    merged.append(a[i]); i += 1
                else:
                    merged.append(a[j]); j += 1

            merged.extend(a[i:mid])
            merged.extend(a[j:right])
            a[left:right] = merged

        size *= 2

    return a
