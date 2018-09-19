import requests
import odbc


def get_app_list():
    """
    call steam api GetAppList
    :return: list of {"appid":"appid (number)" , "name":"name of game"}
    """
    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0001/'
    req = requests.get(url)
    json_data = req.json()
    # print(json_data)
    applist = json_data['applist']['apps']['app']
    return applist


def insert_into_db(sql, data):
    """
    TODO: prevent sql injection
    insert data into db
    :param sql: sql query
    :param data: data
    :return: success or fail
    """

    connect = odbc.odbc('oasis')
    db = connect.cursor()
    for app in data:
        appid = int(app['appid'])
        name = app['name'].replace('\"', "'")
        db.execute(sql % (appid, name))
        print(app)


data1 = get_app_list()
sql = '''
    INSERT INTO oasis.appid(appid, name) 
    VALUES ("%d",("%s")) '''

insert_into_db(sql, data1)