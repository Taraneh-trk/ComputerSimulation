def mian_morabaee(X, n):
    ans = [X]
    for i in range(n):
        a = str(int(ans[i])**2).zfill(8)  
        ans.append(a[2:6])  
    return [float('0.' + str(i)) for i in ans[1:]]  

def mian_zarbi(X_1, X_2, n):
    ans = [X_1, X_2]
    for i in range(1, n+1):
        a = str(int(ans[i-1]) * int(ans[i])).zfill(8)  
        ans.append(a[2:6])
    return [float('0.' + str(i)) for i in ans[2:]]  

def mazrab_sabet(X, k, n):
    ans = [X]
    for i in range(n):
        a = str(int(ans[i]) * k).zfill(8)
        ans.append(a[2:6])
    return [float('0.' + str(i)) for i in ans[1:]]

def hamneheshti_khati(X, a, c, m, n):
    ans = [X]
    for i in range(n):
        ans.append((a * ans[i] + c) % m)  
    return [i / m for i in ans[1:]]

def hamneheshti_jamee(R_list, m, n):
    ans = R_list[:]
    for i in range(len(R_list), n + len(R_list)):
        ans.append((ans[i-1] + ans[i-len(R_list)]) % m)  
    return [i / m for i in ans[len(R_list):]]  

def main():
    # 1-7
    X = 6393
    n = 3
    print('mian morabaee:', mian_morabaee(X, n))

    # 2-7
    X_1 = 4729
    X_2 = 8583
    n = 3
    print('mian zarbi:', mian_zarbi(X_1, X_2, n))

    # 3-7
    X = 4129
    K = 6787
    n = 3
    print('mazrab sabet:', mazrab_sabet(X, K, n))

    # 4-7
    X = 27
    a = 8
    c = 47
    m = 100
    n = 3
    print('hamneheshti khati:', hamneheshti_khati(X, a, c, m, n))

    # 5-7
    R_list = [0.45, 0.37, 0.89, 0.11, 0.66]
    m = 100
    n = 5  # R_6, R_7, R_8, R_9, R_10
    print('hamneheshti jamee (R_list = [0.45, 0.37, 0.89, 0.11, 0.66]) : ', hamneheshti_jamee(R_list, m, n))
    R_list = [45, 37, 89, 11, 66]
    print('hamneheshti jamee (R_list = [45, 37, 89, 11, 66]) : ', hamneheshti_jamee(R_list, m, n))

    # 6-7
    X = 117
    a = 43
    c = 0
    m = 1000
    n = 4
    print('hamneheshti khati:', hamneheshti_khati(X, a, c, m, n))

if __name__ == '__main__':
    main()
