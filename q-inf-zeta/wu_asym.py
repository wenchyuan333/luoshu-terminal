# q=inf 層：H = L * (1 + δ_Wu)
# δ_Wu 是洛書中心 5 的微擾，用來打破對稱

def H_matrix(L_mod, delta=0.1):
    # L_mod 是 q3 活下來的矩陣
    # 把中心點 5 (在 {1,2} 系裡是 2) 做吳氏微擾
    H = [row[:] for row in L_mod]
    H[1][1] = H[1][1] * (1 + delta) # 中宮 5 不對稱
    return H

# 用你剛剛活下來的 M
M = [[1,1,1],[1,2,1],[1,1,2]]
print("L:", M)
print("H δ=0.1:", H_matrix(M, 0.1))
print("H δ=-0.1:", H_matrix(M, -0.1))
# δ 正負不對稱，就是吳健雄 1957 的那個破缺
