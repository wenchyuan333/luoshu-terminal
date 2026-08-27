# 5bit 三元洛書碼
# 0b00000 禁止
# 0b00001-0b11111 對應 U+E000 私用區 31 字

def encode_5bit(val: int) -> str:
    if val == 0: raise ValueError("0 禁止")
    return chr(0xE000 + val)

def decode_5bit(ch: str) -> int:
    return ord(ch) - 0xE000

if __name__ == "__main__":
    for i in [1,2,5,15,31]:
        c = encode_5bit(i)
        print(f"{i:05b} -> U+{ord(c):04X} -> {decode_5bit(c)}")
