from base.com.vo.login_vo import LoginVO


# class LoginDAO:
#     def login_validate(self, login_vo):
#         user = LoginVO.query.filter_by(
#             login_username=login_vo.login_username,
#             login_password=login_vo.login_password
#         ).first()
#         return user
#

class LoginDAO:
    def login_validate(self, login_vo):
        login_vo_liist = LoginVO.query.filter_by(login_username=login_vo.login_username).all()
        print("===============", login_vo_liist)  # Debugging
        return login_vo_liist
