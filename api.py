from openai import OpenAI

from db import create_db, print_table_schema, runSql

from openai_key import API_KEY # This key is in the global string variable 'API_KEY' in a file named "openai_key.py" 
                               # For obvious reasons I am not icluding this file in the repository

SQL_query_maker = OpenAI(api_key=API_KEY)
SQL_query_processor = OpenAI(api_key=API_KEY)

SEPERATOR = '------------------------------------------------------------------------------------------------------------'

def main():
    create_db()
    user_input = ''
    print(SEPERATOR)
    print('This app is used to query the OpenAI API and convert your natural language questions into SQL queries.')
    print('To view the schema of the database, query \"schema\"')
    print('To exit, type \"exit\".')
    print(SEPERATOR)

    while True:
        user_input = input('Enter your query: ')
        print('')

        if check_for_comands(user_input):
            print(SEPERATOR)
            continue
        
        print(ask_chatgpt(user_input))
        print(SEPERATOR)

def check_for_comands(user_input):
    if user_input.lower().strip() == 'exit':
        exit(0)
    elif user_input.lower().strip() == 'schema':
        print_table_schema('Players')
        print('')
        print_table_schema('Matches')
        print('')
        print_table_schema('PlayerStatsMatch')
        return True

    return False

def ask_chatgpt(user_input):
    with open('create_table.txt', 'r') as f:
        sql_create_table = f.read()
    response = SQL_query_maker.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"This SQLite databse schema is what you will be referencing in your SQL query. The schema is as follows: {sql_create_table}"},
        {"role": "system", "content": "Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not explain it!"},
        {"role": "user", "content": user_input},
        ]
    )
    SQL_res = response.choices[0].message.content
    db_res = runSql(SQL_res)
    
    response = SQL_query_processor.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"This SQLite databse schema is what you will be referencing in your response. The schema is as follows: {sql_create_table}"},
        {"role": "user", "content": f"I asked a question \"{user_input}\" and the response was \"{db_res}\" Please, just give a concise response in a more friendly way? Please do not give any other suggests or chatter."},
        ]
    )

    return response.choices[0].message.content



if __name__ == "__main__":
    main()
