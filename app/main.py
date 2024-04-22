from fastapi import FastAPI

from pydantic import BaseModel
from typing import List

from copy import deepcopy
import numpy as np

from app.floyd_warshall import floyd_warshall_initialize
from app.held_karp import held_karp
from app.two_opt import local_search_2_opt
from app.util import distance_calc
from app.make_distance_matrix import make_distance_matrix

import time
import random


class Locations(BaseModel):
    start_location : int
    item_locations : List[int]


# INF 상수는 연결되어있지 않음을 의미.
INF = 10**5

# distance matrix 초기화.
DISTANCE_MATRIX = make_distance_matrix(INF)

# DISTANCE_MATRIX와 floyd-warshall을 이용하여,
# a -> b로의 최단 거리와, 이동 경로 저장.
# 모든 정점으로부터 모든 정점으로까지 최단거리와 최단경로 구하기.
# 즉, 마트 그래프를 완전 그래프로 변환해줌.
SHORTEST_DISTANCES, SHORTEST_PATHS = floyd_warshall_initialize(DISTANCE_MATRIX,INF)


app = FastAPI()


@app.post("/shortest-path")
def find_shortest_path(locations: Locations):
    # 입력 확인.
    print("start_location:", locations.start_location)
    # - 예시
    # - start_location: 0
    print("item_locations:", locations.item_locations)
    # - item_locations: [1, 7, 9]

    # 시작 정점과 끝 정점을 추가해서 TSP를 적용할 list 만들기.
    visit_list = deepcopy(locations.item_locations)
    # 시작 위치.
    start_location = locations.start_location
    visit_list.insert(0,start_location)
    # 끝 정점(계산대) 추가하기. 73번 정점이 계산대.
    visit_list.append(73)
    # - visit_list: [0, 1, 7, 9, 73]

    # TSP 알고리즘을 적용하기 위해, 방문하는 위치들만으로 부분 그래프(sub graph) 만들기.
    # 부분 그래프 만들기.
    l = len(visit_list)
    sub_graph = [[-1 for i in range(l)] for i in range(l)]
    for r in range(l):
        for c in range(l):
            sub_graph[r][c] = SHORTEST_DISTANCES[visit_list[r]][visit_list[c]]
    # - sub_graph:
    # 0.00 13.4 11.4 10.3 5.63
    # 13.4 0.00 4.13 4.17 11.6
    # 11.4 4.13 0.00 2.11 9.65
    # 10.3 4.17 2.11 0.00 8.51
    # 5.63 11.6 9.65 8.51 0.00

    # 최단거리, 최단경로 초기화.
    shortest_distance = -1
    temp_path = []

    # 방문해야할 장소 개수가 14개 미만일 때는 최적 해 algorithm인 held-karp algorithm 적용.
    # 방문해야할 장소 개수가 14개 이상일 때는 heuristic algorithm인 2-opt algorithm 적용.
    if l < 14:
        shortest_distance, temp_path = held_karp(sub_graph,INF)
    else:
        # 입력 형태를 맞추기 위해, sub_graph를 numpy array로 변환해줌.
        sub_graph_np_array = np.array(sub_graph)

        # seed 초기화. seed[0]는 경로를, seed[1]은 거리를 의미.
        seed=[[],[]]

        # path 초기화는 숫자가 낮은 순서로 방문.
        seed[0]=[ i for i in range(len(sub_graph_np_array))]
        seed[1] = distance_calc(sub_graph_np_array,seed)

        temp_path,shortest_distance = local_search_2_opt(sub_graph_np_array,seed,-1,True)

    # - temp_path: [0, 3, 2, 1, 4]
    # temp_path의 요소는 visit_list의 index를 의미.
    # 즉, 방문순서는 0 -> 9 -> 7 -> 1 -> 73

    # 실제 경로로 변환해주기.
    real_path = [start_location]
    temp_path_len = len(temp_path)
    for i in range(temp_path_len-1):
        real_path.extend(SHORTEST_PATHS[visit_list[temp_path[i]]][visit_list[temp_path[i+1]]][1:])

    # 최단 경로 출력
    print("real_path", real_path)
    # - real_path: [0, 71, 70, 69, 68, 58, 55, 52, 48, 45, 
    # 9, 45, 42, 39, 7, 39, 42, 41, 35, 1, 35, 41, 
    # 47, 51, 57, 63, 64, 65, 66, 67, 68, 69, 70, 73]

    # 최단 거리 출력
    print("shortest_distance", (str(shortest_distance) + "m"))
    # - shortest_distance: 28.20m

    return {"path":real_path}

class Test(BaseModel):
    item: int
    count: int


@app.post("/shortest-path/performance-test")
def test_performance(test : Test):
    # 장 볼 물건 개수
    item = test.item
    # 테스트 횟수
    n = test.count

    # 방문할 위치들 n개 랜덤 생성.
    random_locations = []

    # n개의 방문할 리스트 생성
    for _ in range(n):
        random_location = random.sample(range(1,29), item)
        random_locations.append(random_location)

    # 실행 시간 sum
    held_time_sum = 0
    two_time_sum = 0

    # 최단 거리 sum
    held_shortest_distance_sum = 0
    two_shortest_distance_sum = 0

    # 성능 개선율 sum
    improvement_rate_sum = 0
    # 최단 거리 오차율 sum
    distance_error_rate_sum = 0
    
    for locations in random_locations:
        # 시작점과 끝점을 추가해서 TSP를 적용할 list 만들기.
        visit_list = deepcopy(locations)
        visit_list.append(73)

        # TSP 알고리즘을 적용하기 위해, 방문하는 위치들만으로 부분 그래프(sub graph) 만들기.
        # 부분 그래프 만들기.
        l = len(visit_list)
        sub_graph = [[-1 for i in range(l)] for i in range(l)]
        for r in range(l):
            for c in range(l):
                sub_graph[r][c]=SHORTEST_DISTANCES[visit_list[r]][visit_list[c]]

        # 최단거리, 최단경로 초기화.
        held_shortest_distance = -1
        held_temp_path = []
        two_shortest_distance = -1
        two_temp_path = []
        
        # held-karp algorithm 시작 시간.
        held_start_time = time.time()

        # held-karp algorithm.
        held_shortest_distance, held_temp_path = held_karp(sub_graph,INF)

        # 출력
        print("held_temp_path:",held_temp_path)

        # held-karp algorithm 실행 시간.
        held_time = time.time() - held_start_time

        # 2-opt algorithm 시작 시간.
        two_start_time = time.time()
        
        # 2-opt algorithm.
        # 입력 형태를 맞추기 위해, distance matrix인 sub_graph를 numpy array로 변환해줌.
        sub_graph_np_array = np.array(sub_graph)

        # seed 초기화. seed[0]는 경로를, seed[1]은 거리를 의미.
        seed=[[],[]]

        # path 초기화는 숫자가 낮은 순서로 방문.
        seed[0]=[ i for i in range(len(sub_graph_np_array))]
        seed[1] = distance_calc(sub_graph_np_array,seed)

        two_temp_path, two_shortest_distance = local_search_2_opt(sub_graph_np_array,seed,-1,True)

        # 출력
        print("two_temp_path:",two_temp_path)

        # 2-opt 실행 시간.
        two_time = time.time() - two_start_time

        # 시간, 거리 누적하기.
        held_time_sum += held_time
        two_time_sum += two_time

        held_shortest_distance_sum += held_shortest_distance
        two_shortest_distance_sum += two_shortest_distance

        # 성능 개선율, 최단 거리 오차율
        local_improvement_rate = (held_time - two_time) / held_time * 100
        local_distance_error_rate = (two_shortest_distance - held_shortest_distance) / held_shortest_distance * 100

        # 성능 개선율, 최단 거리 오차율 누적
        improvement_rate_sum += local_improvement_rate
        distance_error_rate_sum += local_distance_error_rate



    # 평균 시간.
    held_time_avg = held_time_sum / n
    two_time_avg = two_time_sum / n

    # 평균 거리.
    held_shortest_distance_avg = held_shortest_distance_sum / n
    two_shortest_distance_avg = two_shortest_distance_sum / n

    # 성능 개선율 평균
    improvement_rate_avg = improvement_rate_sum / n
    # 최단 거리 오차율 평균
    distance_error_rate_avg = distance_error_rate_sum / n


    return {"held-karp 실행 시간 평균":str(held_time_avg)+"s",
            "two-opt 실행 시간 평균":str(two_time_avg)+"s",
            "성능 개선율 평균":str(improvement_rate_avg)+"%",
            "held-karp 최단 거리 평균": str(held_shortest_distance_avg)+"m",
            "two-opt 최단 거리 평균":str(two_shortest_distance_avg)+"m",
            "최단 거리 오차율 평균":str(distance_error_rate_avg)+"%"}