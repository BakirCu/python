from twisted.web import server, resource
from twisted.internet import reactor
from user import User
from book import Book
from user_book import UserBook, id_compare_rent_return_book
from errors import InputError
from render import render


class MojSajt(resource.Resource):

    isLeaf = True

    def render_GET(self, request):

        route_choice_dict = {b"/": ('templates\\base.html', "text/html"),
                             b"/add_user": ('templates\\add_user.html', "text/html"),
                             b"/get_user": ('templates\\get_user.html', "text/html"),
                             b"/add_book": ('templates\\add_book.html', "text/html"),
                             b"/get_book": ('templates\\get_book.html', "text/html"),
                             b"/rent_book": ('templates\\rent_book.html', "text/html"),
                             b"/return_book": ('templates\\return_book.html', "text/html"),
                             b"/get_css": ('templates\\hf.css', "text/css"),
                             b"/get_image": ('templates\\leena.jpg', "text/jpg"),
                             b"/get_image1": ('templates\\giphy.gif', "text/jpg")}

        if request.path in route_choice_dict:
            request.setHeader(
                "Content-Type", route_choice_dict[request.path][1])
            with open(route_choice_dict[request.path][0], 'rb') as file:
                data = file.read()
                return data

        elif request.path == b"/user_added":

            # ovo gledas!
            try:
                user = User.read_user(request)
                User.add_user(user)
            except InputError as err:
                return str(err).encode('UTF-8')
            if user:
                data = {'first': user.first_name,
                        'last': user.last_name}
                with open('templates\\result_templates\\user_added.html', 'r') as file:
                    template = file.read()
                return render(template, data).encode('utf-8')

            else:
                return "User {} don't exist!, Try again!".format(user.first_name)

        elif request.path == b"/user_geted":
            user_file = request.args[b"first_last_name"][0].decode('UTF-8')
            try:
                user_file = User.search_user_name(user_file)
            except ValueError as err:
                return str(err).encode('UTF-8')
            else:
                items = User.search_user_database(user_file)

                if not items:
                    return 'No such file, try again'.encode('UTF-8')

                user_values_list = []
                for item in items:
                    item_dict = {'first': item[1],
                                 'last': item[2],
                                 'id': str(item[0]),
                                 'address': item[3]}
                    user_values_list.append(item_dict)
                data = {'users': user_values_list}
                with open('templates\\result_templates\\retun_users.html', 'r') as file:
                    template = file.read()
                return render(template, data).encode('utf-8')

        elif request.path == b"/book_added":
            book_name = request.args[b"book_name"][0].decode('UTF-8')
            author_name = request.args[b"author_name"][0].decode('UTF-8')
            book_num = request.args[b"book_num"][0].decode('UTF-8')
            try:
                book = Book(book_name, author_name, book_num)
                Book.add_book(book)
            except InputError as err:
                return str(err).encode('utf-8')
            except ValueError as err:
                full_err = str(err) + ' BOOK NUMBER must be int'
                return full_err.encode('UTF-8')
            if book:
                data = {'book': book_name,
                        'author': author_name,
                        'num': str(book_num)}
                with open('templates\\result_templates\\book_added.html', 'r') as file:
                    template = file.read()
                return render(template, data).encode('utf-8')

            else:
                return "Book {} did't added! Try again!".format(book_name)

        elif request.path == b"/book_geted":
            book_file = request.args[b"book_author_name"][0].decode('UTF-8')
            try:
                book_file = Book.search_book_name(book_file)
            except InputError as err:
                return str(err).encode('utf-8')
            else:
                items = Book.search_book_database(book_file)
                if not items:
                    return 'No such file, try again'.encode('utf-8')
                    # OVDE POCINJE RENDER
                print(items)
                user_values_list = []
                for item in items:
                    item_dict = {'author': item[1],
                                 'num': str(item[2]),
                                 'book': item[0],
                                 }
                    user_values_list.append(item_dict)
                data = {'books': user_values_list}
                with open('templates\\result_templates\\return_books.html', 'r') as file:
                    template = file.read()
                return render(template, data).encode('utf-8')

        elif request.path == b"/book_rented":
            try:
                user_id = request.args[b"user_id"][0].decode('UTF-8')
                book_id = request.args[b"book_id"][0].decode('UTF-8')
                user_book_id = UserBook(user_id, book_id)
                list_of_rented_books = UserBook.rent_book(user_book_id)
                UserBook.books_rent_limit(list_of_rented_books)
            except ValueError as err:
                full_err = str(err) + 'user id, and book id, must be integer'
                return full_err.encode('UTF-8')
            except InputError as err:
                return str(err).encode('utf-8')
            return "The book is successfully rented".encode('UTF-8')

        elif request.path == b"/book_renturned":
            try:
                user_id = request.args[b"user_id"][0].decode('UTF-8')
                book_id = request.args[b"book_id"][0].decode('UTF-8')
                user_book_id = UserBook(user_id, book_id)
                book_rent_id = UserBook.id_return_book(user_book_id)
                id_compare_rent_return_book(user_book_id, book_rent_id)
                items = UserBook.date_return_book(user_book_id)
                items_str = str(items[0])
                having_book = UserBook.days_keeping_book(items_str)
            except ValueError as err:
                full_err = str(err) + 'user id, and book id, must be integer'
                return full_err.encode('UTF-8')
            except InputError as err:
                return str(err).encode('utf-8')
            except IndexError as err:
                full_err = "You didn't rent a book, try again " + str(err)
                return full_err.encode('UTF-8')
            full_str = 'You took book:' + \
                items_str[2:20] + 'You have a book:' + \
                str(having_book) + 'days'
            return full_str.encode('UTF-8')

        return "Unknown routh".encode('utf-8')


site = server.Site(MojSajt())
reactor.listenTCP(8080, site)
reactor.run()
