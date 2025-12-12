# coding:utf-8

class Authorization():
    class Auth():
        def __init__(self, type: str):
            self.__type: str = type

        @property
        def type(self) -> str:
            return self.__type

        @property
        def username(self) -> str:
            return ""

        @property
        def password(self) -> str:
            raise NotImplementedError

    class Basic(Auth):
        TYPE: str = "Basic"

        def __init__(self, base64: str):
            from base64 import b64decode

            nameword: str = b64decode(base64).decode("utf-8")
            username, password = nameword.split(":", maxsplit=1)
            self.__username: str = username
            self.__password: str = password
            super().__init__(self.TYPE)

        @property
        def username(self) -> str:
            return self.__username

        @property
        def password(self) -> str:
            return self.__password

    class Bearer(Auth):
        TYPE: str = "Bearer"

        def __init__(self, token: str):
            super().__init__(self.TYPE)
            self.__token = token

        @property
        def token(self):
            return self.__token

        @property
        def password(self) -> str:
            return self.token

    class APIKey(Auth):
        TYPE: str = "ApiKey"

        def __init__(self, key: str):
            super().__init__(self.TYPE)
            self.__key = key

        @property
        def key(self):
            return self.__key

        @property
        def password(self) -> str:
            return self.key

    @classmethod
    def paser(cls, authorization: str) -> Auth:
        k, v = authorization.split(" ", maxsplit=1)
        return {
            cls.Basic.TYPE: cls.Basic,
            cls.Bearer.TYPE: cls.Bearer,
            cls.APIKey.TYPE: cls.APIKey,
        }[k](v)
