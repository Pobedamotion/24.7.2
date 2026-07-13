def generate_string(num):
    return "x" * num

def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

import pytest
from petfriends.api import PetFriends
from petfriends.settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user():
    """Test getting an API key for a valid user"""
    status, result = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in result


@pytest.mark.parametrize("filter", ['', 'my_pets'],
                         ids=['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(filter):
    """Parametrized test for getting the list of pets"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

@pytest.mark.parametrize("filter", [
    generate_string(255),
    generate_string(1001),
    russian_chars(),
    special_chars(),
    123
], ids=['255 symbols', 'more than 1000 symbols', 'russian', 'specials', 'digit'])
def test_get_all_pets_with_negative_filter(filter):
    """Bug: server returns 500 instead of 400 for an invalid filter"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500  # server bug — should be 400

def test_add_new_pet_with_valid_data():
    """Test adding a new pet with valid data"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(
        auth_key,
        name='Whiskers',
        animal_type='cat',
        age='2',
        pet_photo='petfriends/images/cat.jpg'
    )
    assert status == 200
    assert result['name'] == 'Whiskers'


def test_delete_pet():
    """Test deleting a pet"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 200


def test_update_pet_info():
    """Test updating a pet's information"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_pet_info(
        auth_key, pet_id,
        name='Tom',
        animal_type='cat',
        age='3'
    )
    assert status == 200
    assert result['name'] == 'Tom'

def test_add_pet_without_photo():
    """Positive test: adding a pet without a photo"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, name='Fluffy', animal_type='cat', age='1')
    assert status == 200
    assert result['name'] == 'Fluffy'

def test_add_photo_to_pet():
    """Positive test: adding a photo to a pet"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(
        auth_key, pet_id, 'petfriends/images/cat.jpg')
    assert status == 200

def test_get_api_key_with_wrong_password():
    """Negative test — incorrect password"""
    status, result = pf.get_api_key(valid_email, 'wrong_password')
    assert status == 403

def test_get_api_key_with_wrong_email():
    """Negative test — incorrect email"""
    status, result = pf.get_api_key('wrong@email.com', valid_password)
    assert status == 403

def test_get_pets_with_wrong_key():
    """Negative test — incorrect auth key"""
    auth_key = {'key': 'wrong_key_123'}
    status, result = pf.get_list_of_pets(auth_key, '')
    assert status == 403

def test_add_pet_with_empty_name():
    """Bug: the site accepts a pet with an empty name"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, name='', animal_type='cat', age='1')
    assert status == 200

def test_add_pet_with_empty_age():
    """Bug: the site accepts a pet with an empty age"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, name='Tom', animal_type='cat', age='')
    assert status == 200

def test_get_only_my_pets():
    """Positive test — get only the user's own pets"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200

def test_add_pet_with_long_name():
    """Bug: the site accepts a pet with a very long name"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, name='A' * 1000, animal_type='cat', age='1')
    assert status == 200

def test_delete_not_existing_pet():
    """Bug: the site returns 200 when deleting a non-existent pet"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.delete_pet(auth_key, '000000')
    assert status == 200
