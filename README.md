
# Эксплуатация автомобильного транспорта
#### Работа транспортного цеха по оперативным заявкам заказчика 


### Описание
Приложение позволяет взаимодействовать структурным 
подразделениям предприятия с транспортным цехом/отделом/службой. 
Структурные подразделения отправляют заявки на выделение 
транспорта (вид, количество, время и место подачи и т.д.), 
а транспортный цех/отдел/служба распределяет списочный 
подвижной состав в соответствии с поставленными задачами.

#### Реализовано:
- Форма подачи заявки с возможностью динамического добавления заявок в одной отправке. Использована технология Django FormSet с применением JavaScript
- Форма обработки заявок (форма распределения транспорта). Использована технология Django FormSet
- Фильтрация заявок по дням (опциональный выбор даты просмотра/обработки заявок)
- Форма добавления транспортной единицы
- Реализован profile пользователя с личными данными (ФИО, должностью, подразделением, e-mail и т.д.)
- Реализована автоматическая привязка заявки к сотруднику-заявителю и подразделению-заказчику
- Реализована функция API для подачи заявки
- Добавлена команда для заполнения тестовой БД из Excel-таблицы
#### Планируется реализовать:
- Добавить функцию обновления списка транспорта импортом из Excel-таблицы
- Добавить функцию редактирования заявки с фиксацией времени создания и коррекции
- Покрыть проект тестами (в особенности приложение заявок)
- Реализовать API для синхронизации работы с другими приложениями
#### Отдаленная перспектива:
- Расширить возможность переноса данных списка
автотранспорта с указанием его технического состояния (расширение возможностей команды переноса данных из Excel-таблицы).
- Автоматизация распределения транспорта по заявкам (определение критериев для автоматизации, доработка приложения в соответствии с выбранными критериями, разработка машинного обучения)
### Технологии
Python 3.9 \
Django 3.2.16 \
Django REST framework (DRF)

### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
```
python -m venv venv
```
```
source venv/scripts/activate
```

- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Для запуска сервера разработки:
```
cd oat
```
```
python3 manage.py runserver
```
  
#### Для тестирования работы приложения можно заполнить БД тестовыми данными. 
- Для заполнения пустой БД выполнить команду:
```
python3 manage.py download_data
```
- При заполнении БД с существующим данными выполнить команду с предварительным удалением существующих данных:
```
python3 manage.py download_data --delete-existing
```
### Авторы:
Максим