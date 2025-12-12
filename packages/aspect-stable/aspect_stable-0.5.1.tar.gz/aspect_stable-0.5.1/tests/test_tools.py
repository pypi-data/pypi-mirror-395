import numpy as np


def comp_counter(arr_mask: np.ndarray) -> int:
    return np.sum(~arr_mask[:-1] & arr_mask[1:]) + arr_mask[0]


arr_int = np.array([0, 1, 1, 0, 2, 2, 0])
arr_bool = np.array([False, True, True, False, True, True, False])
arr_float = np.array([0., 0., 1., 1., 0., 0., 2., 2., 0.])
left_corner = np.array([True, False, False, True, True, False, False, True, True, False])
right_corner = np.array([True, False, True, True, False, False, True, True, False, True, True])


print('\nMy method')
print(comp_counter(~(arr_int < 0.001)))
print(comp_counter(~(arr_bool < 0.001)))
print(comp_counter(~(arr_float < 0.001)))
print(comp_counter(~(left_corner < 0.001)))
print(comp_counter(~(right_corner < 0.001)))

print()
arr1 = np.array([0., 1., 0., 2., 0.])       # 0 | 0 | 0   → 3 zero regions
print(comp_counter(~(arr1 < 0.001)))
arr2 = np.array([0., 0., 1., 2., 0., 3.])   # 00 | 0      → 2 zero regions
print(comp_counter(~(arr2 < 0.001)))
arr3 = np.array([1., 2., 3.])               # no zeros    → 0 regions
print(comp_counter(~(arr3 < 0.001)))
