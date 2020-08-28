from os.path import join, splitext
from os import stat, listdir
from PIL import Image
from util import api
from asyncio import run

res_dir = '/Users/dpetzoldt/.config/joplin-desktop/resources'
png_big = 'accd72f8f52f49988ad8341ad1db7238.png' # 8M
jpg_big = '55087622c67b77904a2a01316393cf72.jpg' # 1.9M

async def res():
    r = await api().get_resource('55087622c67b77904a2a01316393cf72')
    print(r.json())

# run(res())

def resize_directory(directory, kb_treshold=500):
    for filename in listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            dir_file = join(directory, filename)
            size_kb = round(stat(dir_file).st_size * 1.0 / 1024) 
            if size_kb > kb_treshold: 
                try:
                    resize_image(dir_file, dir_file)
                    print(f"Resized: {filename}")
                except Exception:
                    print(f"Cannot resize: {filename}")


def resize_image(source, target,factor=.5):

    # https://github.com/python-pillow/Pillow

    # Create an Image object from a jpg file
    img  = Image.open(source)
    
    # Make the new image half the width and half the height of the original image
    resizedImage = img.resize((round(img.size[0]*factor), round(img.size[1]*factor)))

    # Display the original image
    # img.show()

    # Display the resized image
    # resizedImage.show()

    # Save the resized image to disk
    resizedImage.save(target)


async def flag_dirty(resources):
    """ Updates ``resources`` (or all if None) at server. """
    res = (await api().get_resources()).json()
    print(res)
    if not resources:
        res = [r for r in res if r['id'] in resources]
    print(res)
    for r in res:
        await api().update_resources(r['id'], {'user_created_time': r['user_created_time'] + 1})
        print(f"Updated: {r['id']}")

if __name__ == "__main__":
    #resize_directory(res_dir)
    run(flag_dirty(list('cb8c25fb28cd4861aa7e116edefc99b3')))