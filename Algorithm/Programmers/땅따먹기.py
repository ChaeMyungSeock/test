def solution(land):
    answer = []
    for i in range(len(land)-1):
        land[i+1][0] += max(land[i][1],land[i][2],land[i][3])
        land[i+1][1] += max(land[i][0],land[i][2],land[i][3])
        land[i+1][2] += max(land[i][1],land[i][0],land[i][3])
        land[i+1][3] += max(land[i][1],land[i][2],land[i][0])
# 각각의 다음 타일에서 그 전 타일의 최댓값을 각각 더해 나간다
# 그러면 마지막 타일에서는 각각의 시작타일에서의 최댓값들이 나옴
# 그 중에서 최대값을 뽑아내면 된다   
        answer = max(land[-1])


    # [실행] 버튼을 누르면 출력 값을 볼 수 있습니다.

    return answer

land = [[1,2,3,5],[5,6,7,8],[4,3,2,1]]

print(solution(land))


