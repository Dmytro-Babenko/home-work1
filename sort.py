import pathlib, shutil, sys, norm

def make_translitarate_table() -> dict:
    '''Make translitarate table from cyrillic to latin'''
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", 
        "i", "j", "k", "l", "m", "n", "o", "p", "r", 
        "s", "t", "u","f", "h", "ts", "ch", "sh", "sch", 
        "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g"
        )
    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    return TRANS

def find_free_name (new_stem: str, base_folder: pathlib.Path, 
                    extension) -> tuple[str, pathlib.Path]:
    '''
    Check if there is a file with this name in the folder.
    If there is, adds an index to the end of the folder name 
    until the name will become unique. 

    Return unique name and new Path
    '''
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

def get_folder_contents(folder: pathlib.Path, files_categories = {}, known_extensions = []) -> dict:
    '''write files names in the folder to the category(folder name)'''
    if folder.name not in files_categories:
        files_categories[folder.name] = []
    for file in folder.iterdir():
        files_categories[folder.name].append(file.name)
        if file.suffix not in known_extensions:
            known_extensions.append(file.suffix)
    return files_categories, known_extensions

def put_in_order(folder: pathlib.Path, category_by_extension: dict,
                 files_categories = {}, unknown_extensions = [], 
                 known_extensions = [], TRANS = make_translitarate_table()) -> tuple[dict, list, list]:
    '''
    Remove empty folders

    Recognizes the category of the file and processes file according to it:
    rename and replace
    
    Rename folder

    Returns lists of known and unknown extensions 
    and dictionary with lists of files in the folder by category
    '''
    for file in folder.iterdir():
        if file.is_dir():
            try: 
                file.rmdir()
            except OSError:
                if file.name in set(category_by_extension.values()):
                    get_folder_contents(file, files_categories, known_extensions)
                    continue
                put_in_order(
                    file, category_by_extension, files_categories, 
                    unknown_extensions, known_extensions, TRANS
                    )
                try:
                    file.rmdir()
                except:
                    continue
        else:
            extension = file.suffix
            old_stem = file.stem
            new_stem = norm.normalize(TRANS, old_stem)
            category = category_by_extension.get(extension)
            if category == None:
                if extension not in unknown_extensions:
                    unknown_extensions.append(extension)
                if new_stem == old_stem:
                    continue
                new_name, new_path = find_free_name(new_stem, folder, extension)
                file.rename(new_path)
            else:
                old_name = file.name
                if extension not in known_extensions:
                    known_extensions.append(extension)
                base_folder = folder.joinpath(category)
                if not base_folder.exists():
                    base_folder.mkdir()
                if category == 'archives':
                    new_name, new_path = find_free_name(new_stem, base_folder, '')
                    shutil.unpack_archive(file, new_path)
                    file.unlink()
                else:
                    new_name, new_path = find_free_name(new_stem, base_folder, extension)
                    file.rename(new_path)
                if old_name > category:
                    if category not in files_categories :
                        files_categories[category] = [new_name]
                    else:
                        files_categories[category].append(new_name)                
    old_folder_name = folder.name
    new_folder_name = norm.normalize(TRANS, old_folder_name)
    if new_folder_name != old_folder_name:
        new_folder_name, new_path = find_free_name(new_folder_name, folder.parent, '')
        folder.rename(new_path) 
    return files_categories, unknown_extensions, known_extensions

def main():
    try:
        path = sys.argv[1]
    except IndexError:
        path = input('You didn\'t write path. Please write path here: ')
    folder = pathlib.Path(path)

    while True:
        if folder.is_dir():
            break
        else:
            path = input('There are no folders on this path. Please write another: ')
            folder = pathlib.Path(path)

    category_by_extension = {
        '.jpeg': 'images', '.png': 'images', '.jpg': 'images', '.svg': 'images', 
        '.avi': 'video', '.mp4': 'video', '.mov': 'video', '.mkv': 'video', 
        '.doc': 'documents', '.docx': 'documents', '.txt': 'documents', 
        '.pdf': 'documents', '.xlsx': 'documents', '.pptx': 'documents', 
        '.mp3': 'music', '.ogg': 'music', '.wav': 'music', '.amr': 'music', 
        '.zip': 'archives', '.gz': 'archives', '.tar': 'archives'
        }

    files_categories, unknown_extensions, known_extensions = put_in_order(
                                                                folder, 
                                                                category_by_extension
                                                                )
    return files_categories, unknown_extensions, known_extensions

if __name__ == '__main__':
    print(main())

# python sort.py D:/Motloh
