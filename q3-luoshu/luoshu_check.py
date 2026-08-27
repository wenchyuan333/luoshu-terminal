# q=3 洛書層：元素 ∈{1,2}，det!=0 mod3，總和 15
import itertools

def is_luoshu(mat):
    # mat 3x3 list
    flat = [x for row in mat for x in row]
    if 0 in flat: return False, "0 禁止"
    # 九宮格 1-9 變體檢查，傳統洛書和為15，mod3 下就是 0
    if sum(mat[0]) % 3!= 0: return False, "行和失敗"
    det = (mat[0][0]*(mat[1][1]*mat[2][2]-mat[1][2]*mat[2][1])
         - mat[0][1]*(mat[1][0]*mat[2][2]-mat[1][2]*mat[2][0])
         + mat[0][2]*(mat[1][0]*mat[2][1]-mat[1][1]*mat[2][0])) % 3
    if det == 0: return False, f"不可逆 det={det}"
    return True, f"可逆 det={det}"

# 經典洛書
L = [[4,9,2],[3,5,7],[8,1,6]]
# 轉成 mod3 的 {1,2} 表示，1->1, 2->2, 0用2代替的變體
L_mod = [[(x%3 if x%3!=0 else 2) for x in row] for row in L]
print("L_mod:", L_mod, is_luoshu(L_mod))
