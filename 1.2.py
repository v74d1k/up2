def combination_sum_2(candidates, target):
    candidates.sort()
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path.copy())
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i-1]:
                continue
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()

    backtrack(0, [], target)
    return result

print(combination_sum_2([2,5,2,1,2], 5))
print(combination_sum_2([10,1,2,7,6,1,5], 8))
