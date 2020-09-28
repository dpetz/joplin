from context import zettel
import server


common_fields = [
    'id',
    'title',
    'user_created_time',
    'user_updated_time',
    'updated_time',
    'parent_id',
    'encryption_applied',
    'type_']

returned_fields_search_note = set(common_fields + [
    'is_todo',
    'todo_completed',
    'todo_due',
    'order',
    'markup_language'])

returned_fields_search_tag = set(common_fields + [
    'encryption_cipher_text',
    'is_shared'])

returned_fields_search_folder = set(common_fields + [
    'encryption_cipher_text',
     'created_time',
    'is_shared'])
 


async def _test_tag_search():
    keys = set((await server.api().search('test', item_type='tag')).json()[0].keys())
    assert returned_fields_search_tag == keys, keys
        

async def _test_folder_search():
    keys = set((await server.api().search('Test', item_type='folder')).json()[0].keys())
    assert returned_fields_search_tag == keys, keys
       

async def _test_folder_search():
    keys = set((await server.api().search('Test*')).json()[0].keys())
    assert returned_fields_search_note == keys, keys
        