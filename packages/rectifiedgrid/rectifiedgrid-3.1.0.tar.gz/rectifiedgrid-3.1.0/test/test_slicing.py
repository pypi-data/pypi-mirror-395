from rectifiedgrid.demo import get_demo_data

# slice is implemented by rioxarry
# class TestSlicing(object):
#     def test_left_top(self):
#         grid = get_demo_data()
#         from matplotlib import pyplot as plt
#         grid.rg.plotmap()
#         plt.show()
#         grid.plot()
#         plt.show()
#         slice_xy(minx, miny, maxx, maxy)
#         grid_s = grid[:3, :3]
#         assert grid_s.bounds == (4500000.0, 1530000.0, 4530000.0, 1560000.0)
#
#     def test_center(self):
#         bounds = (4530000.0, 1510000.0, 4550000.0, 1530000.0)
#         grid = get_demo_data()
#         grid_s = grid[3:5, 3:5]
#         assert grid_s.sum() == 1
#         assert grid_s.bounds == bounds
#         # test copy after sliding
#         _grid = grid_s.copy()
#         _grid = _grid.copy()
#         assert _grid.bounds == bounds
#
#         grid.fill(1)
#         _grid.reproject(grid)
#
#     def test_crop(self):
#         bounds = (4530000.0, 1510000.0, 4550000.0, 1530000.0)
#         grid = get_demo_data()
#         grid.fill(0)
#         grid[3:5, 3:5] = 1
#         cropped = grid.crop(0)
#         assert cropped.bounds == bounds
