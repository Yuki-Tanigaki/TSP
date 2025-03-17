import math
import numpy as np
from scipy.spatial.distance import cdist
from typing import List, Tuple

class TSP:
    """
    巡回セールスマン問題 (Traveling Salesman Problem, TSP) を扱うクラス。
    ランダムに都市を配置し、都市間の距離を計算する。
    """

    def __init__(self, num_cities, coord_min, coord_max):
        """
        TSP クラスの初期化。

        :param num_cities: 都市の数
        :param coord_min: 都市座標の最小値
        :param coord_max: 都市座標の最大値
        """
        self.num_cities = num_cities  # 都市の数
        self.coord_min = coord_min  # 都市座標の最小範囲
        self.coord_max = coord_max  # 都市座標の最大範囲
        self.min_distance = (self.coord_max - self.coord_min) / self.num_cities

        self.cities = []  # 都市の座標リスト
        self.start_city = None  # 最初に訪れる都市（ランダムに選択）

        self._initialize()  # 都市の初期化
        self.distance_matrix = self._compute_distance_matrix()  # 距離行列の計算
    
    def _initialize(self):
        """
        都市をランダムに生成し、スタート都市を決定する。
        """
        self._generate_random_cities()  # ランダムな都市の生成
        self.start_city = self.cities.pop(np.random.randint(0, len(self.cities)))  # ランダムにスタート都市を選択し、リストから除外
    
    def _generate_random_cities(self):
        """
        ランダムな都市座標を生成する。
        """
        while len(self.cities) < self.num_cities + 1:
            # 新しい都市をランダムに生成
            new_city = (np.random.randint(self.coord_min, self.coord_max),
                        np.random.randint(self.coord_min, self.coord_max))
            
            # すべての既存都市と距離をチェック
            if all(np.linalg.norm(np.array(new_city) - np.array(city)) >= self.min_distance for city in self.cities):
                self.cities.append(new_city)

    def _compute_distance_matrix(self):
        """
        都市間の距離行列を計算する。
        
        :return: 都市間のユークリッド距離を格納した行列
        """
        cities_array = np.array(self.cities)  # (N, 2) の NumPy 配列に変換
        return cdist(cities_array, cities_array, metric='euclidean')  # ユークリッド距離を計算

    def compute_route_distance(self, route):
        """
        与えられたルートの総距離を計算する。

        :param route: 訪れる都市のインデックスのリスト（例: [0, 2, 1, 3, 0]）
        :return: ルート全体の総距離
        """
        total_distance = sum(
            self.distance_matrix[route[i], route[i + 1]] for i in range(len(route) - 1)
        )
        return total_distance
