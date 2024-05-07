## Задание для черкизово:

Задание
1. Необходимо создать таблицу на сервере MSSQL с 3 столбцами
2. Реализовать загрузку данных на сервер через VBA или Python через UI. При реализации на
Python можно использовать любой UI framework
3. Сделать хранимую процедуру на MS SQL сервере для выгрузки данных за определенный
период.
4. Реализовать возможность указывать период от до (на форме VBA или значения в Excel, на
выбранной UI framework форме) и результат хранимой процедуры из 3 пункта выгружать в
новую книгу Excel. Так же реализовать форматирование отчета (закрепление шапки и
формат столбцов)
5. Отчет должен содержать столбцы: Год, Месяц, Артикул, средние продажи за год и месяц,
доля продаж артикула за выбранный период
6. Логика отчета с расчетом средних продаж и доли продаж должна быть реализована в
хранимой процедуре



-----------------------------
> [!IMPORTANT]
> Использовал Postgres SQL по тех причинам.


> [!NOTE]
> Open API в качестве UI

-----------------------------


### Создание хранимой процедуры:
```sql
CREATE OR REPLACE PROCEDURE btwdt(start_dt integer, end_dt integer)
LANGUAGE SQL
BEGIN ATOMIC
    SELECT article,count(id) FROM item WHERE dt BETWEEN start_dt AND end_dt GROUP BY article;
END;

```
### Вызов хранимой процедуры:


```sql
CALL btwdt('2021-02-04','2021-03-01')
```
Именно так выглядит Stored Procedure для Postgres SQL. 
> [!NOTE]
> Процесс создания хранимой процедуры на MS SQL немного отличается.

-----------------------------
### Сборка и запуск приложения `Docker` - `FastAPI` - `Postgres`:

> [!NOTE] 
> В production не рекомендуется пушить `.env`, но в целях наглядности и удобства все тут.


```yaml

POSTGRES_USER=ewan
POSTGRES_PASSWORD=myPassword1979
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB_NAME=pgdb1


API_DESCRIPTION='Черкизово API - Тестовая работа Ивана Гончарова'
API_TITLE='eXCEL55 - Вэб сервис получения отчетов в формате файлов Excel'
CONTACT_EMAIL='ivan.stereotekk@gmail.com'
CONTACT_NAME='Ivan Goncharov'
CONTACT_URL='http://www.iskk.space/resume'
CONTACT_PHONE='+79855203082'
CONTACT_CV_FILE='https://hh.ru/resume/ede10e7eff0b33519e0039ed1f695844313832'
SECRET=GghjcnjNjrty3455

```




