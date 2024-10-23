from twosum import two_sum_quadratic, two_sum_nlogn, two_sum_n

def test_quadratic():
    assert two_sum_quadratic([1, 2, 3, 4, 5], 9) == [3, 4]

def test_nlogn():
    assert two_sum_nlogn([1, 2, 3, 4, 5], 9) == [3, 4]
    
def test_n():
    assert two_sum_n([1, 2, 3, 4, 5], 9) == [3, 4]

    