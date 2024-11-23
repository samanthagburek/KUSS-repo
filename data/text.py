"""
This module interfaces to our journal text data.
"""
import data.db_connect as dbc

TEXT_COLLECT = 'text'


# fields
KEY = 'key'
TITLE = 'title'
TEXT = 'text'

EMAIL = 'email'

TEST_KEY = 'HomePage'
DEL_KEY = 'DeletePage'

text_dict = {
    TEST_KEY: {
        TITLE: 'Home Page',
        TEXT: 'This is a journal about building API servers.',
    },
    DEL_KEY: {
        TITLE: 'Home Page',
        TEXT: 'This is a journal about building API servers.',
    },
}


client = dbc.connect_db()
print(f'{client=}')


def create(key: str, title: str, text: str):
    if key in read():
        raise ValueError(f'Page already exists {key=}')
    newtext = {KEY: key, TITLE: title, TEXT: text}
    dbc.create(TEXT_COLLECT, newtext)
    return key


def delete(key):
    return dbc.delete(TEXT_COLLECT, {KEY: key})


def update(key: str, title: str, text: str):
    if key in read():
        text_dict[key][TITLE] = title
        text_dict[key][TEXT] = text
        return dbc.update_doc(TEXT_COLLECT, {KEY: key},
                                            {TITLE: title, TEXT: text})
    else:
        raise ValueError(f'Text not found {key=}')


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = dbc.read_dict(TEXT_COLLECT, KEY)
    return text


def read_one(key: str) -> dict:
    text = dbc.fetch_one(TEXT_COLLECT, {KEY: key})
    print(f'{key=}')
    return text


def main():
    print(read())


if __name__ == '__main__':
    main()
