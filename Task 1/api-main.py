#python api-main.py

import requests
import sqlite3
"""At fist we need to work on fetching the data from Open Library """
def api_fetch(query):
    url = f'https://openlibrary.org/search.json?q={query}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: API failed to fetch the data with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: Exception occurred - {e}")
        return None
#query = 'the lord of the rings'
#book_data =api_fetch(query)
#(query)

''' We want the query to be user input 
and also change the input to the lower case'''

user=input("Which book u want to choose ? : ")
query=user.lower()
book_data=api_fetch(query)

if book_data:
    print("Successfully Fetched")
    print("Number of books found:", book_data.get('numFound', 0))
    
    
    '''FORMAT-docs": [
        {
            "author_alternative_name": [
                "J. R. R. Tolkien",
                "Yue Han Luo Na De Rui Er Tuo Er Jin",
                "Tolkien",
                "John R. R. Tolkien",
                "Dzhon R. R. Tolkin",
                "John Ronald Reuel Tolkien"
            ],
            "author_key": [
                "OL26320A"
            ],
            "author_name": [
                "J.R.R. Tolkien"
            ],...............'''
    #Sub-Task: Storing it in a local SQLite database
    #Lets Start with connecting database

    user_db = input("Enter the name of the database : ")
    conn = sqlite3.connect(user_db)
    print("Connected to SQLite database")          
            
    if 'docs' in book_data:
        print("Book Information:")
        print("=" * 50)
        for doc in book_data['docs']:
            
            
            title = doc.get('title', 'NA')
            if title != 'NA':
                print(f"Title : {title}")
            authors = ', '.join(doc.get('author_name', 'NA'))
            if authors != 'NA':
                print(f"Author(s) Name: {authors}")
            publish_year = doc.get('first_publish_year', 'NA')
            if publish_year != 'NA':
                print(f"First published year: {publish_year}")
                
            #Converting the title to lower case and replacing the spaces with underscores
            table_name = title.lower().replace(" ", "_")  
            #Creating Table 
            table_creation_query = f"CREATE TABLE IF NOT EXISTS {table_name} (Title TEXT, Author TEXT, First_Publication_Year TEXT)"
            conn.execute(table_creation_query)
            data_insertion = f"INSERT INTO {table_name} (Title, Author, First_Publication_Year) VALUES (?, ?, ?)"
            conn.execute(data_insertion, (title, authors, publish_year))
            conn.commit()

            print(f"Table created and data inserted for book: {title}")

            print("-" * 50)
    else:
        print("API fetch failed.")
    conn.close()
    print("Disconnected from SQLite database")   


