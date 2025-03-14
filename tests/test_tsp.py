import unittest
import numpy as np
from src.tsp import TSP  # tsp.py をインポート

class TestTSP(unittest.TestCase):

    def setUp(self):
        """ テストごとに新しいTSPインスタンスを作成 """
        self.num_cities = 5
        self.coord_min = 0
        self.coord_max = 100
        self.rng = np.random.default_rng(42)  # 乱数を固定
        self.tsp = TSP(self.num_cities, self.coord_min, self.coord_max)

    def test_city_count(self):
        """ 指定された数の都市が生成されているか """
        self.assertEqual(len(self.tsp.cities), self.num_cities)

    def test_distance_matrix_size(self):
        """ 距離行列のサイズが正しいか """
        self.assertEqual(self.tsp.distance_matrix.shape, (self.num_cities, self.num_cities))

    def test_route_distance_calculation(self):
        """ ルートの距離計算が正しいか確認 """
        if self.num_cities >= 3:
            route = [0, 1, 2, 0]  # 3都市を巡回
            distance = self.tsp.compute_route_distance(route)
            self.assertIsInstance(distance, float)  # 返り値が float であることを確認

    def test_non_negative_distances(self):
        """ 距離行列の全要素が非負であることを確認 """
        self.assertTrue(np.all(self.tsp.distance_matrix >= 0))

if __name__ == '__main__':
    unittest.main()
