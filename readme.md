# Library backend v1

Nginx\
MySQL\
Flask\
Docker

## Nginx

```docker
FROM nginx:1.23

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/
```
```
server {
    listen 80;
    server_name IP_ADDRESS;

    location / {
        #include /etc/nginx/proxy_params;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://flask:5000;
    }
}
```
## Flask + Gunicorn
```docker
FROM python:3.8-slim

RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--reload", "app:app"]
```

## MySQL
```docker
FROM mysql:8.0

ENV LANG=C.UTF-8

ENV MYSQL_ROOT_PASSWORD=valami

COPY ./init_db.sql /docker-entrypoint-initdb.d/
```
## Docker-compose
A 3 containert a docker-compose segítségével buildelem, és indítom el.
```shell
docker-compose build
docker-compose up
```

```yaml
version: "3.7"


services:

  flask:
    build: ./flask
    container_name: flask
    restart: always
    expose:
      - 5000
    networks:
      - my-network

  nginx:
    build: ./nginx
    container_name: nginx
    restart: always
    ports:
      - 80:80
    networks:
      - my-network
    depends_on:
      - flask

  mysql:
    build: ./mysql
    container_name: mysql
    restart: always
    expose:
      - 3306
    networks:
      - my-network
    depends_on:
      - flask

networks:
  my-network:
```
# Funkciók
Minden lekérdezés egy JSON-t ad vissza.

## Összes könyv
/getall

## Egyedi könyvek
/getuniq

## Keresés title alapján
/search/title/\<title>

## Keresés author alapján
/search/author/\<author>

## Keresés publisher alapján
/search/publisher/\<publisher>

## Keresés publikálási dátum alapján
/search/pubdate/\<pubdate>

## Keresés könyvtárba kerülés dátuma alapján 
/search/libdate/\<libdate>

## Egy szerzőnek hány könyve van
/author_stat

## Egy könyvből hány példány van
/book_stat

## Egy kiadónak hány könyve van
/pub_stat

## Könyvek átlagos kora
/avg_age

## Legfiatalabb könyv
/max_age

## Legidősebb könyv
/min_age

## Szerzők akiktől a legtöbb egyedi könyv van a könyvtárban
/top_authors

## Megjelenéstől a könyvtárba kerülésig eltelt idő átlaga szerzőnként
/avg_after_pub_to_lib

## Új köny felvétele
/addnew
POSTolni kell egy megfelelő JSON-t, például:
```json
{
    "flname": "Bernard Moitessier",
    "lib_date": "2013-03-12",
    "pub_date": "2010-08-20",
    "publisher": "Alexandra Könyvkiadó",
    "title": "A hosszú út"
}
```
# Az adatbázisról és a lekérdezésekről
Nem volt egszerű, de találtam valahol egy CSV-t amiben volt szerző, cím, kiadó, kiadás dátum. Elég nagy "kupleráj" fogadott, de a pandas segítségével sikerült megtisztogatni. Könyvtárba kerülés dátum nyilván nem volt benne, azokat én generáltam... Tehát nem sok köze van a valósághoz, de a mi céljainknak most megfelelő. 

A statisztikákat tartalmazó táblák az első új könyv hozzáadása után jönnek létre, és minden új könyv után frissülnek.

Az alábbiakban az eredeti queryk vannak, ezekkel hoztam létre a statisztikákat tartalmazó táblákat.

## Egy szerzőnek hány könyve van
/author_stat

Az ilyen queryknél én nem az összes példányt hanem a ténylegesen különbőző könyveket vettem:
```sql
count(distinct title_id)
```
Ha az összes példány érdekelne, akkor:
```sql
count(*)
```

```sql
select author_id, count(distinct title_id) as count from books group by author_id;
```

## hány egyedi title van a könyvtárban (egy title nem feltétlenül tartozik csak egy szerzőhöz)
/book_stat

```sql
select title_id, count(*) as count from books group by title_id;
```

## Egy kiadónak hány könyve van a könyvtárban
/pub_stat

```sql
select publisher_id, count(distinct title_id) as count from books group by publisher_id;
```

## Statisztikák
/avg_age\
/max_age\
/min_age

```sql
mysql> SELECT avg(DATEDIFF(now(), pub_date))/365 AS DateDiff from books;
+-------------+
| DateDiff    |
+-------------+
| 26.06106490 |
+-------------+
1 row in set (0.02 sec)

mysql> select max(pub_date) from books;
+---------------+
| max(pub_date) |
+---------------+
| 2013-12-21    |
+---------------+
1 row in set (0.00 sec)

mysql> select min(pub_date) from books;
+---------------+
| min(pub_date) |
+---------------+
| 1969-01-01    |
+---------------+
1 row in set (0.01 sec)
```

## Legtermékenyebb szerzők
/top_authors

```sql
mysql> select author_id, authors.flname, count(distinct title_id) as count from books left join authors on books.author_id = authors.id group by author_id order by count DESC limit 15;
+-----------+--------------------------+-------+
| author_id | flname                   | count |
+-----------+--------------------------+-------+
|       224 | Terry Pratchett          |    32 |
|       410 | Orson Scott Card         |    25 |
|       918 | Bonnie Bryant            |    24 |
|      1077 | Mercedes Lackey          |    21 |
|       578 | Cynthia Harrod-Eagles    |    18 |
|      1051 | Danielle Steel           |    18 |
|         2 | Anne McCaffrey           |    17 |
|       194 | Diana Wynne Jones        |    16 |
|      1269 | R.A. Salvatore           |    16 |
|       883 | David Gemmell            |    15 |
|       971 | Linda Howard             |    15 |
|      2184 | Margaret Peterson Haddix |    14 |
|       387 | Osho                     |    14 |
|       485 | Janette Oke              |    13 |
|       841 | Johanna Lindsey          |    13 |
+-----------+--------------------------+-------+
15 rows in set (0.03 sec)
```

## Egy adott évig egy szerzőnek hány különböző könyve érhető el
/author_year/\<year>/\<author>
```sql
mysql> select * from books where author_id = 224 and lib_date <= '1990-01-01';
+------+----------+-----------+--------------+------------+------------+---------------------+---------------------+
| id   | title_id | author_id | publisher_id | pub_date   | lib_date   | updated_at          | created_at          |
+------+----------+-----------+--------------+------------+------------+---------------------+---------------------+
|  304 |      245 |       224 |          194 | 1971-11-15 | 1976-09-28 | 2023-02-06 15:13:43 | 2023-02-06 15:13:43 |
| 1127 |      828 |       224 |          482 | 1981-11-06 | 1984-02-18 | 2023-02-06 15:13:50 | 2023-02-06 15:13:50 |
| 1462 |      828 |       224 |          482 | 1981-11-06 | 1986-05-24 | 2023-02-06 15:13:53 | 2023-02-06 15:13:53 |
| 1592 |     1159 |       224 |          129 | 1987-01-15 | 1987-04-28 | 2023-02-06 15:13:54 | 2023-02-06 15:13:54 |
| 1917 |     1406 |       224 |           60 | 1987-11-12 | 1989-05-05 | 2023-02-06 15:13:57 | 2023-02-06 15:13:57 |
+------+----------+-----------+--------------+------------+------------+---------------------+---------------------+
5 rows in set (0.01 sec)
```

## A megjelenéstől a könyvtárba kerülésig eltelt idő átlaga (év) szerzőnként.
/avg_after_pub_to_lib
```sql
mysql> select author_id, authors.flname, avg(DATEDIFF(lib_date, pub_date))/365 AS 'avg_diff' from books left join authors on books.author_id = authors.id group by author_id;
```
## Egy szerzőknek a harmadikként megjelent könyve hány példányban van meg a könyvtárban. Ezt kifejtem részletesebben.

Egy szerző összes könyveinek példányai
```sql
mysql> select pub_date from books where author_id = 433;
+------------+
| pub_date   |
+------------+
| 1978-10-30 |
| 1979-10-08 |
| 1979-10-08 |
| 1985-11-06 |
| 1992-10-30 |
| 2003-11-06 |
| 2004-11-06 |
+------------+
7 rows in set (0.01 sec)
```

A példányok nem kellenek
```sql
mysql> select pub_date from books where author_id = 433 group by pub_date;
+------------+
| pub_date   |
+------------+
| 1978-10-30 |
| 1979-10-08 |
| 1985-11-06 |
| 1992-10-30 |
| 2003-11-06 |
| 2004-11-06 |
+------------+
6 rows in set (0.00 sec)
```

A harmadikként megjelent könyv
```sql
mysql> select pub_date from books where author_id = 433 group by pub_date order by pub_date asc limit 1 offset 2;
+------------+
| pub_date   |
+------------+
| 1985-11-06 |
+------------+
1 row in set (0.01 sec)
```

Az előző queryt beleraktam ennek a "hasába"
```sql
mysql> select count(*) as count from books where pub_date = (select pub_date from books where author_id = 433 group by pub_date order by pub_date asc limit 1 offset 2) and author_id = 433;
+-------+
| count |
+-------+
|     1 |
+-------+
1 row in set (0.01 sec)

mysql> select author_id, count(*) as count from books where pub_date = (select pub_date from books where author_id = 224 group by pub_date order by pub_date asc limit 1 offset 2) and author_id = 224;
+-----------+-------+
| author_id | count |
+-----------+-------+
|       224 |     2 |
+-----------+-------+
1 row in set (0.01 sec)

```
## így néz ki a DB
```sql
+----------------------+
| Tables_in_library    |
+----------------------+
| authors              | = szerzők
| avg_after_pub_to_lib | = Szerzőnként átlagosan mennyi idő után kerül be egy könyve a könyvtárba a megjelenés után
| avg_age              | = Átlagosan milyen idősek a könyvek
| books                | = könyvek
| book_stat            | = könyvek példányszáma
| author_stat          | = Egy szerzőnek hány könyve szerepel a könyvtárban
| pub_stat             | = Egy kiadónak hány könyve van a könyvtárban
| max_age              | = a legnagyobb dátum (legfiatalabb könyv)
| min_age              | = legkisebb dátum (legidősebb könyv)
| publishers           | = kiadók
| titles               | = címek
+----------------------+
```
# Update
A statisztikákat tartalmazó táblákat (engine = memory) hozom létre:
```sql
create table author_stat (primary key (author_id)) engine = memory as (select author_id, count(distinct title_id) as count from books group by author_id)
```
az alábbi módon teszteltem:
```python
import requests
import json
import time

t = time.time()

json = json.dumps({
    "flname": "Károly Simonyi",
    "lib_date": "2011-04-17",
    "pub_date": "2012-02-21",
    "publisher": "Akadémiai kiadó",
    "title": "A fizika kultúrtörténete"
})

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

for i in range(10):
    r = requests.post('http://127.0.0.1:5000/addnew', data = json, headers = headers)
    #print(f"Status Code: {r.status_code}, Response: {r.json()}")

print(time.time() - t)
```
futási idők:
a hagyományos táblákkal   ~3.94 sec\
a memóriában tároltakkal  ~1.83 sec

Egész jelentős gyorsulást sikerült elérni :)