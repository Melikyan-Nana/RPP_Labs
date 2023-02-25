#Задание 1
print('Введите первое число:')
chislo_1 = input()

print('Введите второе число:')
chislo_2 = input()

print('Введите третье число:')
chislo_3 = input()

print('Минимальное из трех введенных чисел: ', min(int(chislo_1), int(chislo_2), int(chislo_3)))

#Задание 2
print('Введите первое число:')
chislo_4 = int(input())

print('Введите второе число:')
chislo_5 = int(input())

print('Введите третье число:')
chislo_6 = int(input())

if 1 <= chislo_4 <= 50:
    print(chislo_4, ' входит в интервал [1;50]')
if 1 <= chislo_5 <= 50:
    print(chislo_5, ' входит в интервал [1;50]')
if 1 <= chislo_6 <= 50:
    print(chislo_6, ' входит в интервал [1;50]')

#Задание 3
print('Введите вещественное число (число с плавающей точкой):')
m = float(input())
for i in range(1, 11):
    print(i*m)

#Задание 4 (i)
print('Введите числа и нажмите ENTER дважды')
a = int(input('-->> '))
list = []
b = 0
while True:
    try:
        list.append(a)
        b = b + a
        a = int(input('-->> '))
    except:
        break;
print(b)

#Задание 4 (ii)
print('Введите числа и нажмите ENTER дважды')
a = int(input('-->> '))
list = []
b = 0
while True:
    try:
        list.append(a)
        b = b + 1
        a = int(input('-->> '))
    except:
        break;
print(b)