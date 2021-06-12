import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from jobparser.items import InstaparserItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_user = 'zero949555'
    inst_password = 'fs437w6tA5kvLEa'
    inst_password_hash = '#PWD_INSTAGRAM_BROWSER:10:1623394961:ARdQACTYHCpEdoIVnq1gtyGLeWhMuMWv6FQHWOw3eJqE505UJLYVy+KIFONWIq3Y1Poaqs6R9PmT4j37snyClzeLk9kEGn3MP5h8EM5NtiVBl5XS/oWGarZgHPWFpCwMq3Wfzbdt1sAaSVPoc1v+9tNcrA=='
    parse_user = 'ai_machine_learning'
    posts_hash = '7ea6ae3cf6fb05e73fcbe1732b1d2a42'
    graphql_url = 'https://www.instagram.com/graphql/query/?'

    def parse(self, response:HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_user, 'enc_password': self.inst_password_hash},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response:HtmlResponse):
        j_body = response.json()
        if j_body.get('authenticated'):
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.parse_user}
            )
            print()


    def user_data_parse(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id, 'first': 12}

        url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'

        yield response.follow(url_posts,
                              callback=self.user_posts_parse,
                              cb_kwargs={
                                  'username': username,
                                  'user_id': user_id,
                                  'variables': deepcopy(variables)
                             })


    def user_posts_parse(self, response:HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')

            url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'

            yield response.follow(url_posts,
                                  callback=self.user_posts_parse,
                                  cb_kwargs={
                                      'username': username,
                                      'user_id': user_id,
                                      'variables': deepcopy(variables)
                                 })
        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            item = InstaparserItem(
                user_id=user_id,
                photo=post.get('node').get('display_url'),
                likes=post.get('node').get('edge_media_preview_like').get('count'),
                post_data=post.get('node')
            )
            yield item

    def fetch_csrf_token(selfself, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')


    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')