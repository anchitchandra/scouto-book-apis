# book-apis

## API for searching books
    GET : https://scouto-apis.herokuapp.com/search-book

    ### params:
        book_q : str | null
        category_q : str | null
        min_rent_q : str | null
        max_rent_q : str | null

## API for Transactions (Mark Issued)
    POST : https://scouto-apis.herokuapp.com/book-status

    ### params:
        book_name : str | imp
        person_name : str | imp
        issued_date : str | imp

## API for Transactions (Mark Returned)
    PUT : https://scouto-apis.herokuapp.com/book-status

    ### params:
        book_name : str | imp
        person_name : str | imp
        issued_date : str | imp

## API to get to list of peoples issued to book
    POST : https://scouto-apis.herokuapp.com/people-list

    ### params:
        book_name : str | imp

## API to get total rent generated by a book
    POST : https://scouto-apis.herokuapp.com/total-rent

    ### params:
        book_name : str | imp

## API to get to list of book issued to single person
    POST : https://scouto-apis.herokuapp.com/person-collection

    ### params:
        person_name : str | imp

## API to get to list of books issued between given date range
    POST : https://scouto-apis.herokuapp.com/between-dates
    ### params:
        fromDate : str | imp
        toDate : str | imp
