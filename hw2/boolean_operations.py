def list_a_and_not_list_b(a, b):
    results = []
    idx_a = 0
    idx_b = 0
    len_a = len(a)
    len_b = len(b)
    while idx_a < len_a and idx_b < len_b:
        if a[idx_a] < b[idx_b]:
            results.append(a[idx_a])
            idx_a += 1
        elif b[idx_b] < a[idx_a]:
            idx_b += 1
        else:
            idx_a += 1
            idx_b += 1

    results.extend(a[idx_a:])
    return results


def list_a_and_list_b(a, b):
    results = []
    idx_a = 0
    idx_b = 0
    len_a = len(a)
    len_b = len(b)
    while idx_a < len_a and idx_b < len_b:
        if a[idx_a] == b[idx_b]:
            results.append(a[idx_a])
            idx_a += 1
            idx_b += 1
        elif a[idx_a] < b[idx_b]:
            idx_a += 1
        else:
            idx_b += 1
    return results


def list_a_or_list_b(a, b):
    results = []
    idx_a = 0
    idx_b = 0
    len_a = len(a)
    len_b = len(b)
    while idx_a < len_a and idx_b < len_b:
        if a[idx_a] == b[idx_b]:
            results.append(a[idx_a])
            idx_a += 1
            idx_b += 1
        elif a[idx_a] < b[idx_b]:
            results.append(a[idx_a])
            idx_a += 1
        else:
            results.append(b[idx_b])
            idx_b += 1

    results.extend(a[idx_a:])
    results.extend(b[idx_b:])
    return results


def ll_a_and_ll_b(a, b):
    results = []
    while a and b:
        if a.val() == b.val():
            results.append(a.val())
            a = a.next()
            b = b.next()
        elif a.val() < b.val():
            while a and a.val() < b.val():
                skip_val = a.skip_val()
                if skip_val and skip_val <= b.val():
                    a = a.skip()
                else:
                    a = a.next()
        else:
            while b and b.val() < a.val():
                skip_val = b.skip_val()
                if skip_val and skip_val <= a.val():
                    b = b.skip()
                else:
                    b = b.next()
    return results


def ll_a_or_ll_b(a, b):
    results = []
    while a and b:
        if a.val() == b.val():
            results.append(a.val())
            a = a.next()
            b = b.next()
        elif a.val() < b.val():
            results.append(a.val())
            a = a.next()
        else:
            results.append(b.val())
            b = b.next()

    while a:
        results.append(a.val())
        a = a.next()

    while b:
        results.append(b.val())
        b = b.next()

    return results


def ll_a_and_list_b(a, b):
    results = []
    idx_b = 0
    len_b = len(b)
    while a and idx_b < len_b:
        if a.val() == b[idx_b]:
            results.append(a.val())
            a = a.next()
            idx_b += 1
        elif a.val() < b[idx_b]:
            while a and a.val() < b[idx_b]:
                skip_val = a.skip_val()
                if skip_val and skip_val <= b[idx_b]:
                    a = a.skip()
                else:
                    a = a.next()
        else:
            idx_b += 1
    return results


def ll_a_or_list_b(a, b):
    results = []
    idx_b = 0
    len_b = len(b)
    while a and idx_b < len_b:
        if a.val() == b[idx_b]:
            results.append(a.val())
            a = a.next()
            idx_b += 1
        elif a.val() < b[idx_b]:
            results.append(a.val())
            a = a.next()
        else:
            results.append(b[idx_b])
            idx_b += 1

    while a:
        results.append(a.val())
        a = a.next()

    results.extend(b[idx_b:])
    return results
