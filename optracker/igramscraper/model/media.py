import urllib.parse
import textwrap

from .initializer_model import InitializerModel
from .comment import Comment
from .carousel_media import CarouselMedia
from .. import endpoints


class Media(InitializerModel):
    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_SIDECAR = 'sidecar'
    TYPE_CAROUSEL = 'carousel'

    def __init__(self, props=None):
        self.identifier = None
        self.short_code = None
        self.created_time = 0
        self.type = None
        self.link = None
        self.image_low_resolution_url = None
        self.image_thumbnail_url = None
        self.image_standard_resolution_url = None
        self.image_high_resolution_url = None
        self.square_images = []
        self.carousel_media = []
        self.caption = None
        self.is_ad = False
        self.video_low_resolution_url = None
        self.video_standard_resolution_url = None
        self.video_low_bandwidth_url = None
        self.video_views = 0
        self.video_url = None
        # account object
        self.owner = None
        self.likes_count = 0
        self.location_id = None
        self.location_name = None
        self.comments_count = 0
        self.comments = []
        self.has_more_comments = False
        self.comments_next_page = None
        self.location_slug = None

        super(Media, self).__init__(props)

    @staticmethod
    def get_id_from_code(code):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
        id = 0

        for i in range(len(code)):
            c = code[i]
            id = id * 64 + alphabet.index(c)

        return id

    @staticmethod
    def get_link_from_id(id):
        code = Media.get_code_from_id(id)
        return endpoints.get_media_page_link(code)

    @staticmethod
    def get_code_from_id(id):
        parts = str(id).partition('_')
        id = int(parts[0])
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
        code = ''

        while (id > 0):
            remainder = int(id) % 64
            id = (id - remainder) // 64
            code = alphabet[remainder] + code

        return code

    def __str__(self):
        string = f"""
        Media Info:
        'Id: {self.identifier}
        Shortcode: {self.short_code}
        Created at: {self.created_time}
        Caption: {self.caption}
        Number of comments: {self.comments_count if hasattr(self,
                                                            'commentsCount') else 0}
        Number of likes: {self.likes_count}
        Link: {self.link}
        Hig res image: {self.image_high_resolution_url}
        Media type: {self.type}
        """

        return textwrap.dedent(string)

    def _init_properties_custom(self, value, prop, arr):

        if prop == 'id':
            self.identifier = value

        standart_properties = [
            'type',
            'link',
            'thumbnail_src',
            'caption',
            'video_view_count',
            'caption_is_edited',
            'is_ad'
        ]

        if prop in standart_properties:
            self.__setattr__(prop, value)

        elif prop == 'created_time' or prop == 'taken_at_timestamp' or prop == 'date':
            self.created_time = int(value)

        elif prop == 'code':
            self.short_code = value
            self.link = endpoints.get_media_page_link(self.short_code)

        elif prop == 'comments':
            self.comments_count = arr[prop]['count']
        elif prop == 'likes':
            self.likes_count = arr[prop]['count']

        elif prop == 'display_resources':
            medias_url = []
            for media in value:
                medias_url.append(media['src'])

                if media['config_width'] == 640:
                    self.image_thumbnail_url = media['src']
                elif media['config_width'] == 750:
                    self.image_low_resolution_url = media['src']
                elif media['config_width'] == 1080:
                    self.image_standard_resolution_url = media['src']

        elif prop == 'display_src' or prop == 'display_url':
            self.image_high_resolution_url = value
            if self.type is None:
                self.type = Media.TYPE_IMAGE

        elif prop == 'thumbnail_resources':
            square_images_url = []
            for square_image in value:
                square_images_url.append(square_image['src'])
            self.square_images = square_images_url

        elif prop == 'carousel_media':
            self.type = Media.TYPE_CAROUSEL
            self.carousel_media = []
            for carousel_array in arr["carousel_media"]:
                self.set_carousel_media(arr, carousel_array)

        elif prop == 'video_views':
            self.video_views = value
            self.type = Media.TYPE_VIDEO

        elif prop == 'videos':
            self.video_low_resolution_url = arr[prop]['low_resolution']['url']
            self.video_standard_resolution_url = \
            arr[prop]['standard_resolution']['url']
            self.video_low_bandwith_url = arr[prop]['low_bandwidth']['url']

        elif prop == 'video_resources':
            for video in value:
                if video['profile'] == 'MAIN':
                    self.video_standard_resolution_url = video['src']
                elif video['profile'] == 'BASELINE':
                    self.video_low_resolution_url = video['src']
                    self.video_low_bandwith_url = video['src']

        elif prop == 'location' and value is not None:
            self.location_id = arr[prop]['id']
            self.location_name = arr[prop]['name']
            self.location_slug = arr[prop]['slug']

        elif prop == 'user' or prop == 'owner':
            from .account import Account
            self.owner = Account(arr[prop])

        elif prop == 'is_video':
            if bool(value):
                self.type = Media.TYPE_VIDEO

        elif prop == 'video_url':
            self.video_standard_resolution_url = value

        elif prop == 'shortcode':
            self.short_code = value
            self.link = endpoints.get_media_page_link(self.short_code)

        elif prop == 'edge_media_to_comment':
            try:
                self.comments_count = int(arr[prop]['count'])
            except KeyError:
                pass
            try:
                edges = arr[prop]['edges']

                for comment_data in edges:
                    self.comments.append(Comment(comment_data['node']))
            except KeyError:
                pass
            try:
                self.has_more_comments = bool(
                    arr[prop]['page_info']['has_next_page'])
            except KeyError:
                pass
            try:
                self.comments_next_page = str(
                    arr[prop]['page_info']['end_cursor'])
            except KeyError:
                pass

        elif prop == 'edge_media_preview_like':
            self.likes_count = arr[prop]['count']
        elif prop == 'edge_liked_by':
            self.likes_count = arr[prop]['count']

        elif prop == 'edge_media_to_caption':
            try:
                self.caption = arr[prop]['edges'][0]['node']['text']
            except (KeyError, IndexError):
                pass

        elif prop == 'edge_sidecar_to_children':
            pass
            # #TODO implement
            # if (!is_array($arr[$prop]['edges'])) {
            #     break;
            # }
            # foreach ($arr[$prop]['edges'] as $edge) {
            #     if (!isset($edge['node'])) {
            #         continue;
            #     }

            #     $this->sidecarMedias[] = static::create($edge['node']);
            # }
        elif prop == '__typename':
            if value == 'GraphImage':
                self.type = Media.TYPE_IMAGE
            elif value == 'GraphVideo':
                self.type = Media.TYPE_VIDEO
            elif value == 'GraphSidecar':
                self.type = Media.TYPE_SIDECAR

        # if self.ownerId and self.owner != None:
        #     self.ownerId = self.getOwner().getId()

    @staticmethod
    def set_carousel_media(media_array, carousel_array):

        print(carousel_array)
        # TODO implement
        pass
        """
        param mediaArray
        param carouselArray
        param instance
        return mixed
        """
        # carousel_media = CarouselMedia()
        # carousel_media.type(carousel_array['type'])

        # try:
        #     images = carousel_array['images']
        # except KeyError:
        #     pass

        # carousel_images = Media.__get_image_urls(
        #     carousel_array['images']['standard_resolution']['url'])
        # carousel_media.imageLowResolutionUrl = carousel_images['low']
        # carousel_media.imageThumbnailUrl = carousel_images['thumbnail']
        # carousel_media.imageStandardResolutionUrl = carousel_images['standard']
        # carousel_media.imageHighResolutionUrl = carousel_images['high']

        # if carousel_media.type == Media.TYPE_VIDEO:
        #     try:
        #         carousel_media.video_views = carousel_array['video_views']
        #     except KeyError:
        #         pass

        #     if 'videos' in carousel_array.keys():
        #         carousel_media.videoLowResolutionUrl(
        #             carousel_array['videos']['low_resolution']['url'])
        #         carousel_media.videoStandardResolutionUrl(
        #             carousel_array['videos']['standard_resolution']['url'])
        #         carousel_media.videoLowBandwidthUrl(
        #             carousel_array['videos']['low_bandwidth']['url'])

        # media_array.append(carousel_media)
        # # array_push($instance->carouselMedia, $carouselMedia);
        # return media_array

    @staticmethod
    def __getImageUrls(image_url):
        parts = '/'.split(urllib.parse.quote_plus(image_url)['path'])
        imageName = parts[len(parts) - 1]
        urls = {
            'thumbnail': endpoints.INSTAGRAM_CDN_URL + 't/s150x150/' + imageName,
            'low': endpoints.INSTAGRAM_CDN_URL + 't/s320x320/' + imageName,
            'standard': endpoints.INSTAGRAM_CDN_URL + 't/s640x640/' + imageName,
            'high': endpoints.INSTAGRAM_CDN_URL + 't/' + imageName,
        }
        return urls
