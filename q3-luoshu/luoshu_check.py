# q=3 洛書層 v2：只驗證 0禁止 + 可逆 det!=0，不驗和
def det3(mat):
    return (mat[0][0]*(mat[1][1]*mat[2][2]-mat[1][2]*mat[2][1])
          - mat[0][1]*(mat[1][0]*mat[2][2]-mat[1][2]*mat[2][0])
          + mat[0][2]*(mat[1][0]*mat[2][1]-mat[1][1]*mat[2][0])) % 3

def is_luoshu(mat):
    flat=[x for r in mat for x in r]
    if 0 in flat: return False, "0 禁止"
    d=det3(mat)
    if d==0: return False, f"不可逆 det={d}"
    return True, f"可逆 det={d} - 洛書存活"

# 用純 {1,2} 的矩陣，才是你在 q=1 5bit 長出來的本體
M = [[1,1,1],[1,2,1],[1,1,2]] # 中宮 2
print(M, is_luoshu(M))

M2 = [[1,2,2],[2,2,1],[2,1,2]] # 你剛剛 L_mod
print(M2, is_luoshu(M2))
