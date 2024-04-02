import os
import pandas as pd
from app.util import build_distance_matrix

# edge 생성.
def make_edge(distance_matrix,x,y,distances):
    distance_matrix[x][y]=distances[x][y]
    distance_matrix[y][x]=distances[x][y]

def make_distance_matrix(INF):
    # 현재 작업 중인 디렉토리를 확인합니다.
    cwd = os.getcwd()

    # 파일 경로를 지정합니다.
    file_path = os.path.join(cwd, 'app/map_coordinates.txt')

    # map의 안내할 node 좌표.
    coordinates = pd.read_csv(file_path, sep = ' ')
    coordinates = coordinates.values

    # 각 노드간의 거리.
    distances = build_distance_matrix(coordinates)

    # 노드 총 개수
    node_num = len(coordinates)

    # 모두 다 연결되어 있지 않는 걸로 초기화.
    distance_matrix = [[INF for j in range(node_num)] for i in range(node_num)]

    # 자기 자신과의 거리는 0
    for i in range(node_num):
        distance_matrix[i][i]=0

    # distances를 이용하여 edge 양방향 생성
    make_edge(distance_matrix,0,71,distances)
    make_edge(distance_matrix,1,35,distances)
    make_edge(distance_matrix,2,36,distances)
    make_edge(distance_matrix,3,47,distances)
    make_edge(distance_matrix,4,48,distances)
    make_edge(distance_matrix,5,57,distances)
    make_edge(distance_matrix,6,58,distances)
    make_edge(distance_matrix,7,39,distances)
    make_edge(distance_matrix,8,40,distances)
    make_edge(distance_matrix,9,45,distances)
    make_edge(distance_matrix,10,46,distances)
    make_edge(distance_matrix,11,52,distances)
    make_edge(distance_matrix,12,53,distances)
    make_edge(distance_matrix,13,55,distances)
    make_edge(distance_matrix,14,56,distances)
    make_edge(distance_matrix,15,37,distances)
    make_edge(distance_matrix,16,38,distances)
    make_edge(distance_matrix,17,49,distances)
    make_edge(distance_matrix,18,50,distances)
    make_edge(distance_matrix,19,59,distances)
    make_edge(distance_matrix,20,60,distances)
    make_edge(distance_matrix,21,30,distances)
    make_edge(distance_matrix,22,31,distances)
    make_edge(distance_matrix,23,61,distances)
    make_edge(distance_matrix,24,62,distances)
    make_edge(distance_matrix,25,64,distances)
    make_edge(distance_matrix,26,65,distances)
    make_edge(distance_matrix,27,66,distances)
    make_edge(distance_matrix,28,67,distances)
    make_edge(distance_matrix,29,30,distances)
    make_edge(distance_matrix,29,35,distances)
    make_edge(distance_matrix,30,31,distances)
    make_edge(distance_matrix,31,32,distances)
    make_edge(distance_matrix,32,33,distances)
    make_edge(distance_matrix,32,36,distances)
    make_edge(distance_matrix,33,34,distances)
    make_edge(distance_matrix,33,37,distances)
    make_edge(distance_matrix,34,38,distances)
    make_edge(distance_matrix,35,41,distances)
    make_edge(distance_matrix,36,39,distances)
    make_edge(distance_matrix,37,40,distances)
    make_edge(distance_matrix,38,44,distances)
    make_edge(distance_matrix,39,42,distances)
    make_edge(distance_matrix,40,43,distances)
    make_edge(distance_matrix,41,42,distances)
    make_edge(distance_matrix,41,47,distances)
    make_edge(distance_matrix,42,45,distances)
    make_edge(distance_matrix,43,44,distances)
    make_edge(distance_matrix,43,46,distances)
    make_edge(distance_matrix,44,50,distances)
    make_edge(distance_matrix,45,48,distances)
    make_edge(distance_matrix,46,49,distances)
    make_edge(distance_matrix,47,51,distances)
    make_edge(distance_matrix,48,52,distances)
    make_edge(distance_matrix,49,53,distances)
    make_edge(distance_matrix,50,54,distances)
    make_edge(distance_matrix,51,52,distances)
    make_edge(distance_matrix,51,57,distances)
    make_edge(distance_matrix,52,55,distances)
    make_edge(distance_matrix,53,54,distances)
    make_edge(distance_matrix,53,56,distances)
    make_edge(distance_matrix,54,60,distances)
    make_edge(distance_matrix,55,58,distances)
    make_edge(distance_matrix,56,59,distances)
    make_edge(distance_matrix,57,63,distances)
    make_edge(distance_matrix,58,68,distances)
    make_edge(distance_matrix,59,69,distances)
    make_edge(distance_matrix,60,72,distances)
    make_edge(distance_matrix,61,62,distances)
    make_edge(distance_matrix,62,63,distances)
    make_edge(distance_matrix,63,64,distances)
    make_edge(distance_matrix,64,65,distances)
    make_edge(distance_matrix,65,66,distances)
    make_edge(distance_matrix,66,67,distances)
    make_edge(distance_matrix,67,68,distances)
    make_edge(distance_matrix,68,69,distances)
    make_edge(distance_matrix,69,70,distances)
    make_edge(distance_matrix,70,71,distances)
    make_edge(distance_matrix,70,73,distances)
    make_edge(distance_matrix,71,72,distances)

    return distance_matrix