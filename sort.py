import pathlib, shutil, re

def put_in_order(folder: pathlib.Path, category_by_extension: dict, unknown_extensions: list, known_extensions: list, files_categories: dict):
    
    for file in folder.iterdir():
        if file.name in files_categories:
            continue

        elif file.is_dir():
            try: 
                file.rmdir()
            except OSError:
                put_in_order(file, category_by_extension, unknown_extensions, known_extensions, files_categories)
        
        else:
            extension = file.suffix
            old_stem = file.stem
            new_stem = normalize(TRANS, old_stem)
            new_name = f'{new_stem}{extension}'
            category = category_by_extension.get(extension)
            if category == None:
                base_folder = folder
                if extension not in unknown_extensions:
                    unknown_extensions.append(extension)
            else:
                if extension not in known_extensions:
                    known_extensions.append(extension)
                base_folder = folder.joinpath(category)
                if not base_folder.exists():
                    base_folder.mkdir()

            if category == 'archives':
                new_name, new_path = find_free_name(new_stem, base_folder)
                shutil.unpack_archive(file, new_path)
                file.unlink()
            elif category != None or (category == None and new_stem != old_stem):
                new_name, new_path = find_free_name(new_stem, base_folder, extension=extension)
                file.rename(new_path)

            if category != None:
                files_categories[category].append(new_name)
                
    old_folder_name = folder.name
    new_folder_name = normalize(TRANS, old_folder_name)
    if new_folder_name != old_folder_name:
        new_folder_name, new_path = find_free_name(new_folder_name, folder.parent)
        folder.rename(new_path) 
    return files_categories, unknown_extensions, known_extensions

def normalize(TRANS: dict, old_name: str) -> str:
    name_translitarate = old_name.translate(TRANS)
    new_name = re.sub(r'\W', '_', name_translitarate) 
    return new_name

def find_free_name (new_stem: str, base_folder: pathlib.Path, extension = ''):
    new_name = f'{new_stem}{extension}'
    new_path = base_folder.joinpath(new_name)
    if new_path.exists():
        i = 1
        while True:
            if not base_folder.joinpath(f'{new_stem}_{i}{extension}').exists():
                new_name = f'{new_stem}_{i}{extension}'
                new_path = base_folder.joinpath(new_name)
                break
            i += 1
    return new_name, new_path


def make_translitarate_table() -> dict:
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    return TRANS

TRANS = make_translitarate_table()

unknown_extensions = [] 
known_extensions = []
files_categories = {'archives' : [], 'video' : [], 'audio' : [], 'documents' : [], 'images' : []}
category_by_extension = {'.jpeg': 'images', '.png': 'images', '.jpg': 'images', '.svg': 'images', '.avi': 'video', '.mp4': 'video', '.mov': 'video', '.mkv': 'video', '.doc': 'documents', '.docx': 'documents', '.txt': 'documents', '.pdf': 'documents', '.xlsx': 'documents', '.pptx': 'documents', '.mp3': 'music', '.ogg': 'music', '.wav': 'music', '.amr': 'music', '.zip': 'archives', '.gz': 'archives', '.tar': 'archives'}

path = r'D:\Мотлох'
# path2 = r'D:\Мотлох\Новая папка(.zip'
folder = pathlib.Path(path)
# shutil.rmtree(folder)
# folder.unlink()


print(put_in_order(folder, category_by_extension, unknown_extensions, known_extensions, files_categories))






