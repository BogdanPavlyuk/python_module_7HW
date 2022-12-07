from pathlib import Path
import sys
import shutil
"""
Словник з розширеннями, при додаванні нового розширення
 - будуть створюватись нові теки під файли з новими розширеннями
"""
REGISTER_EXTENSIONS = {
    "JPEG": "images",
    "PNG": "images",
    "JPG": "images",
    "SVG": "images",
    "AVI": "video",
    "MOV": "video",
    "MKV": "video",
    "MP4": "video",
    "DOC": "documents",
    "DOCX": "documents",
    "TXT": "documents",
    "PDF": "documents",
    "XLSX": "documents",
    "PPTX": "documents",
    "MP3": "audio",
    "OGG": "audio",
    "MAV": "audio",
    "AMR": "audio",
    "ZIP": "archives",
    "GZ": "archives",
    "TAR": "archives",
    "": "other"}
""" Функція отримання списку всіх файлів."""


def get_file_list(folder):
    file_list = sorted(folder.glob("**/*"))
    return file_list


""" Функція normalize, для перекладу кирилиці."""
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ!?#$%&()[]<>;=-^"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_",
               "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str):
    return name.translate(TRANS)


"""Функція розпакування архівів"""


def unpack(archive_path, path_to_unpack):
    return shutil.unpack_archive(archive_path, path_to_unpack)


"""" Функція сортування файлів згідно їх розширень, повертає словник:
ключ - кортеж з розширення та типу файлу, значення - це список файлів
Приклад {("JPEG", "images"): ['foto.jpeg', 'logo.jpeg']}
Список файлів отримуйте за допомогою функції get_file_list()"""


def sorter(path):
    file_list = get_file_list(path)
    result_dict = {}
    for file in [files for files in file_list if files.is_file()]:
        ext = file.suffix[1:].upper()
        file_type = REGISTER_EXTENSIONS.get(ext, "other")
        if result_dict.get((ext, file_type)):
            result_dict[(ext, file_type)].append(file)
        else:
            result_dict[(ext, file_type)] = [file]
    return result_dict


""" Функція file_parser() - це головна функція."""


def file_parser(folder_for_scan):
    """ Функція отримує від користувача шлях до папки яку треба відсортувати 
    Дивиться як працює sys.argv - який парсить командний рядок"""
    """ Отримуємо список всіх файлів в цій папці, функція get_file_list()"""
    """ Нормалізуємо ім'я файлів, функція normalize()"""
    """ Сортуємо файли згідно розширень функція sorter(),
    Ітеруємось по словнику який прийшов від функції sorter()
    та списку файлів який є значеннями цього словника"""
    try:
        sorted_file_dict = sorter(folder_for_scan)
    except FileNotFoundError:
        return (
            f"Not able to find '{folder_for_scan}' folder. Please enter a correct folder name."
        )
    except IndexError:
        return "Please enter a folder name."
    except IsADirectoryError:
        return "Unknown file "
    for file_types, files in sorted_file_dict.items():
        for file in files:
            try:
                name_normalize = f"{normalize(file.name[0:-len(file.suffix)])}{file.suffix}"
                if not (path / file_types[1]).exists():
                    (path / file_types[1]).mkdir()
                if not (path / file_types[1] / file_types[0]).exists():
                    (path / file_types[1] / file_types[0]).mkdir()
                file.replace(
                    path / file_types[1] / file_types[0] / name_normalize)
            except Exception as err:
                print(f'[ERROR] {err}')
                continue
            # розпакування архівів
    for j in path.iterdir():
        if j.name == "archives" and len(list(j.iterdir())) != 0:
            for arch in j.iterdir():
                if arch.is_file() and arch.suffix in (".zip", ".gz", ".tar"):
                    arch_dir_name = arch.resolve().stem
                    path_to_unpack = Path("archives", arch_dir_name)
                    shutil.unpack_archive(arch, path_to_unpack)
    remove_folders(folder_for_scan)


""" Функція видалення старих папок """


def remove_folders(path: str):
    for i in path.iterdir():
        try:
            if i.name in ("images", "video", "audio", "documents", "archives", "other"):
                continue
            else:
                shutil.rmtree(i)
        except Exception as err:
            print(f'[ERROR] {err}')


# 2 конструкція if name == main
if __name__ == '__main__':
    path = Path(sys.argv[1]).resolve()
    file_parser(path)