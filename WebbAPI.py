from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Databas för böcker och recensioner
books = []
reviews = []

# Hjälpfunktion för att generera bok-ID
def generate_book_id():
    return len(books) + 1

# GET /books - Hämtar alla böcker i databasen med filtrering
@app.route('/books', methods=['GET'])
def get_books():
    filtered_books = books.copy()

    # Filtrera efter titel
    title = request.args.get('title')
    if title:
        filtered_books = [book for book in filtered_books if title.lower() in book['title'].lower()]

    # Filtrera efter författare
    author = request.args.get('author')
    if author:
        filtered_books = [book for book in filtered_books if author.lower() in book['author'].lower()]

    # Filtrera efter genre
    genre = request.args.get('genre')
    if genre:
        filtered_books = [book for book in filtered_books if genre.lower() in book['genre'].lower()]

    return jsonify(filtered_books)

# POST /books - Lägger till en eller flera böcker i databasen
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    data['id'] = generate_book_id()  # Tilldela ett ID till den nya boken
    books.append(data)
    return jsonify(data), 201

# GET /books/{book_id} - Hämtar en enskild bok
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({'message': 'Book not found'}), 404

# PUT /books/{book_id} - Uppdaterar information om en enskild bok
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        book.update(data)
        return jsonify(book)
    return jsonify({'message': 'Book not found'}), 404

# DELETE /books/{book_id} - Tar bort en enskild bok
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return jsonify({'message': 'Book deleted'}), 200

# POST /reviews - Lägger till en ny recension till en bok
@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    reviews.append(data)
    return jsonify(data), 201

# GET /reviews - Hämtar alla recensioner som finns i databasen
@app.route('/reviews', methods=['GET'])
def get_reviews():
    return jsonify(reviews)

# GET /reviews/{book_id} - Hämtar alla recensioner för en enskild bok
@app.route('/reviews/<int:book_id>', methods=['GET'])
def get_book_reviews(book_id):
    book_reviews = [review for review in reviews if review['book_id'] == book_id]
    return jsonify(book_reviews)

# GET /books/top - Hämtar de fem böckerna med högst genomsnittliga recensioner
@app.route('/books/top', methods=['GET'])
def get_top_books():
    # Beräkna genomsnittliga recensioner för varje bok
    avg_ratings = {}
    for review in reviews:
        book_id = review['book_id']
        rating = review['rating']
        if book_id in avg_ratings:
            avg_ratings[book_id]['total'] += rating
            avg_ratings[book_id]['count'] += 1
        else:
            avg_ratings[book_id] = {'total': rating, 'count': 1}

    # Sortera böcker efter genomsnittlig betyg och hämta de fem högsta
    sorted_books = sorted(avg_ratings.items(), key=lambda x: x[1]['total']/x[1]['count'], reverse=True)[:5]
    top_books = [{'id': book[0], 'avg_rating': book[1]['total']/book[1]['count']} for book in sorted_books]

    return jsonify(top_books)

# GET /author - Hämtar en kort sammanfattning om författaren och författarens mest kända verk
@app.route('/author', methods=['GET'])
def get_author_info():
    author = 'Aldous Huxley'
    summary_url = 'https://en.wikipedia.org/api/rest_v1/page/summary/' + author.replace(' ', '%20')
    books_url = 'https://openlibrary.org/search/authors.json?q=' + author.replace(' ', '%20')

    # Hämta kort sammanfattning av författaren från Wikipedia API
    summary_response = requests.get(summary_url)
    summary = summary_response.json()['extract'] if summary_response.status_code == 200 else None

    # Hämta författarens mest kända verk från Open Library API
    books_response = requests.get(books_url)
    works = books_response.json()['docs'][0]['author_name'] if books_response.status_code == 200 else None

    return jsonify({'summary': summary, 'most_famous_works': works})

if __name__ == "__main__":
    app.run(debug=True)




#from flask import Flask, request, json, jsonify
#
#Test = Flask(__name__)
#Resentioner = []
#
## Skapar någon form av huvudmeny.
#@Test.route("/")
#def home():
#    return "Main Menue"
#
## Låter en söka efter användarnamn.
#@Test.route("/user/<username>")
#def show_user_profile(username):
#    return f"User: {username}"
#
## Ansvarig för att kunna logga in.
#@Test.route("/login", methods=["GET", "POST"])
#def login():
#    if request.method == "POST":
#        return "Login POST Request"
#    else:
#        return "Login Page"
#
#
## Kastar in en json-fil.
#@Test.route("/submit-json", methods=["POST"])
#def handle_json():
#    data = request.json
#    return "Success!"
#
## Retunerar resentioner.
#@Test.route('/Resentioner', methods=['GET'])
#def get_reviews():
#    return jsonify(Resentioner)
#
## Lägger till resentioner.
#@Test.route('/Resentioner', methods=['POST'])
#def add_review():
#    data = request.json
#    username = data.get('username')
#    grade = data.get('grade')
#    text = data.get('text')
#
#    if not (username and grade and text):
#        return jsonify({'error': 'Incomplete data'}), 400
#
#    try:
#        grade = int(grade)
#        if grade < 1 or grade > 5:
#            raise ValueError
#    except ValueError:
#        return jsonify({'error': 'Grade must be an integer between 1 and 5'}), 400
#
#    review = {'username': username, 'grade': grade, 'text': text}
#    Resentioner.append(review)
#    return jsonify({'message': 'Review added successfully'}), 201
#
## Startar allting.
#if __name__ == "__main__":
#    Test.run(debug=True)

#from flask import Flask, request, json, jsonify
#
#app = Flask(__name__)
#
## Rot-URL route
#@app.route("/", methods=["GET"])
#def index():
#    return "Välkommen till bokrecensionsplattformen!"
#
## Ignorera favicon-förfrågningar
#@app.route('/favicon.ico')
#def favicon():
#    return jsonify({'message': 'No favicon'})
#
## Resterande kod för endpoints här
#
## Dummylagring för böcker (ersätt med en riktig databaslösning)
#bocker = []
#
## Enkel bokmodell
#class Bok:
#    def __init__(self, id, titel, forfattare, sammanfattning, genre):
#        self.id = id
#        self.titel = titel
#        self.forfattare = forfattare
#        self.sammanfattning = sammanfattning
#        self.genre = genre
#
## GET-endpoint för att hämta alla böcker
#@app.route('/books', methods=['GET'])
#def hamta_bocker():
#    # Filtrera böcker baserat på sökparametrar om de finns
#    titel = request.args.get('titel')
#    forfattare = request.args.get('forfattare')
#    genre = request.args.get('genre')
#
#    filtrerade_bocker = bocker
#    if titel:
#        filtrerade_bocker = [bok for bok in filtrerade_bocker if titel.lower() in bok['titel'].lower()]
#    if forfattare:
#        filtrerade_bocker = [bok for bok in filtrerade_bocker if forfattare.lower() in bok['forfattare'].lower()]
#    if genre:
#        filtrerade_bocker = [bok for bok in filtrerade_bocker if genre.lower() in bok['genre'].lower()]
#
#    return jsonify(filtrerade_bocker)
#
## POST-endpoint för att lägga till en ny bok
#@app.route('/books', methods=['POST'])
#def lagg_till_bok():
#    data = request.json
#    ny_bok = {
#        'id': len(bocker) + 1,
#        'titel': data['titel'],
#        'forfattare': data['forfattare'],
#        'sammanfattning': data['sammanfattning'],
#        'genre': data['genre']
#    }
#    bocker.append(ny_bok)
#    return jsonify({'meddelande': 'Bok tillagd'}), 201
#
## GET-endpoint för att hämta en specifik bok baserat på ID
#@app.route('/books/<int:bok_id>', methods=['GET'])
#def hamta_bok(bok_id):
#    bok = [bok for bok in bocker if bok['id'] == bok_id]
#    if len(bok) == 0:
#        return jsonify({'meddelande': 'Bok ej hittad'}), 404
#    return jsonify(bok[0])
#
## PUT-endpoint för att uppdatera en specifik bok baserat på ID
#@app.route('/books/<int:bok_id>', methods=['PUT'])
#def uppdatera_bok(bok_id):
#    for bok in bocker:
#        if bok['id'] == bok_id:
#            data = request.json
#            bok['titel'] = data['titel']
#            bok['forfattare'] = data['forfattare']
#            bok['sammanfattning'] = data['sammanfattning']
#            bok['genre'] = data['genre']
#            return jsonify({'meddelande': 'Bok uppdaterad'})
#    return jsonify({'meddelande': 'Bok ej hittad'}), 404
#
## DELETE-endpoint för att ta bort en specifik bok baserat på ID
#@app.route('/books/<int:bok_id>', methods=['DELETE'])
#def ta_bort_bok(bok_id):
#    for bok in bocker:
#        if bok['id'] == bok_id:
#            bocker.remove(bok)
#            return jsonify({'meddelande': 'Bok borttagen'})
#    return jsonify({'meddelande': 'Bok ej hittad'}), 404
#
#if __name__ == '__main__':
#    app.run(debug=True)