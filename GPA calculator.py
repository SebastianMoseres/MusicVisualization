import math
fall_2021 = [4.0, 4.0, 3.7, 3.3]
winter_2022 = [3.7, 3.7, 4.0, 3.3]
fall_2022 = [3.7, 4.0, 4.0, 4.0, 4.0]
winter_2023 = [4.0, 3.7, 4.0, 4.0, 4.0]
fall_2023 = [4.0, 4.0, 4.0, 3.3, 3.7]
winter_2024 = [4.0, 3.3, 4.0, 4.0, 4.0]
fall_2024 = [4.0, 4.0, 4.0, 3.7, 3.3]

all_terms = fall_2021 + winter_2022 + fall_2022 + winter_2023 + fall_2023 + winter_2024 + fall_2024

GPA = sum(all_terms)/len(all_terms)

print(f"sum: {sum(all_terms)},len: {len(all_terms)}")
print (f"GPA is: {GPA}")