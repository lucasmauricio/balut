# coding: utf-8

from flask import Flask, request, jsonify
import requests
import socket
import os
import sqlite3
import logging
import sys

__all__ = ['make_json_app']

app = Flask("user_app")

#departments = {1: {"nome": "Departamento Comercial"}, 2: {"nome": "Vendas"}, 3: {"nome": "Recursos Humanos"}, 4: {"nome": "Produção"}}
DATABASE_FILE = 'user-database.db'

#host_address = '0.0.0.0'
host_port = 0

@app.route("/users", methods = ['GET', 'POST'])
def pessoas_api(user_data=None):
    if request.method == "GET":

        logging.info('chamada get: {}'.format(user_data))
        statement = '''SELECT name, email, phone FROM users'''
        return jsonify(executa_statement_retrieve_db(statement))

    elif request.method == "POST":

        user_data = request.json
        #logging.info('chamada POST: {}'.format(user_data))
        if request.json:
            logging.info("chegou um JSON no POST: {}".format(user_data))
            return create_user(user_data)
            #return "Thanks. Your age is %s" % mydata.get("name")
        else:
            logging.info("nem sinal do JSON")
            return "no json received"


        # print 'isso é um POST, com params := ' + user_data
        #
        # print 'request.args'
        # print request.args
        #
        # name1 = 'Andres'
        # phone1 = '3366858'
        # email1 = 'user@example.com'
        # password1 = '12345'
        #
        # statement = '''INSERT INTO users(name, phone, email, password)
        #                   VALUES(?,?,?,?)'''
        #
        # valores = {(name1,phone1, email1, password1)}
        #
        # executa_statement_change_db(statement, valores)



@app.route("/user/", methods = ['GET'])
@app.route("/user/<int:user_id>", methods = ['GET', 'PUT', 'DELETE'])
def department_api(user_id=None):
    if request.method == "GET":
        logging.info('get request for id="{}"'.format(user_id))
        if user_id:
            # retrieve one specific user
            statement = '''SELECT name, email, phone FROM users where id = {}'''.format(user_id)
            logging.debug('SQL={}'.format(statement))
            user = executa_statement_retrieve_db(statement)
            logging.debug('user found for de id {}: {}'.format(user_id, user))
            if user:
                return jsonify(user)
            else:
                return "Not found", 404
        else:
            # retorna todas as notícias
            # TODO raise error
            return "Bad Request", 400

    elif request.method == "PUT":
        # update one specific user's data
        # TODO raise error
        return "Not Implemented", 501

    elif request.method == "DELETE":
        # delete one specific user
        # TODO raise error
        return "Not Implemented", 501



def test_db():
    query = 'PRAGMA database_list'
    test = executa_statement_retrieve_db(query)
    logging.info('test results: {}'.format(test))



def initialize_db():
    cria_tabelas = '''
        CREATE TABLE IF NOT EXISTS
          users(id INTEGER PRIMARY KEY, name TEXT,
                           phone TEXT, email TEXT unique, password TEXT)
    '''
    executa_statement_change_db(cria_tabelas, None)
    logging.info('table created/verified successfully')



def executa_statement_change_db(statement, values=None):
    #faz algo
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    if (values):
        resultado = cursor.execute(statement, values)
    else:
        resultado = cursor.execute(statement)
    db.commit()
    db.close()
    return resultado



def executa_statement_retrieve_db(statement):
    #faz algo
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    cursor.execute(statement)
    all_rows = cursor.fetchall()
    db.close()
    return all_rows



def create_user(new_user):

    #FIXME the application must define the id value. So, it mut not be accepted in the user's request
    #columns = ', '.join(new_user.keys())
    #placeholders = ', '.join('?' * len(new_user))
    #sql = 'INSERT INTO users ({}) VALUES ({})'.format(columns, placeholders)
    sql = 'INSERT INTO users VALUES %s'
    #logging.info(sql)
    #insert_pessoa = 'insert into users(id, name, phone, email, password) values (?,?,?,?,?)',
    #logging.info(insert_pessoa)
    #logging.info(new_user)
    #executa_statement_change_db(insert_pessoa, new_user)
    #resultado = executa_statement_change_db(sql, new_user.values())
    #resultado = executa_statement_change_db(sql)

    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    resultado = cursor.execute(sql, new_user)
    db.commit()
    db.close()


    return resultado



#registrando API do serviço
def api_register(api_id, api_data):
    logging.info("registrando o serviço '{}'".format(api_id))

    REGISTRADOR_API = 'http://registrator:8080/asset/'
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.put(REGISTRADOR_API+api_id, headers=headers, json=api_data)
        if r.status_code == 201:
            logging.info(" -registrado com sucesso: {}".format(r.status_code))
        else:
            logging.info(" -ocorreu erro no registro do serviço: {}".format(r.status_code))
            logging.info(" ->resposta do registrador: " + r.text)
            sys.exit(1)
    except requests.exceptions.ConnectionError as ce:
        # http://dev.mobify.com/blog/http-requests-are-hard/
        logging.error("These aren't the domains we're looking for. '%s'." % REGISTRADOR_API)
        logging.debug(ce)
        sys.exit(1)


def run_server(port):
    logging.info("")
    logging.info("")
    logging.info("initializing the app and its 2 services")
#    print "the server's address is " + app.config['SERVER_NAME']
    logging.info(app.config.get('SERVER_NAME'))
    logging.info(app.config.get('PORT'))

    #registering service users_api
    enterprise_api_id = 'users'
    #TODO automatizar a forma de recuperar o endereço do serviço
    payload = {'name':'Users data', "address": "http://{}:{}/users".format('localhost', port)}
    logging.info(payload)
    api_register(enterprise_api_id, payload);

    #registering service user_api
    departments_api_id = 'user'
    #TODO automatizar a forma de recuperar o endereço do serviço
    payload = {'name':'User data', "address": "http://{}:{}/user/{}user_id{}".format('localhost', port, '{','}')}
    logging.info(payload)
    api_register(departments_api_id, payload);

    app.run(host= '0.0.0.0', port=port, debug=True, use_reloader=True)



#https://github.com/benoitc/gunicorn/issues/379
@app.before_first_request
def setup_logging():
    # In production mode, add log handler to sys.stderr.
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)-5s]: %(message)s',
                        )



if __name__ == '__main__':

    setup_logging()
    logging.info('initializing the app {}...'.format(app))

    initialize_db()
    test_db()

    host_port = int(os.environ.get('PORT', 7070))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #TODO trocar ou não pelo endereço de rede da máquina??
    #sock.bind(('localhost', 0))
    #host_address, host_port = sock.getsockname()
    logging.info("==> a porta escolhida foi {}".format(host_port))
    #print "==> e meu IP {}".format(host_address)
    sock.close()

    run_server(host_port)
