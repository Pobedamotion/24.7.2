# 24.7.2 PetFriends API Tests

## Task
API tests for PetFriends website using requests library.
Found and implemented 2 missing API methods.
Written 15 tests total (positive and negative).

## New methods added to api.py
- add_new_pet_without_photo — adds pet without photo
- add_photo_of_pet — adds photo to existing pet

## All 15 Tests

Positive tests:
- test_get_api_key_for_valid_user ✅
- test_get_all_pets_with_valid_key ✅
- test_add_new_pet_with_valid_data ✅
- test_delete_pet ✅
- test_update_pet_info ✅
- test_add_pet_without_photo ✅
- test_add_photo_to_pet ✅
- test_get_only_my_pets ✅

Negative tests (bugs found):
- test_get_api_key_with_wrong_password ✅
- test_get_api_key_with_wrong_email ✅
- test_get_pets_with_wrong_key ✅
- test_add_pet_with_empty_name ✅ (bug: returns 200)
- test_add_pet_with_empty_age ✅ (bug: returns 200)
- test_add_pet_with_long_name ✅ (bug: returns 200)
- test_delete_not_existing_pet ✅ (bug: returns 200)

## How to run
pip install requests pytest
pytest tests/test_pet_friends.py

## Results
15 passed in 27.69s ✅
