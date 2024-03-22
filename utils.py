def most_common_digit(arr):
    counts = {}
    for num in arr:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1

    most_common = max(counts, key=counts.get)
    return most_common