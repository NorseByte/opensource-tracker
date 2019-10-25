from time import sleep

class InstagramFunc():
    def __init__(self, instagram):
        self.instagram = instagram

    def page_size_check(self, totalFollow):
        page_size = 100
        if totalFollow < page_size:
            page_size = totalFollow
        return page_size

    def get_insta_follow_by(self, totalFollow, insta_id):
        followers = []
        followers = self.instagram.get_followers(insta_id, totalFollow, self.page_size_check(totalFollow), delayed=True)
        return followers

    def get_insta_following(self, totalFollow, insta_id):
        following = []
        following = self.instagram.get_following(insta_id, totalFollow, self.page_size_check(totalFollow), delayed=True)
        return following

    def get_insta_media(self, user):
        medias = self.instagram.get_medias(user, 25)
        media = medias[6]
        print(media)
        account = media.owner

    def get_insta_account_info(self, currentUser):
        newInfo = self.instagram.get_account(currentUser)
        sleep(3) #mimic user
        return newInfo

    def get_insta_account_info_id(self, currentUser):
        newInfo = self.instagram.get_account_by_id(currentUser)
        sleep(3) #mimix user
        return newInfo
