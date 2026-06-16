import pytest
from petfriends.api import PetFriends
from petfriends.settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user():
    """Тест получения API ключа для валидного пользователя"""
    status, result = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key():
    """Тест получения списка питомцев с валидным ключом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data():
    """Тест добавления нового питомца с валидными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(
        auth_key,
        name='Мурзик',
        animal_type='кот',
        age='2',
        pet_photo='petfriends/images/cat.jpg'
    )
    assert status == 200
    assert result['name'] == 'Мурзик'


def test_delete_pet():
    """Тест удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 200


def test_update_pet_info():
    """Тест обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_pet_info(
        auth_key, pet_id,
        name='Барсик',
        animal_type='кот',
        age='3'
    )
    assert status == 200
    assert result['name'] == 'Барсик'