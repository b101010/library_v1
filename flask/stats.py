import mysql.connector


def refreshStats():
    
    db = mysql.connector.connect(
        host ="mysql",
        user ="root",
        passwd ="valami",
        database = "library"
    )

    try: 
        cur = db.cursor()
        sql = "drop table if exists author_stat, book_stat, pub_stat, avg_age, max_age, min_age, avg_after_pub_to_lib"
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = "create table author_stat (primary key (author_id)) engine = memory as (select author_id, count(distinct title_id) as count from books group by author_id)"
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = "create table book_stat (primary key (title_id)) engine = memory as (select title_id, count(*) as count from books group by title_id)"
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = "create table pub_stat (primary key (publisher_id)) engine = memory as (select publisher_id, count(distinct title_id) as count from books group by publisher_id)"
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = "create table avg_age engine = memory as (SELECT avg(DATEDIFF(now(), pub_date))/365 AS avg_age from books)"
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = "create table max_age engine = memory as (select max(pub_date) as max_age from books)"
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = "create table min_age engine = memory as (select min(pub_date) as min_age from books)"
        cur.execute(sql)
        db.commit()

        cur = db.cursor()
        sql = "create table avg_after_pub_to_lib (primary key (author_id)) engine = memory as (select author_id, avg(DATEDIFF(lib_date, pub_date))/365 AS 'avg_diff' from books left join authors on books.author_id = authors.id group by author_id)"
        cur.execute(sql)
        db.commit()

        return True
    except Exception as e:
        return e        
  