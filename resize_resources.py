from os.path import join, splitext
from os import stat, listdir
from PIL import Image
from util import api
from asyncio import run
from io import BytesIO

res_dir = '/Users/dpetzoldt/.config/joplin-desktop/resources'
png_big = 'accd72f8f52f49988ad8341ad1db7238.png' # 8M
jpg_big = '55087622c67b77904a2a01316393cf72.jpg' # 1.9M
tmp_folder = './tmp'

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

async def report_mimes():
    res = (await api().get_resources()).json()
    mimes = {}
    for r in res:
        mime = r.get('mime','unknown')

        mimes[mime] = mimes.get(mime,0) + 1
    print(mimes)
    # {'image/png': 228, 'application/octet-stream': 1, 'image/jpeg': 133, 'image/gif': 9, 
    # application/pdf': 16, 'image/jpg': 2, 'image/svg+xml': 1, 'image/webp': 1}

async def big_resources(kb=500):
    """List of all resources bigger than ``kb`` kilobytes"""
    res = (await api().get_resources()).json()
    # print(res)    
    return [r['id'] for r in res if r.get('size',0) > kb * 1024]


async def resize_and_replace(id,factor=.5):
    # {'id': '7d01ddbe8a37351f6ba6d1ed3ce513ec', 'title': '', 'mime': 'image/png', 'filename': '',
    # 'created_time': 1598440403780, 'updated_time': 1598641722907, 'user_created_time': 1598440403781,
    # 'user_updated_time': 1598641722907, 'file_extension': '', 'encryption_cipher_text': '', 'encryption_applied': 0,
    # 'encryption_blob_encrypted': 0, 'size': 105794, 'is_shared': 0, 'type_': 4}

    #try:
    res_old = (await api().get_resource(id)).json()
    #print(res_old)
    mime_type, mime_sub = res_old['mime'].split('/')
    if mime_sub in 'gif jpeg jpg png'.split():

        #download resource as binary content
        binary = (await api().download_resources(id))

        # save to tmp folder with mime subtype as suffix
        fname = f"{id}.{mime_sub}"
        tmp_file = join(tmp_folder,fname)
        with open(tmp_file, 'wb') as f:
            f.write(bytes(binary._content))

        img = Image.open(tmp_file)
        #img = img.resize((round(img.size[0]*factor), round(img.size[1]*factor)))
        img.save(tmp_file)
    
        await api().delete_resources(id)
        await api().create_resource(tmp_file,title=fname)
        id_new = (await api().search(fname, item_type='resource')).json()[0]['id']
        n = await replace_in_notes(id,id_new)
        print(f"Rescaled: {id_new}. Updated notes: {n}")
        
    #except Exception(e):
        # print(f"Rescaling failed: {e}")

async def replace_in_notes(source, target):
    notes = (await api().search(source, item_type='note')).json()
    for note in notes:
        body = (await api().get_note(note['id'])).json()['body']
        body =  body.replace(source,target)
        
        await api().update_note(note['id'],note['title'],body, note['parent_id'])
    return len(notes)

async def resource_by_title(title):
    res = (await api().search(title, item_type='resource', field_restrictions=body)).json()
    print(res)

if __name__ == "__main__":
    #resize_directory(res_dir)
    #run(flag_dirty(list('cb8c25fb28cd4861aa7e116edefc99b3')))
    #print( run(big_resources()) )
    #run(report_mimes())
    run(resize_and_replace('cb476015f6e742609cd221a823f572ec'))
    #run(resource_by_title('8c8746b1f18041d7a3664ac56757255e.png'))
    #run(replace_in_notes('8c8746b1f18041d7a3664ac56757255e',''))