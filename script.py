import csv
import hashlib

ORIGINAL_FILENAME = 'static/test.csv'
NEW_FILENAME = 'static/changed.csv'

transliterate_dict = {
    'а': 'a', 'в': 'b', 'е': 'e', 'к': 'k', 'м': 'm', 'н': 'h', 'о': 'o', 'р': 'p', 'с': 'c',
    'у': 'y', 'х': 'x', 'і': 'i', 'і': 'i', 'ї': 'yi', 'є': 'ye', 'ї': 'yi', 'ґ': 'g', 'т': 't',
    'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 'Р': 'P', 'С': 'C',
    'У': 'Y', 'Х': 'X', 'І': 'I', 'І': 'I', 'Ї': 'YI', 'Є': 'YE', 'Ґ': 'G', 'Т': 'T'
}

total_summary = 0


def transliterate(text: str) -> str:
    """
        Transliterates Cyrillic characters in the given text to their Latin counterparts.

        Args:
            text (str): The input text containing Cyrillic characters to transliterate.

        Returns:
            str: The transliterated text with Cyrillic characters replaced by their Latin equivalents.

        Example:
            >>> transliterate("Привіт, світ!")
            'Privіt, svіt!'
    """
    return ''.join(transliterate_dict.get(char, char) for char in text)


with open(file=ORIGINAL_FILENAME) as original, \
        open(file=NEW_FILENAME, mode='w') as new:
    # Read original file
    reader = csv.reader(original, delimiter=',')
    rows = list(reader)

    # translitera cyrillic character and calculate sum by last column
    for i in range(1, len(rows)):
        rows[i] = list(map(transliterate, rows[i]))
        total_summary += float(rows[i][-1])

    # Set header and add new column with default value
    header = rows[0]
    header.insert(1, 'Property')
    for row in rows[1:]:
        row.insert(1, 'None')

    # sort content by last column
    sorted_rows = sorted(rows[1:], key=lambda row: row[-1])
    sorted_rows.insert(0, header)

    # save data to new CSV file
    writer = csv.writer(new, delimiter=';')
    writer.writerows(sorted_rows)


def md5_check_sum(filepath) -> str:
    with open(filepath) as file:
        content = file.read()
        md5_sum = hashlib.md5(content.encode('utf-8')).hexdigest()
    return md5_sum


print(f'MD5 check sum: {md5_check_sum(NEW_FILENAME)}')
print(f'Total summ of last column = {total_summary}')
