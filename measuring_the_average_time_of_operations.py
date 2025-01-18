# Основний код (программа)
class GF2Field: 
    def __init__(self, m, irreducible_poly): 
        self.m = m 
        self.irreducible_poly = irreducible_poly 

    # Додавання двох елементів у полі 
    def add(self, a, b): 
        return a ^ b 

    # Множення двох елементів у полі 
    def multiply(self, a, b): 
        c = 0 
        t = a 
        for i in range(b.bit_length()): 
            if (b >> i) & 1: 
                c ^= t 
            t <<= 1 
        return self.mod(c) 

    # Редукція елемента за незвідним поліномом 
    def mod(self, c): 
        t = c 
        while t.bit_length() >= self.irreducible_poly.bit_length(): 
            shift = t.bit_length() - self.irreducible_poly.bit_length() 
            t ^= self.irreducible_poly << shift 
        return t 

    # Піднесення елемента поля до квадрату 
    def square(self, a): 
        return self.multiply(a, a) 

    # Піднесення елемента поля до довільного степеня 
    def power(self, a, n): 
        result = 1 
        base = a 
        while n > 0: 
            if n & 1: 
                result = self.multiply(result, base) 
            base = self.square(base) 
            n >>= 1 
        return result 

    # Знаходження оберненого елемента за множенням 
    def inverse(self, a): 
        # Використовуємо те, що a^(2^m - 2) = a^{-1} у GF(2^m) 
        return self.power(a, (1 << self.m) - 2) 

# Визначення середнього часу виконання операцій у полі
import random, time 

# Генерація випадкових елементів у полі 
def random_element(m): 
    return random.randint(1, (1 << m) - 1) 

# Вимірювання часу виконання операцій 
def benchmark_operations(field, m, iterations): 
    times = {"add": 0, "multiply": 0, "square": 0, "inverse": 0, "power": 0} 

    for _ in range(iterations): 
        a = random_element(m) 
        b = random_element(m) 
        n = random_element(m) 

        # Час для додавання 
        start = time.perf_counter() 
        field.add(a, b) 
        times["add"] += time.perf_counter() - start 

        # Час для множення 
        start = time.perf_counter() 
        field.multiply(a, b) 
        times["multiply"] += time.perf_counter() - start 

        # Час для зведення до квадрату 
        start = time.perf_counter() 
        field.square(a) 
        times["square"] += time.perf_counter() - start 

        # Час для знаходження оберненого 
        if a != 0: 
            start = time.perf_counter() 
            field.inverse(a) 
            times["inverse"] += time.perf_counter() - start 

        # Час для зведення до довільного степеня 
        start = time.perf_counter() 
        field.power(a, n) 
        times["power"] += time.perf_counter() - start 

    # Середній час для кожної операції 
    for op in times: 
        times[op] /= iterations 

    return times 

# Основна функція тестування 
if __name__ == "__main__": 
    x_a, x_b, x_c, x_d = 491, 17, 6, 2 
    irreducible_poly = (1 << x_a) | (1 << x_b) | (1 << x_c) | (1 << x_d) | 1 

    field = GF2Field(x_a, irreducible_poly) 

    # Тестування часу виконання 
    operation_times = benchmark_operations(field, x_a, 100) 

    # Вивід результатів 
    print("\nСередній час виконання операцій у полі GF(2^491):") 
    for op, avg_time in operation_times.items(): 
        print(f"Операція {op}: {avg_time:.10f} секунд")
