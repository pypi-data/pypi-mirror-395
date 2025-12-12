
DIC = '0123456789'
SEP = '#'

def encrypt(origin_text: str) -> str:
    """
    将字符串按每个字符的 Unicode 编码拆成数字字符映射后用 SEP 连接。
    等价于原 JS 实现。
    """
    parts = []
    for ch in origin_text:
        code_str = str(ord(ch))
        # 按位映射（此处 DIC[int(d)] 恢复原数字字符，保持与原实现一致）
        mapped = ''.join(DIC[int(d)] for d in code_str)
        parts.append(mapped)
    return SEP.join(parts) + SEP  # 保持末尾有一个分隔符，和原实现一致

def decrypt(cipher_text: str) -> str:
    """
    将加密文本按 SEP 分段，反向把每段的字符通过 DIC.index 还原为数字，再用 chr 恢复字符。
    """
    origin_chars = []
    for item in cipher_text.split(SEP):
        item = item.strip()
        if not item:
            continue
        # 每个字符在 DIC 中找到索引，拼成码点字符串
        num_str = ''.join(str(DIC.index(ch)) for ch in item)
        origin_chars.append(chr(int(num_str)))
    return ''.join(origin_chars)

# 示例
if __name__ == '__main__':
    import json
    payload = {"username": "zhangjiancong", "password": "Zjc123@", "phoneNumber": "18388116550"}
    plain = json.dumps(payload, ensure_ascii=False)
    login_cipher = "123#34#117#115#101#114#110#97#109#101#34#58#34#99#118#112#105#108#111#116#34#44#34#112#97#115#115#119#111#114#100#34#58#34#67#118#112#105#108#111#116#48#49#64#34#125#"
    cipher = encrypt(plain)
    print('cipher:', cipher)
    print('decrypted:', decrypt(login_cipher))
