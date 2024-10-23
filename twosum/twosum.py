def two_sum_quadratic(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return None

def two_sum_nlogn(nums, target):
    # Criar uma lista de (valor, índice) para manter a referência do índice original
    nums_with_index = [(num, idx) for idx, num in enumerate(nums)]
    # Ordenar com base nos valores
    nums_with_index.sort()
    
    # Usar dois ponteiros para procurar a combinação
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums_with_index[left][0] + nums_with_index[right][0]
        if current_sum == target:
            # Retornar os índices originais
            return [nums_with_index[left][1], nums_with_index[right][1]]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return None

def two_sum_n(nums, target):
    num_map = {}  # Initialize the hash map
    for index, num in enumerate(nums):
        complement = target - num  # Calculate the complement
        if complement in num_map:  # Check if the complement is already in the map
            return [num_map[complement], index]  # Return the indices of the complement and the current number
        num_map[num] = index  # Store the current number and its index in the map
    return None
