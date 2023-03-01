
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import stats

import MySQLdb

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b17b264b25ed4837fe37c363f500ae15'

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'valami'
app.config['MYSQL_DB'] = 'library'


class db:

    def __init__(self, sql):
        self.sql = sql

    def get(self):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(self.sql)
        results = cursor.fetchall()
        cursor.close()
        return results


mysql = MySQL(app)

# osszes konyv


@app.route("/getall", methods=['GET'])
def getall():
    try:
        sql = "select books.id, pub_date, lib_date, titles.title, authors.flname, created_at, updated_at, publishers.publisher from books left join titles on books.title_id = titles.id left join authors on books.author_id = authors.id left join publishers on books.publisher_id = publishers.id"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# egyedi konyvek


@app.route("/getuniq", methods=['GET'])
def getuniq():
    try:
        sql = 'select distinct titles.title, authors.flname, publishers.publisher from books left join titles on books.title_id = titles.id left join authors on books.author_id = authors.id left join publishers on books.publisher_id = publishers.id'
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# kereses title alapjan


@app.route("/search/title/<title>", methods=['GET'])
def search_by_title(title):
    try:
        sql = f"select books.id, pub_date, lib_date, titles.title, authors.flname, created_at, updated_at, publishers.publisher from books left join titles on books.title_id = titles.id left join authors on books.author_id = authors.id left join publishers on books.publisher_id = publishers.id where titles.title LIKE '%{title}%'"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# kereses author alapjan


@app.route("/search/author/<author>", methods=['GET'])
def search_by_author(author):
    try:
        sql = f"select books.id, pub_date, lib_date, titles.title, authors.flname, created_at, updated_at, publishers.publisher from books left join titles on books.title_id = titles.id left join authors on books.author_id = authors.id left join publishers on books.publisher_id = publishers.id where authors.flname LIKE '%{author}%'"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# kereses kiado alapjan


@app.route("/search/publisher/<publisher>", methods=['GET'])
def search_by_publisher(publisher):
    try:
        sql = f"select books.id, pub_date, lib_date, titles.title, authors.flname, created_at, updated_at, publishers.publisher from books left join titles on books.title_id = titles.id left join authors on books.author_id = authors.id left join publishers on books.publisher_id = publishers.id where publishers.publisher LIKE '%{publisher}%'"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# kereses publikalasi datum alapjan


@app.route("/search/pubdate/<pubdate>", methods=['GET'])
def search_by_pubdate(pubdate):
    try:
        sql = f"select books.id, pub_date, lib_date, titles.title, authors.flname, created_at, updated_at, publishers.publisher from books left join titles on books.title_id = titles.id left join authors on books.author_id = authors.id left join publishers on books.publisher_id = publishers.id where pub_date LIKE '%{pubdate}%'"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# kereses konyvtarba kerules datuma alapjan


@app.route("/search/libdate/<libdate>", methods=['GET'])
def search_by_libdate(libdate):
    try:
        sql = f"select books.id, pub_date, lib_date, titles.title, authors.flname, created_at, updated_at, publishers.publisher from books left join titles on books.title_id = titles.id left join authors on books.author_id = authors.id left join publishers on books.publisher_id = publishers.id where lib_date LIKE '%{libdate}%'"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# statisztikak
# egy szerzonek hany konyve van


@app.route("/author_stat", methods=['GET'])
def author_stat():
    try:
        sql = f"select flname, count from author_stat left join authors on author_stat.author_id = authors.id"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# egy konyvbol hany peldany van


@app.route("/book_stat", methods=['GET'])
def book_stat():
    try:
        sql = f"select title, count from book_stat left join titles on book_stat.title_id = titles.id"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# egy kiadonak hany konyve van


@app.route("/pub_stat", methods=['GET'])
def pub_stat():
    try:
        sql = f"select publisher, count from pub_stat left join publishers on pub_stat.publisher_id = publishers.id"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# konyvek atlagos kora


@app.route("/avg_age", methods=['GET'])
def avg_age():
    try:
        sql = f"select * from avg_age"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# legfiatalabb konyv


@app.route("/max_age", methods=['GET'])
def max_age():
    try:
        sql = f"select * from max_age"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# legidosebb konyv


@app.route("/min_age", methods=['GET'])
def min_stat():
    try:
        sql = f"select * from min_age"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404


# top_authors


@app.route("/top_authors", methods=['GET'])
def top_authors():
    try:
        sql = f"select author_id, authors.flname, count(distinct title_id) as count from books left join authors on books.author_id = authors.id group by author_id order by count DESC limit 15"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404


# a megjelenestol a konyvtarba kerulesig eltelt ido atlaga (ev) szerzonkent.


@app.route("/avg_after_pub_to_lib", methods=['GET'])
def avg_after_pub_to_lib():
    try:
        sql = f"select avg_diff, authors.flname from avg_after_pub_to_lib left join authors on avg_after_pub_to_lib.author_id = authors.id"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# adott szerzonek adott evig elerheto konyvei


@app.route("/author_year/<year>/<author>", methods=['GET'])
def author_year(year, author):
    year = datetime.strptime(year, '%Y')
    try:
        sql = f"select * from books where author_id = '{author}' and lib_date <= '{year}'"
        query = db(sql)
        books = query.get()

        return jsonify(books)
    except:
        error = {
            'error': 'Something wrong happend... :(',
        }
        return jsonify(error), 404

# delete book


@app.route("/delete/<id>", methods=['DELETE'])
def delete(id):
    # megnezem, h. van e mar ilyen a DBben
    cur = mysql.connection.cursor()
    cur.execute(f"select * from books where id = '{id}'")
    result = cur.fetchone()
    cur.close()
    if result != None:  # ha van mar ilyen
        cur = mysql.connection.cursor()
        cur.execute(f"delete from books where id = '{id}'")
        mysql.connection.commit()
        deleted = {
            'deleted': id
        }
        return jsonify(deleted)
    else:
        error = {
            'error': 'Nothong to delete... :(',
        }
        return jsonify(error), 404


# uj konyv


@app.route("/addnew", methods=['POST'])
def addnew():
    # a json strukturajat jo lenne csekkolni...
    if request.is_json:
        data = request.json
        flname = data.get('flname')
        lib_date = data.get('lib_date')
        pub_date = data.get('pub_date')
        publisher = data.get('publisher')
        title = data.get('title')

        # author
        # megnezem, h. van e mar ilyen a DBben
        cur = mysql.connection.cursor()
        cur.execute(f"select * from authors where flname = '{flname}'")
        result = cur.fetchone()
        cur.close()
        if result != None:  # ha van mar ilyen
            author_id = result[0]
        else:  # ha nincs
            cur = mysql.connection.cursor()
            cur.execute(f"insert into authors (flname) values ('{flname}')")
            mysql.connection.commit()
            author_id = cur.lastrowid
            cur.close()

        # title
        # megnezem, h. van e mar ilyen a DBben
        cur = mysql.connection.cursor()
        cur.execute(f"select * from titles where title = '{title}'")
        result = cur.fetchone()
        cur.close()
        if result != None:  # ha van mar ilyen
            title_id = result[0]
        else:  # ha nincs
            cur = mysql.connection.cursor()
            cur.execute(f"insert into titles (title) values ('{title}')")
            mysql.connection.commit()
            title_id = cur.lastrowid
            cur.close()

        # publisher
        # megnezem, h. van e mar ilyen a DBben
        cur = mysql.connection.cursor()
        cur.execute(
            f"select * from publishers where publisher = '{publisher}'")
        result = cur.fetchone()
        cur.close()
        if result != None:  # ha van mar ilyen
            publisher_id = result[0]
        else:  # ha nincs
            cur = mysql.connection.cursor()
            cur.execute(
                f"insert into publishers (publisher) values ('{publisher}')")
            mysql.connection.commit()
            publisher_id = cur.lastrowid
            cur.close()

        # book
        cur = mysql.connection.cursor()
        cur.execute(
            f'INSERT INTO books(title_id, author_id, publisher_id, pub_date, lib_date) VALUES("{title_id}","{author_id}","{publisher_id}","{pub_date}","{lib_date}")')
        mysql.connection.commit()
        last_id = cur.lastrowid
        cur.close()

        st = stats.refreshStats()

        info = {
            'stats refreshed': st,
            'last id': last_id 
        }

        return jsonify(info)
    else:
        return jsonify('ez nem json...'), 404


if __name__ == "__main__":
    app.run(debug=True)
