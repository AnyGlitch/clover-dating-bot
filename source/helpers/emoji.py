from source.types import Sex

__all__ = ["EmojiHelper"]


class EmojiHelper:
    @staticmethod
    def get_sex(emoji: str) -> Sex:
        sex = {"🙋‍♀️": Sex.FEMALE, "🙋‍♂️": Sex.MALE, "❤️": Sex.ANY}
        return sex[emoji]

    @staticmethod
    def get_opposite_sex(emoji: str) -> Sex:
        opposite = {"🙋‍♀️": Sex.MALE, "🙋‍♂️": Sex.FEMALE}
        return opposite[emoji]

    @staticmethod
    def get_by_sex(sex: Sex) -> str:
        emoji = {Sex.FEMALE: "🙋‍♀️", Sex.MALE: "🙋‍♂️", Sex.ANY: "❤️"}
        return emoji[sex]
