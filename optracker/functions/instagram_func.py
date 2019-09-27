from time import sleep

class InstagramFunc():
    def __init__(self, instagram, user):
        self.instagram = instagram
        self.user = user

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

    def get_insta_media(self):
        medias = self.instagram.get_medias(self.user, 25)
        media = medias[6]
        print(media)
        account = media.owner

    def get_insta_accountinfo_name(self):
        account = self.instagram.get_account(self.user)
        print('Account info for zeroPoint')
        print('---------------------------')
        print('Id: ', account.identifier)
        print('Username: ', account.username)
        print('Full name: ', account.full_name)
        print('Biography: ', account.biography)
        print('Profile pic url: ', account.get_profile_picture_url())
        print('External Url: ', account.external_url)
        print('Number of published posts: ', account.media_count)
        print('Number of followers: ', account.followed_by_count)
        print('Number of follows: ', account.follows_count)
        print('Is private: ', account.is_private)
        print('Is verified: ', account.is_verified, "\n\n")

    def get_insta_account_info(self, currentUser):
        newInfo = self.instagram.get_account(currentUser)
        sleep(3) #mimic user
        return newInfo

    def get_insta_account_info_id(self, currentUser):
        newInfo = self.instagram.get_account_by_id(currentUser)
        sleep(3) #mimix user
        return newInfo
