############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Lesson: pyCombinatorial - Util
 
# GitHub Repository: <https://github.com/Valdecy>

############################################################################

# Required Libraries
import numpy  as np

############################################################################

# Function: Tour Distance
# 경로 거리 계산.
# 경로가 0 -> 1 -> 2 -> 3 이라면, 0 -> 1, 1 -> 2, 2 -> 3 거리를 더하는 코드.
def distance_calc(distance_matrix, city_tour):
    distance = 0
    for k in range(0, len(city_tour[0])-1):
        m        = k + 1
        # 기존 코드
        # distance = distance + distance_matrix[city_tour[0][k]-1, city_tour[0][m]-1]
        # 레퍼런스 코드와 다르게, 노드 번호와 distance_matrix의 인덱스 번호가 맞기 때문에 -1을 해줄 필요 없음.
        distance = distance + distance_matrix[city_tour[0][k], city_tour[0][m]]    
    return distance

# Function: Build Distance Matrix
def build_distance_matrix(coordinates):
   a = coordinates
   b = a.reshape(np.prod(a.shape[:-1]), 1, a.shape[-1])
   return np.sqrt(np.einsum('ijk,ijk->ij',  b - a,  b - a)).squeeze()

############################################################################
