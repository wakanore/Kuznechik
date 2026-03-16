def mul(a: int, b: int, mod: int = 0x1C3) -> int:
    """
    Умножение в поле GF(2^8)
    
    Args:
        a, b: байты для умножения (0-255)
        mod: неприводимый многочлен (по умолчанию 0x1C3 для Кузнечика)
    
    Returns:
        Результат умножения в поле GF(2^8)
    """
    result = 0
    # Умножаем, пока b > 0
    while b > 0:
        # Если младший бит b установлен, добавляем a к результату
        if b & 1:
            result ^= a
        
        # Удваиваем a (умножаем на x) в поле GF(2^8)
        a <<= 1
        
        # Если произошел перенос за пределы байта, редуцируем по модулю
        if a & 0x100:
            a ^= mod
        
        # Сдвигаем b вправо
        b >>= 1
    
    return result & 0xFF  # Ограничиваем до байта


def build_multiplication_table(mod: int = 0x1C3) -> list:
    """
    Построение таблицы умножения для поля GF(2^8)
    
    Returns:
        Матрица 256x256 с результатами умножения
    """
    table = [[0] * 256 for _ in range(256)]
    
    for i in range(256):
        for j in range(256):
            table[i][j] = mul(i, j, mod)
    
    return table


def print_multiplication_table(table: list, size: int = 16):
    """Вывод части таблицы умножения для наглядности"""
    print("Таблица умножения в GF(2^8) (первые 16x16 элементов):")
    print("    " + " ".join(f"{i:2X}" for i in range(size)))
    
    for i in range(size):
        row = f"{i:2X}: " + " ".join(f"{table[i][j]:2X}" for j in range(size))
        print(row)


# Тестирование умножения
if __name__ == "__main__":
    # Проверка умножения
    a, b = 0x57, 0x13
    result = mul(a, b)
    print(f"0x57 * 0x13 = 0x{result:02X}")
    
    # Построение и вывод таблицы
    table = build_multiplication_table()
    print_multiplication_table(table)