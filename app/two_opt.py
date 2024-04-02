############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Lesson: Local Search-2-opt
 
# GitHub Repository: <https://github.com/Valdecy>

############################################################################

# Required Libraries
import copy
from app.util import distance_calc

############################################################################

# Function: 2_opt
def local_search_2_opt(distance_matrix, city_tour, recursive_seeding = -1, verbose = True):
    if (recursive_seeding < 0):
        count = -2
    else:
        count = 0
    city_list = copy.deepcopy(city_tour)
    distance  = city_list[1]*2
    iteration = 0
    while (count < recursive_seeding):
        if (verbose == True):
            print('Iteration = ', iteration, 'Distance = ', round(city_list[1], 2))  
        best_route = copy.deepcopy(city_list)
        seed       = copy.deepcopy(city_list)
        
        # 시작 정점과 끝 정점을 고정한 채, 사이에서 2개의 정점을 골라 경로를 뒤집은 후 개선이 있는지 확인하는 코드.
        # 레퍼런스 코드
        # for i in range(0, len(city_list[0]) - 2):
        # i를 1에서 시작함으로써 시작 위치를 고정.         
        for i in range(1, len(city_list[0]) - 2):
            # 끝 정점(계산대)은 고정하기 위해 범위를 len - 1까지.
            for j in range(i+1, len(city_list[0]) - 1):
                best_route[0][i:j+1] = list(reversed(best_route[0][i:j+1]))
                # 레퍼런스 코드는 0 -> 1 -> 2 -> 3 -> 0 과 같은 순환 경로를 넣었지만,
                # 본 프로젝트에서는 초기 경로를 0 -> 1 -> 2 -> 3 과 같이 초기화하였기때문에, 아래 코드가 필요 없음.
                # best_route[0][-1]    = best_route[0][0]     
                best_route[1]        = distance_calc(distance_matrix, best_route)                    
                if (city_list[1] > best_route[1]):
                    city_list = copy.deepcopy(best_route)         
                best_route = copy.deepcopy(seed)
        count     = count + 1
        iteration = iteration + 1  
        if (distance > city_list[1] and recursive_seeding < 0):
             distance          = city_list[1]
             count             = -2
             recursive_seeding = -1
        elif(city_list[1] >= distance and recursive_seeding < 0):
            count              = -1
            recursive_seeding  = -2
    return city_list[0], city_list[1]

############################################################################