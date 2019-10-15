import urllib.parse
import json

USER_MEDIAS = '17880160963012870'
USER_STORIES = '17890626976041463'
STORIES = '17873473675158481'

BASE_URL = 'https://www.instagram.com'
LOGIN_URL = 'https://www.instagram.com/accounts/login/ajax/'
ACCOUNT_PAGE = 'https://www.instagram.com/%s'
MEDIA_LINK = 'https://www.instagram.com/p/%s'
ACCOUNT_MEDIAS = 'https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables=%s'
ACCOUNT_JSON_INFO = 'https://www.instagram.com/%s/?__a=1'
MEDIA_JSON_INFO = 'https://www.instagram.com/p/%s/?__a=1'
MEDIA_JSON_BY_LOCATION_ID = 'https://www.instagram.com/explore/locations/%s/?__a=1&max_id=%s'
MEDIA_JSON_BY_TAG = 'https://www.instagram.com/explore/tags/%s/?__a=1&max_id=%s'
GENERAL_SEARCH = 'https://www.instagram.com/web/search/topsearch/?query=%s'
COMMENTS_BEFORE_COMMENT_ID_BY_CODE = 'https://www.instagram.com/graphql/query/?query_hash=97b41c52301f77ce508f55e66d17620e&variables=%s'
LIKES_BY_SHORTCODE_OLD = 'https://www.instagram.com/graphql/query/?query_id=17864450716183058&variables={"shortcode":"%s","first":%s,"after":"%s"}'
LIKES_BY_SHORTCODE = 'https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables=%s'
FOLLOWING_URL_OLD = 'https://www.instagram.com/graphql/query/?query_id=17874545323001329&id={{accountId}}&first={{count}}&after={{after}}'
FOLLOWING_URL = 'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%s'
FOLLOWERS_URL_OLD = 'https://www.instagram.com/graphql/query/?query_id=17851374694183129&id={{accountId}}&first={{count}}&after={{after}}'
FOLLOWERS_URL = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%s'
FOLLOW_URL = 'https://www.instagram.com/web/friendships/%s/follow/'
UNFOLLOW_URL = 'https://www.instagram.com/web/friendships/%s/unfollow/'
INSTAGRAM_CDN_URL = 'https://scontent.cdninstagram.com/'
ACCOUNT_JSON_PRIVATE_INFO_BY_ID = 'https://i.instagram.com/api/v1/users/%s/info/'
LIKE_URL = 'https://www.instagram.com/web/likes/%s/like/'
UNLIKE_URL = 'https://www.instagram.com/web/likes/%s/unlike/'
ADD_COMMENT_URL = 'https://www.instagram.com/web/comments/%s/add/'
DELETE_COMMENT_URL = 'https://www.instagram.com/web/comments/%s/delete/%s/'

ACCOUNT_MEDIAS2 = 'https://www.instagram.com/graphql/query/?query_id=17880160963012870&id={{accountId}}&first=10&after='

GRAPH_QL_QUERY_URL = 'https://www.instagram.com/graphql/query/?query_id=%s'

request_media_count = 30


def get_account_page_link(username):
    return ACCOUNT_PAGE % urllib.parse.quote_plus(username)


def get_account_json_link(username):
    return ACCOUNT_JSON_INFO % urllib.parse.quote_plus(username)


def get_account_json_private_info_link_by_account_id(account_id):
    return ACCOUNT_JSON_PRIVATE_INFO_BY_ID % urllib.parse.quote_plus(str(account_id))


def get_account_medias_json_link(variables):
    return ACCOUNT_MEDIAS % urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':')))


def get_media_page_link(code):
    return MEDIA_LINK % urllib.parse.quote_plus(code)


def get_media_json_link(code):
    return MEDIA_JSON_INFO % urllib.parse.quote_plus(code)


def get_medias_json_by_location_id_link(facebook_location_id, max_id=''):
    return MEDIA_JSON_BY_LOCATION_ID % (urllib.parse.quote_plus(str(facebook_location_id)), urllib.parse.quote_plus(max_id))


def get_medias_json_by_tag_link(tag, max_id=''):
    return MEDIA_JSON_BY_TAG % (urllib.parse.quote_plus(str(tag)), urllib.parse.quote_plus(str(max_id)))


def get_general_search_json_link(query):
    return GENERAL_SEARCH % urllib.parse.quote_plus(query)


def get_comments_before_comments_id_by_code(variables):
    return COMMENTS_BEFORE_COMMENT_ID_BY_CODE % urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':')))


def get_last_likes_by_code_old(code, count, last_like_id):
    return LIKES_BY_SHORTCODE_OLD % (urllib.parse.quote_plus(code), urllib.parse.quote_plus(str(count)), urllib.parse.quote_plus(str(last_like_id)))


def get_last_likes_by_code(variables):
    return LIKES_BY_SHORTCODE % urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':')))


def get_follow_url(account_id):
    return FOLLOW_URL % urllib.parse.quote_plus(account_id)


def get_unfollow_url(account_id):
    return UNFOLLOW_URL % urllib.parse.quote_plus(account_id)


def get_followers_json_link_old(account_id, count, after=''):
    url = FOLLOWERS_URL_OLD.replace(
        '{{accountId}}', urllib.parse.quote_plus(account_id))
    url = url.replace('{{count}}', urllib.parse.quote_plus(str(count)))

    if after == '':
        url = url.replace('&after={{after}}', '')
    else:
        url = url.replace('{{after}}', urllib.parse.quote_plus(str(after)))

    return url

def get_followers_json_link(variables):
    return FOLLOWERS_URL % urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':')))


def get_following_json_link_old(account_id, count, after=''):
    url = FOLLOWING_URL_OLD.replace(
        '{{accountId}}', urllib.parse.quote_plus(account_id))
    url = url.replace('{{count}}', urllib.parse.quote_plus(count))

    if after == '':
        url = url.replace('&after={{after}}', '')
    else:
        url = url.replace('{{after}}', urllib.parse.quote_plus(after))

    return url

def get_following_json_link(variables):
    return FOLLOWING_URL % urllib.parse.quote_plus(json.dumps(variables, separators=(',', ':')))

def get_user_stories_link():
    return get_graph_ql_url(USER_STORIES, {'variables': json.dumps([], separators=(',', ':'))})


def get_graph_ql_url(query_id, parameters):
    url = GRAPH_QL_QUERY_URL % urllib.parse.quote_plus(query_id)

    if len(parameters) > 0:
        query_string = urllib.parse.urlencode(parameters)
        url += '&' + query_string

    return url


def get_stories_link(variables):
    return get_graph_ql_url(STORIES, {'variables': json.dumps(variables, separators=(',', ':'))})


def get_like_url(media_id):
    return LIKE_URL % urllib.parse.quote_plus(str(media_id))


def get_unlike_url(media_id):
    return UNLIKE_URL % urllib.parse.quote_plus(str(media_id))


def get_add_comment_url(media_id):
    return ADD_COMMENT_URL % urllib.parse.quote_plus(str(media_id))


def get_delete_comment_url(media_id, comment_id):
    return DELETE_COMMENT_URL % (urllib.parse.quote_plus(str(media_id)), urllib.parse.quote_plus(str(comment_id)))

