# ------------- Sorting Algorithms ---------------


def bubble_sort(arr, key=lambda x: x):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if key(arr[j]) > key(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr


def insertion_sort(arr, key=lambda x: x):
    for i in range(1, len(arr)):
        key_item = arr[i]
        key_val = key(key_item)
        j = i - 1
        while j >= 0 and key(arr[j]) > key_val:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr
        arr[j + 1] = key_item
        yield arr


def selection_sort(arr, key=lambda x: x):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if key(arr[j]) < key(arr[min_idx]):
                min_idx = j
                yield arr
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr


def quick_sort(arr, key=lambda x: x):
    def _qs(lo, hi):
        if lo >= hi:
            return

        pivot = arr[(lo + hi) // 2]
        i, j = lo, hi

        while i <= j:
            while key(arr[i]) < key(pivot):
                i += 1
            while key(arr[j]) > key(pivot):
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                yield arr
                i += 1
                j -= 1

        if lo < j:
            yield from _qs(lo, j)
        if i < hi:
            yield from _qs(i, hi)

    if len(arr) <= 1:
        return

    yield from _qs(0, len(arr) - 1)


def merge_sort(arr, key=lambda x: x):
    n = len(arr)
    if n <= 1:
        return

    tmp = arr[:]

    def _ms(left, right):
        if right - left <= 1:
            return

        mid = (left + right) // 2
        yield from _ms(left, mid)
        yield from _ms(mid, right)

        i, j = left, mid
        k = left

        while i < mid and j < right:
            if key(arr[i]) <= key(arr[j]):
                tmp[k] = arr[i]
                i += 1
            else:
                tmp[k] = arr[j]
                j += 1
            k += 1

        while i < mid:
            tmp[k] = arr[i]
            i += 1
            k += 1

        while j < right:
            tmp[k] = arr[j]
            j += 1
            k += 1

        for k in range(left, right):
            arr[k] = tmp[k]
            yield arr

    yield from _ms(0, n)


def heap_sort(arr, key=lambda x: x):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and key(arr[l]) > key(arr[largest]):
            largest = l

        if r < n and key(arr[r]) > key(arr[largest]):
            largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield from heapify(arr, n, largest)

    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr
        yield from heapify(arr, i, 0)


def radix_sort(arr, key=lambda x: x):
    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = (key(arr[i]) // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = (key(arr[i]) // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        for i in range(n):
            arr[i] = output[i]
            yield arr

    max1 = max(arr, key=key)
    exp = 1
    while key(max1) // exp > 0:
        yield from counting_sort(arr, exp)
        exp *= 10


# -------------- Connectors ------------------


SORT_ALGORITHMS = {
    "Bubble": bubble_sort,
    "Insertion": insertion_sort,
    "Selection": selection_sort,
    "Quick": quick_sort,
    "Merge": merge_sort,
    "Heap": heap_sort,
    "Radix": radix_sort,
}

ALGO_DESCRIPTIONS = {
    "Bubble": "Bubble Sort: Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. O(N^2)",
    "Insertion": "Insertion Sort: Builds the final sorted array one item at a time. O(N^2)",
    "Selection": "Selection Sort: Divides the input list into two parts: a sorted and an unsorted part. O(N^2)",
    "Quick": "Quick Sort: Picks an element as a pivot and partitions the array around the pivot. O(N log N)",
    "Merge": "Merge Sort: Divides the array into halves, sorts them and then merges them back together. O(N log N)",
    "Heap": "Heap Sort: Uses a binary heap data structure to sort elements. O(N log N)",
    "Radix": "Radix Sort: Non-comparative integer sorting algorithm that sorts data with integer keys by grouping keys by individual digits. O(Nk)",
}


def get_sort_generator(name, arr, key=lambda x: x):
    if name not in SORT_ALGORITHMS:
        raise ValueError(f"Sorting algorithm '{name}' not found.")

    sort_func = SORT_ALGORITHMS[name]
    gen = sort_func(arr, key=key)

    for state in gen:
        if state is not arr:
            arr[:] = state
        yield arr
