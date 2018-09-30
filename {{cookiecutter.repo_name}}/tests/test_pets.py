from {{cookiecutter.package_name}}.components.pets import Pet, PetManager, Species


def test_pets_can_be_listed(app, client, load_component):
    # Given that I have a couple of pets
    manager = load_component(PetManager)
    pet_1 = manager.insert(Pet(species=Species.Cat, name="Fluffy", age=2))
    pet_2 = manager.insert(Pet(species=Species.Dog, name="Fido", age=1))
    manager.session.commit()

    # When I call the list_pets endpoint
    response = client.get(app.reverse_uri("pets:list_pets"))

    # Then I should get a successful response back
    assert response.status_code == 200
    assert response.json() == {
        "pets": [
            {"id": pet_1.id, "species": "cat", "name": "Fluffy", "age": 2},
            {"id": pet_2.id, "species": "dog", "name": "Fido", "age": 1},
        ]
    }


def test_pets_can_be_created(app, client):
    # Given that I don't have any pets
    # When I try to create one with valid parameters
    response = client.post(
        app.reverse_uri("pets:add_pet"),
        json={
            "species": "cat",
            "name": "Fluffy",
            "age": 2,
        }
    )

    # Then I should get back a 201 response
    assert response.status_code == 201
    assert response.json()["id"]
    assert response.json()["species"] == "cat"
    assert response.json()["name"] == "Fluffy"
    assert response.json()["age"] == 2

    # When I try to create another with the same name
    response = client.post(
        app.reverse_uri("pets:add_pet"),
        json={
            "species": "cat",
            "name": "Fluffy",
            "age": 2,
        }
    )

    # Then I should get back an error
    assert response.status_code == 400
    assert response.json() == {"error": "you already have a pet named 'Fluffy'!"}
