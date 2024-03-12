import logging

import requests

from URLS import urls
from api_models.booking import Booking

class TestBooking:
    # Can take optional query strings to search and return a subset of booking ids.
    def test_get_all_bookings_ids_using(
        self,
        no_auth_session: requests.Session
    ):
        response_create = no_auth_session.get(urls.GET_BOOKING_IDS_URL)
        logging.info(response_create)
        response_create_json = response_create.json()

        for booking_id in response_create_json:
            assert list(booking_id)[0] == "bookingid"
        # we use list() to extract keys from dict
        assert response_create.status_code == 200

    def test_get_booking_ids_using_firstname_and_lastname(
        self,
        no_auth_session: requests.Session,
        auth_session: requests.Session
    ):
        create_booking = Booking.create_single_booking(no_auth_session)
        # print(create_booking.__dict__)
        booking_id = create_booking.bookingid
        first_name = create_booking.firstname
        last_name = create_booking.lastname
        # why ids is being changed
        create_booking2 = Booking.create_single_booking(no_auth_session, first_name=create_booking.firstname, last_name=create_booking.lastname)

        response_create = no_auth_session.get(f'{urls.GET_BOOKING_IDS_URL}?firstname={first_name}&lastname={last_name}')
        logging.info(response_create)
        response_create_json = response_create.json()
        # print(response_create_json)

        get_bookings_first_name = [Booking.get_single_booking_by_id(booking_id["bookingid"], no_auth_session).json()["firstname"] for booking_id in response_create_json]
        get_bookings_last_name = [Booking.get_single_booking_by_id(booking_id["bookingid"], no_auth_session).json()["lastname"] for booking_id in response_create_json]
        # print(get_booking_first_name)
        # print(get_booking_last_name)
        # clean up
        Booking.delete_by_id(booking_id, auth_session)
        # assert
        for booking_id in range(len(response_create_json)):
            # print(booking_id)
            # get_booking = Booking.get_single_booking_by_id(booking_id["bookingid"], no_auth_session).json()
            assert get_bookings_first_name[booking_id] == first_name
            assert get_bookings_last_name[booking_id] == last_name
            # print(response_create_json[booking_id])
            assert "bookingid" == list(response_create_json[booking_id])[0]
        assert response_create.status_code == 200


        #thinking about what is being checked , we use name and lastname , but we dont use it in asserts , and what if we will have several with same name and last name...

    def test_get_booking_ids_using_checkin_and_checkout(
        self,
        no_auth_session: requests.Session,
        auth_session: requests.Session
    ):
        book = { "checkin": '2034-12-03', "checkout": "2034-12-12" }
        create_booking = Booking.create_single_booking(no_auth_session, booking_dates=book)
        print(create_booking.__dict__)
        # booking_id = create_booking.bookingid
        # # check_in = datetime.strptime(create_booking.bookingdates["checkin"], "%Y-%m-%d").date()
        # # check_out = datetime.strptime(create_booking.bookingdates["checkout"], "%Y-%m-%d").date()
        # check_in = 2014, 3, 3
        # check_out = 2014, 5, 1

        response_create = no_auth_session.get(f'https://restful-booker.herokuapp.com/booking?checkin=2023-03-03&checkout=2023-05-01')
        # the problem is hiding somewhere here  {urls.GET_BOOKING_IDS_URL}?checkin={check_in}&checkout={check_out}
        logging.info(response_create)
        response_create_json = response_create.json()
        print(response_create_json)

        get_bookings_bookingdates_checkin = [Booking.get_single_booking_by_id(booking_id["bookingid"], no_auth_session).json()["bookingdates"]["checkin"] for booking_id in response_create_json]
        get_bookings_bookingdates_checkout = [Booking.get_single_booking_by_id(booking_id["bookingid"], no_auth_session).json()["bookingdates"]["checkout"] for booking_id in response_create_json]
        print(get_bookings_bookingdates_checkin)
        print(get_bookings_bookingdates_checkout)
        #
        # # assert
        # for booking_id in range(len(response_create_json)):
        #     assert get_bookings_bookingdates_checkin[booking_id] == check_in
        #     assert get_bookings_bookingdates_checkout[booking_id] == check_out
        #     # print(response_create_json[booking_id])
        #     assert "bookingid" == list(response_create_json[booking_id])[0]
        # assert response_create.status_code == 200
        # # clean up
        # Booking.delete_by_id(booking_id, auth_session)

    def test_find_a_specific_booking_by_id(
        self,
        no_auth_session: requests.Session,
        auth_session: requests.Session
    ):
        create_booking = Booking.create_single_booking(no_auth_session)
        booking_id = create_booking.bookingid

        response_create = no_auth_session.get(f'{urls.GET_BOOKING_IDS_URL}/{booking_id}')
        logging.info(response_create)
        response_create_json = response_create.json()

        # clean up
        Booking.delete_by_id(booking_id, auth_session)
        # assert
        assert response_create_json['firstname'] == create_booking.firstname
        assert response_create_json['lastname'] == create_booking.lastname
        assert response_create_json['totalprice'] == create_booking.totalprice
        assert response_create_json['depositpaid'] == create_booking.depositpaid
        assert response_create_json['bookingdates'] == create_booking.bookingdates
        assert response_create_json['additionalneeds'] == create_booking.additionalneeds
        assert response_create.status_code == 200

    def test_create_booking(
        self,
        no_auth_session: requests.Session,
        auth_session: requests.Session,
        faker
    ):
        booking_request_body_create = {
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "totalprice": faker.pyint(min_value=1, max_value=100),
            "depositpaid": faker.pybool(),
            "bookingdates": {
                "checkin": faker.date(pattern='%Y-%m-%d'),
                "checkout": faker.date(pattern='%Y-%m-%d')
            },
            "additionalneeds": faker.word()
        }
        response_create = no_auth_session.post(urls.CREATE_BOOKING_URL, json=booking_request_body_create)
        logging.info(response_create)
        response_json = response_create.json()
        created_booking = response_json["booking"]
        booking_id = response_json["bookingid"]

        get_created_booking = Booking.get_single_booking_by_id(booking_id, no_auth_session)
        get_created_booking_json = get_created_booking.json()

        # clean up
        Booking.delete_by_id(booking_id, auth_session)
        # assert
        assert created_booking['firstname'] == get_created_booking_json['firstname']
        assert created_booking['lastname'] == get_created_booking_json['lastname']
        assert created_booking['totalprice'] == get_created_booking_json['totalprice']
        assert created_booking['depositpaid'] == get_created_booking_json['depositpaid']
        assert created_booking['bookingdates'] == get_created_booking_json['bookingdates']
        assert created_booking['additionalneeds'] == get_created_booking_json['additionalneeds']
        assert response_create.status_code == 200

    def test_update_booking(
        self,
        auth_session: requests.Session,
        faker
    ):
        create_booking = Booking.create_single_booking(auth_session)
        booking_id = create_booking.bookingid

        get_created_booking = Booking.get_single_booking_by_id(booking_id, auth_session)
        created_booking_json = get_created_booking.json()

        booking_to_update = create_booking
        booking_to_update.firstname = faker.first_name()
        booking_to_update.additionalneeds = faker.word()

        response_create = auth_session.put(f'{urls.UPDATE_BOOKING_URL}/{booking_id}',
                                           json=Booking.to_dict(booking_to_update))
        logging.info(response_create)

        get_updated_booking = Booking.get_single_booking_by_id(booking_id, auth_session)
        updated_booking_json = get_updated_booking.json()
        # clean up
        Booking.delete_by_id(booking_to_update.bookingid, auth_session)
        # assert
        assert response_create.status_code == 200
        assert updated_booking_json['firstname'] != created_booking_json['firstname']
        assert updated_booking_json['lastname'] == created_booking_json['lastname']
        assert updated_booking_json['totalprice'] == created_booking_json['totalprice']
        assert updated_booking_json['depositpaid'] == created_booking_json['depositpaid']
        assert updated_booking_json['bookingdates'] == created_booking_json['bookingdates']
        assert updated_booking_json['additionalneeds'] != created_booking_json['additionalneeds']

    def test_partial_update_booking(
        self,
        auth_session: requests.Session,
        faker
    ):
        create_booking = Booking.create_single_booking(auth_session)
        booking_id = create_booking.bookingid

        get_created_booking = Booking.get_single_booking_by_id(booking_id, auth_session)
        created_booking_json = get_created_booking.json()

        booking_to_update = {
            "firstname": faker.first_name(),
            "lastname": faker.last_name()
        }

        response_create = auth_session.patch(f'{urls.UPDATE_BOOKING_URL}/{booking_id}', json=booking_to_update)
        logging.info(response_create)
        get_updated_booking = Booking.get_single_booking_by_id(booking_id, auth_session)
        updated_booking_json = get_updated_booking.json()
        # clean up
        Booking.delete_by_id(create_booking.bookingid, auth_session)  # not sure if i delete the right instance
        # assert
        assert response_create.status_code == 200
        assert updated_booking_json['firstname'] != created_booking_json['firstname']
        assert updated_booking_json['lastname'] != created_booking_json['lastname']
        assert updated_booking_json['totalprice'] == created_booking_json['totalprice']
        assert updated_booking_json['depositpaid'] == created_booking_json['depositpaid']
        assert updated_booking_json['bookingdates'] == created_booking_json['bookingdates']
        assert updated_booking_json['additionalneeds'] == created_booking_json['additionalneeds']

    def test_delete_booking(
        self,
        auth_session: requests.Session,
        faker
    ):
        create_booking = Booking.create_single_booking(auth_session)
        booking_id = create_booking.bookingid
        get_created_booking = Booking.get_single_booking_by_id(booking_id, auth_session)
        response_create = auth_session.delete(f"{urls.DELETE_BOOKING_URL}/{booking_id}")
        logging.info(response_create)
        assert response_create.status_code == 201
        assert get_created_booking.status_code == 404










        # booking_request_body_create = {
        #     "firstname": faker.first_name(),
        #     "lastname": faker.last_name(),
        #     "totalprice": faker.pyint(min_value=1, max_value=100),
        #     "depositpaid": faker.pybool(),
        #     "bookingdates": {
        #         "checkin": faker.date(pattern='%Y-%m-%d'),
        #         "checkout": faker.date(pattern='%Y-%m-%d')
        #     },
        #     "additionalneeds": faker.word()
        # }
        # response = no_auth_session.post(urls.CREATE_BOOKING_URL, json=booking_request_body_create)
        # response_json = response.json()
        # created_booking = response_json["booking"]
        # booking_id = response_json["bookingid"]
        #
        # get_created_booking = Booking.get_single_booking_by_id(booking_id, no_auth_session)
        # get_created_booking_json = get_created_booking.json()
        #
        # # clean up
        # Booking.delete_by_id(booking_id, auth_session)
        # # assert
        # assert created_booking['firstname'] == get_created_booking_json['firstname']
        # assert created_booking['lastname'] == get_created_booking_json['lastname']
        # assert created_booking['totalprice'] == get_created_booking_json['totalprice']
        # assert created_booking['depositpaid'] == get_created_booking_json['depositpaid']
        # assert created_booking['bookingdates'] == get_created_booking_json['bookingdates']
        # assert created_booking['additionalneeds'] == get_created_booking_json['additionalneeds']
        # assert response.status_code == 200

        #
        # for booking_id in response_create_json:
        #     assert "bookingid" == list(booking_id)[0]
        # assert response_create.status_code == 200
