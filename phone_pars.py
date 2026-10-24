import re
import os
import sys

# Настройка путей
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

directory = os.path.join(base_dir, 'base')

# Проверяем существование папки
if not os.path.exists(directory):
    print(f'Папка "{directory}" не найдена!')
    input('Нажмите ENTER для выхода...')
    sys.exit()

# Ищем .txt файлы
txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

if not txt_files:
    print(f'Файлов с расширением .txt в папке "{directory}" не найдено')
    input('Нажмите ENTER для выхода...')
    sys.exit()

# Обрабатываем каждый .txt файл
for txt_file in txt_files:
    print(f'\nОбработка файла: {txt_file}')
    filepath = os.path.join(directory, txt_file)
    filepath2 = os.path.join(directory, f'output_{txt_file.replace(".txt", ".csv")}')

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            with open(filepath2, 'w', encoding='utf-8', newline='') as output:
                valid_phones = set()
                total_lines = 0
                processed_phones = 0
                invalid_count = 0

                for line in file:
                    total_lines += 1
                    print(f'Обработано строк: {total_lines}', end='\r')

                    # Ищем все числа в строке
                    numbers = re.findall(r'\d+', line)

                    for number in numbers:
                        # Проверяем длину - номер должен быть 11 цифр
                        if len(number) < 10 or len(number) > 11:
                            invalid_count += 1
                            continue

                        # Приводим к стандартному формату (11 цифр)
                        if len(number) == 10:
                            number = '7' + number
                        elif len(number) == 11:
                            # Меняем 8 на 7 в начале
                            if number.startswith('8'):
                                number = '7' + number[1:]
                            # Если начинается не с 7 или 8 - возможно городской
                            elif not number.startswith('7'):
                                invalid_count += 1
                                continue
                        else:
                            invalid_count += 1
                            continue

                        # Проверка на мобильный номер (коды операторов РФ)
                        # Мобильные коды: 910-919, 980-989, 920-939, 950-953, 960-969, 990-999
                        # Также 901-909, 930-939, 940-949, 950-959, 960-969, 970-979, 980-989, 990-999
                        mobile_codes = [
                            '900','901', '902', '903', '904', '905', '906', '907', '908', '909',
                            '910', '911', '912', '913', '914', '915', '916', '917', '918', '919',
                            '920', '921', '922', '923', '924', '925', '926', '927', '928', '929',
                            '930', '931', '932', '933', '934', '935', '936', '937', '938', '939',
                            '940', '941', '942', '943', '944', '945', '946', '947', '948', '949',
                            '950', '951', '952', '953', '954', '955', '956', '957', '958', '959',
                            '960', '961', '962', '963', '964', '965', '966', '967', '968', '969',
                            '970', '971', '972', '973', '974', '975', '976', '977', '978', '979',
                            '980', '981', '982', '983', '984', '985', '986', '987', '988', '989',
                            '990', '991', '992', '993', '994', '995', '996', '997', '998', '999'
                        ]

                        # Проверяем код оператора (первые 3 цифры после 7)
                        if len(number) == 11 and number[0] == '7':
                            operator_code = number[1:4]
                            if operator_code in mobile_codes:
                                valid_phones.add(number + '\r\n')
                                processed_phones += 1
                            else:
                                invalid_count += 1
                                # Городской номер или невалидный мобильный
                        else:
                            invalid_count += 1

                # Записываем уникальные номера
                valid_phones_list = list(valid_phones)
                for phone in valid_phones_list:
                    output.write(phone)

                print(f'\n{"="*50}')
                print(f'Файл: {txt_file}')
                print(f'Всего строк обработано: {total_lines}')
                print(f'Найдено уникальных валидных номеров: {processed_phones}')
                print(f'Невалидных номеров (включая городские): {invalid_count}')
                print(f'Результат сохранён в: {filepath2}')
                print(f'{"="*50}\n')

    except Exception as e:
        print(f'Ошибка при обработке файла {txt_file}: {e}')

input('Нажмите ENTER для выхода...')