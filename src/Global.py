from pathlib import Path

photos = {
    photo.stem: photo.absolute()
    for photo in Path('resources').glob('*.png')
    if photo.is_file()
}
