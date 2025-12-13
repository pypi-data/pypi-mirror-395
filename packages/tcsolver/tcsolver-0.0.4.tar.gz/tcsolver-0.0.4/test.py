
import tcsolver.image_utility as imageutil

bg_image_name = "test_cheetah.png"
distance = imageutil.calc_gap_distance(bg_image_name)
print("test_cheetah.distance:" + str(distance))

bg_image_name = "test_wheat.png"
distance = imageutil.calc_gap_distance(bg_image_name)
print("test_wheat.distance:" + str(distance))
