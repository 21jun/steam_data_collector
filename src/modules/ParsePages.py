from src.utills.UrlGenerator import url_generator
from src.crawler import SteamAppParser
import src.modules.GetAppIds as GetAppIds
from tqdm import tqdm


def page_parser(data_base, table, crawler):
    GetAppIds.db_update_dist_table('player_count', 'watching_games')
    apps = data_base.db_get_apps(table)
    for app in tqdm(apps):
        info = {
            'appid': int(app[0]),
            'name': app[1]
        }
        try:
            soup = crawler.parse_url(url_generator(info['appid']))
            result = SteamAppParser.GetAppInfo(soup, info).get_info()
            print(result)
            data_base.db_update_app_data(result)
        except TimeoutError:
            print("TIME OUT")


if __name__ == "__main__":
    # initialize
    crawler = SteamAppParser.HeadlessChrome('C:/chromedriver_win32/chromedriver')
    data_base = SteamAppParser.DataBaseConnector()

    page_parser(data_base, 'watching_games', crawler)