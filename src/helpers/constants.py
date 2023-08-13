from enum import Enum

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Environment(str, Enum):
    LOCAL = "LOCAL"
    STAGING = "STAGING"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)


S3_SONG_PATH = "songs/audios/"
S3_SONG_THEME_PATH = "songs/themes/"
S3_AVATAR_FOLDER_PATH = "users/avatar/"
S3_DEFAULT_AVATAR = "users/avatar/DEFAULT_FEMALE.svg"
S3_ALBUM_COVER_IMAGE_PATH = "albums/cover/"
S3_Artist_AVATAR_PATH = "artists/avatar/"


class Gender(int, Enum):
    MALE = 1
    FEMALE = 2
    UNDEFINED = 0
