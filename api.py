import requests


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str):
        """Gets an API key using email and password"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: dict, filter: str = ''):
        """Gets the list of pets"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets',
                          headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: dict, name: str,
                    animal_type: str, age: str, pet_photo: str):
        """Adds a new pet"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url + 'api/pets',
                           headers=headers, data=data, files=file)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: dict, pet_id: str):
        """Deletes a pet by ID"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id,
                             headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: dict, pet_id: str, name: str,
                        animal_type: str, age: str):
        """Updates a pet's information"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id,
                          headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: dict, name: str,
                                  animal_type: str, age: str):
        """Adds a pet without a photo"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.post(self.base_url + 'api/create_pet_simple',
                            headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: dict, pet_id: str, pet_photo: str):
        """Adds a photo to a pet"""
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id,
                            headers=headers, files=file)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
