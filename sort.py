import pathlib, shutil, re

def put_in_order(folder: pathlib.Path, category_by_extension: dict, unknown_extensions: list, known_extensions: list, files_categories: dict):
    
    for file in folder.iterdir():
        if file.name in files_categories:
            continue
        elif file.is_dir():
            try: 
                file.rmdir()
            except:
                put_in_order(file, category_by_extension, unknown_extensions, known_extensions, files_categories)
        else:
            extension = file.suffix
            new_stem = normalize(TRANS, file.stem)
            new_name = f'{new_stem}{extension}'
            category = category_by_extension.get(extension)
            if category == None:
                if extension not in unknown_extensions:
                    unknown_extensions.append(extension)
            else:
                if extension not in known_extensions:
                    known_extensions.append(extension)

                if category == 'archives':
                    files_categories[category].append(new_name)

                else:
                    category_folder = folder.joinpath(category)
                    if not category_folder.exists():
                        category_folder.mkdir()
                
                    try:
                        file.rename(category_folder.joinpath(new_name))
                    except FileExistsError:
                        i = 1
                        while True:
                            try: 
                                new_name = f'{new_stem}_{i}{extension}'
                                file.rename(category_folder.joinpath(new_name))
                            except FileExistsError:
                                i += 1
                            else:
                                break

                    files_categories[category].append(new_name)   
    new_name = normalize(TRANS, folder.name)
    folder.rename(folder.with_name(new_name)) 
    return files_categories, unknown_extensions, known_extensions

def normalize(TRANS: dict, old_name: str) -> str:
    name_translitarate = old_name.translate(TRANS)
    new_name = re.sub(r'\W', '_', name_translitarate) 
    return new_name

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
path = r'D:\Мотлох'
unknown_extensions = [] 
known_extensions = []
files_categories = {'archives' : [], 'video' : [], 'audio' : [], 'documents' : [], 'images' : []}
category_by_extension = {'.jpeg': 'images', '.png': 'images', '.jpg': 'images', '.svg': 'images', '.avi': 'video', '.mp4': 'video', '.mov': 'video', '.mkv': 'video', '.doc': 'documents', '.docx': 'documents', '.txt': 'documents', '.pdf': 'documents', '.xlsx': 'documents', '.pptx': 'documents', '.mp3': 'music', '.ogg': 'music', '.wav': 'music', '.amr': 'music', '.zip': 'archives', '.gz': 'archives', '.tar': 'archives', '.rar': 'archives'}

folder = pathlib.Path(path)
print(put_in_order(folder, category_by_extension, unknown_extensions, known_extensions, files_categories))






