a = []
n = int(input('Введите количество элементов массива: '))
sum = 0
p = 1
for i in range(n):
    a.append(int(input('Введите число, которое попадёт в массив: ')))
    if i % 2 == 0:
        sum += a[i]
    else:
        p *= a[i]
print(a)
print('Сумма четных элементов = ',sum)
print('Произведение нечетных элементов = ',p)
maximum = max(a)
minimum = min(a)
for i in range(len(a)):
    if a[i] == maximum:
        a[i] = minimum
    elif a[i] == minimum:
        a[i] = maximum
print(a)