class Kuznyechik:
    """
    Реализация алгоритма шифрования "Кузнечик" (ГОСТ 34.12-2015)
    """
    
    # S-блок (нелинейное преобразование)
    PI = [
        0xFC, 0xEE, 0xDD, 0x11, 0xCF, 0x6E, 0x31, 0x16, 0xFB, 0xC4, 0xFA, 0xDA, 0x23, 0xC5, 0x04, 0x4D,
        0xE9, 0x77, 0xF0, 0xDB, 0x93, 0x2E, 0x99, 0xBA, 0x17, 0x36, 0xF1, 0xBB, 0x14, 0xCD, 0x5F, 0xC1,
        0xF9, 0x18, 0x65, 0x5A, 0xE2, 0x5C, 0xEF, 0x21, 0x81, 0x1C, 0x3C, 0x42, 0x8B, 0x01, 0x8E, 0x4F,
        0x05, 0x84, 0x02, 0xAE, 0xE3, 0x6A, 0x8F, 0xA0, 0x06, 0x0B, 0xED, 0x98, 0x7F, 0xD4, 0xD3, 0x1F,
        0xEB, 0x34, 0x2C, 0x51, 0xEA, 0xC8, 0x48, 0xAB, 0xF2, 0x2A, 0x68, 0xA2, 0xFD, 0x3A, 0xCE, 0xCC,
        0xB5, 0x70, 0x0E, 0x56, 0x08, 0x0C, 0x76, 0x12, 0xBF, 0x72, 0x13, 0x47, 0x9C, 0xB7, 0x5D, 0x87,
        0x15, 0xA1, 0x96, 0x29, 0x10, 0x7B, 0x9A, 0xC7, 0xF3, 0x91, 0x78, 0x6F, 0x9D, 0x9E, 0xB2, 0xB1,
        0x32, 0x75, 0x19, 0x3D, 0xFF, 0x35, 0x8A, 0x7E, 0x6D, 0x54, 0xC6, 0x80, 0xC3, 0xBD, 0x0D, 0x57,
        0xDF, 0xF5, 0x24, 0xA9, 0x3E, 0xA8, 0x43, 0xC9, 0xD7, 0x79, 0xD6, 0xF6, 0x7C, 0x22, 0xB9, 0x03,
        0xE0, 0x0F, 0xEC, 0xDE, 0x7A, 0x94, 0xB0, 0xBC, 0xDC, 0xE8, 0x28, 0x50, 0x4E, 0x33, 0x0A, 0x4A,
        0xA7, 0x97, 0x60, 0x73, 0x1E, 0x00, 0x62, 0x44, 0x1A, 0xB8, 0x38, 0x82, 0x64, 0x9F, 0x26, 0x41,
        0xAD, 0x45, 0x46, 0x92, 0x27, 0x5E, 0x55, 0x2F, 0x8C, 0xA3, 0xA5, 0x7D, 0x69, 0xD5, 0x95, 0x3B,
        0x07, 0x58, 0xB3, 0x40, 0x86, 0xAC, 0x1D, 0xF7, 0x30, 0x37, 0x6B, 0xE4, 0x88, 0xD9, 0xE7, 0x89,
        0xE1, 0x1B, 0x83, 0x49, 0x4C, 0x3F, 0xF8, 0xFE, 0x8D, 0x53, 0xAA, 0x90, 0xCA, 0xD8, 0x85, 0x61,
        0x20, 0x71, 0x67, 0xA4, 0x2D, 0x2B, 0x09, 0x5B, 0xCB, 0x9B, 0x25, 0xD0, 0xBE, 0xE5, 0x6C, 0x52,
        0x59, 0xA6, 0x74, 0xD2, 0xE6, 0xF4, 0xB4, 0xC0, 0xD1, 0x66, 0xAF, 0xC2, 0x39, 0x4B, 0x63, 0xB6
    ]
    
    # Обратный S-блок
    PI_INV = [0] * 256
    
    # Матрица линейного преобразования R
    R = [
        0x01, 0x01, 0x05, 0x01, 0x08, 0x06, 0x07, 0x04,
        0x0E, 0x09, 0x03, 0x02, 0x0F, 0x0C, 0x0A, 0x0D
    ]
    
    # Константы для развертки ключей
    C = []
    
    def __init__(self, key: bytes):
        """Инициализация шифра с заданным ключом"""
        if len(key) != 32:
            raise ValueError("Ключ должен быть 32 байта")
        
        # Инициализация обратного S-блока
        for i, val in enumerate(self.PI):
            self.PI_INV[val] = i
        
        # Предвычисление констант
        self._generate_constants()
        
        # Развертка ключей
        self.round_keys = self._expand_key(key)
    
    def _generate_constants(self):
        """Генерация констант для развертки ключей"""
        self.C = []
        for i in range(1, 33):
            const = [0] * 16
            const[0] = i
            self.C.append(const)
    
    def _expand_key(self, key: bytes) -> list:
        """
        Развертка ключей для 10 раундов
        """
        round_keys = []
        
        # Начальные ключи K1 и K2
        k1 = list(key[:16])
        k2 = list(key[16:])
        round_keys.extend([k1, k2])
        
        # Генерация остальных ключей
        for i in range(4):
            for j in range(8):
                # Вычисление очередного ключа
                k1, k2 = self._feistel_step(k1, k2, self.C[8*i + j])
                round_keys.extend([k1, k2])
        
        return round_keys
    
    def _feistel_step(self, k1: list, k2: list, const: list) -> tuple:
        """
        Один шаг сети Фейстеля для развертки ключей
        """
        # Копируем k1
        new_k1 = k2.copy()
        
        # Применяем преобразование F к k1 с константой
        k1_transformed = self._f(k1, const)
        
        # XOR с k2
        new_k2 = [k1_transformed[i] ^ k2[i] for i in range(16)]
        
        return new_k1, new_k2
    
    def _f(self, state: list, round_key: list) -> list:
        """
        Преобразование F (S затем L)
        """
        # S-преобразование
        after_s = [self.PI[b] for b in state]
        
        # L-преобразование (линейное)
        after_l = self._l(after_s)
        
        # XOR с раундовым ключом
        return [after_l[i] ^ round_key[i] for i in range(16)]
    
    def _l(self, state: list) -> list:
        """
        Линейное преобразование L
        """
        result = state.copy()
        
        # 16 итераций линейного преобразования
        for _ in range(16):
            # Вычисление нового байта
            new_byte = 0
            for j in range(16):
                new_byte ^= mul(result[j], self.R[j])
            
            # Сдвиг
            result = [new_byte] + result[:-1]
        
        return result
    
    def encrypt_block(self, block: bytes) -> bytes:
        """
        Шифрование одного блока (16 байт)
        """
        if len(block) != 16:
            raise ValueError("Блок должен быть 16 байт")
        
        state = list(block)
        
        # 9 раундов с ключами и преобразованием F
        for i in range(9):
            # XOR с раундовым ключом
            xored = [state[j] ^ self.round_keys[i][j] for j in range(16)]
            # Преобразование F
            state = self._f(xored, self.round_keys[i+1])
        
        # Последний XOR
        state = [state[j] ^ self.round_keys[9][j] for j in range(16)]
        
        return bytes(state)
    
    def decrypt_block(self, block: bytes) -> bytes:
        """
        Расшифрование одного блока (16 байт)
        """
        if len(block) != 16:
            raise ValueError("Блок должен быть 16 байт")
        
        state = list(block)
        
        # Начинаем с последнего XOR
        state = [state[j] ^ self.round_keys[9][j] for j in range(16)]
        
        # 9 обратных раундов
        for i in range(8, -1, -1):
            # Обратное преобразование F
            state = self._f_inv(state, self.round_keys[i+1])
            # XOR с ключом
            state = [state[j] ^ self.round_keys[i][j] for j in range(16)]
        
        return bytes(state)
    
    def _f_inv(self, state: list, round_key: list) -> list:
        """
        Обратное преобразование F
        """
        # Сначала применяем L_inv, затем S_inv
        after_l_inv = self._l_inv(state)
        return [self.PI_INV[b] for b in after_l_inv]
    
    def _l_inv(self, state: list) -> list:
        """
        Обратное линейное преобразование L
        """
        result = state.copy()
        
        for _ in range(16):
            # Сдвиг в обратную сторону
            result = result[1:] + [result[0]]
            
            # Вычисление нового байта для позиции 15
            new_byte = 0
            for j in range(16):
                new_byte ^= mul(result[j], self.R[j])
            
            result[15] = new_byte
        
        return result


def test_kuznyechik():
    """Тестирование реализации"""
    
    # Тестовый вектор из стандарта
    key = bytes.fromhex("8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef")
    plaintext = bytes.fromhex("1122334455667700ffeeddccbbaa9988")
    ciphertext = bytes.fromhex("7f679d90bebc24305a468d42b9d4edcd")
    
    cipher = Kuznyechik(key)
    encrypted = cipher.encrypt_block(plaintext)
    decrypted = cipher.decrypt_block(encrypted)
    
    print(f"Ключ: {key.hex()}")
    print(f"Открытый текст: {plaintext.hex()}")
    print(f"Ожидаемый шифротекст: {ciphertext.hex()}")
    print(f"Полученный шифротекст: {encrypted.hex()}")
    print(f"Расшифровано: {decrypted.hex()}")
    print(f"Шифрование верно: {encrypted == ciphertext}")
    print(f"Расшифрование верно: {decrypted == plaintext}")


if __name__ == "__main__":
    test_kuznyechik()