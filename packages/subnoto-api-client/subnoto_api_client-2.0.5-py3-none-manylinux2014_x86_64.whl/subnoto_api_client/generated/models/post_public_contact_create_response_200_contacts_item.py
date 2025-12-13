from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_contact_create_response_200_contacts_item_language import PostPublicContactCreateResponse200ContactsItemLanguage
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="PostPublicContactCreateResponse200ContactsItem")



@_attrs_define
class PostPublicContactCreateResponse200ContactsItem:
    """ 
        Attributes:
            uuid (str): The UUID of the contact.
            email (str): The email of the contact.
            firstname (str): The first name of the contact.
            lastname (str): The last name of the contact.
            phone (None | str): The phone number of the contact.
            language (PostPublicContactCreateResponse200ContactsItemLanguage | Unset): The language of the contact.
            job_title (str | Unset): The job title of the contact.
            company (str | Unset): The company of the contact.
            address_line_1 (str | Unset): The address line 1 of the contact.
            address_line_2 (str | Unset): The address line 2 of the contact.
            zip_code (str | Unset): The zip code of the contact.
            city (str | Unset): The city of the contact.
            country (str | Unset): The country of the contact.
     """

    uuid: str
    email: str
    firstname: str
    lastname: str
    phone: None | str
    language: PostPublicContactCreateResponse200ContactsItemLanguage | Unset = UNSET
    job_title: str | Unset = UNSET
    company: str | Unset = UNSET
    address_line_1: str | Unset = UNSET
    address_line_2: str | Unset = UNSET
    zip_code: str | Unset = UNSET
    city: str | Unset = UNSET
    country: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        email = self.email

        firstname = self.firstname

        lastname = self.lastname

        phone: None | str
        phone = self.phone

        language: str | Unset = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.value


        job_title = self.job_title

        company = self.company

        address_line_1 = self.address_line_1

        address_line_2 = self.address_line_2

        zip_code = self.zip_code

        city = self.city

        country = self.country


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uuid": uuid,
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            "phone": phone,
        })
        if language is not UNSET:
            field_dict["language"] = language
        if job_title is not UNSET:
            field_dict["jobTitle"] = job_title
        if company is not UNSET:
            field_dict["company"] = company
        if address_line_1 is not UNSET:
            field_dict["addressLine1"] = address_line_1
        if address_line_2 is not UNSET:
            field_dict["addressLine2"] = address_line_2
        if zip_code is not UNSET:
            field_dict["zipCode"] = zip_code
        if city is not UNSET:
            field_dict["city"] = city
        if country is not UNSET:
            field_dict["country"] = country

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        email = d.pop("email")

        firstname = d.pop("firstname")

        lastname = d.pop("lastname")

        def _parse_phone(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone = _parse_phone(d.pop("phone"))


        _language = d.pop("language", UNSET)
        language: PostPublicContactCreateResponse200ContactsItemLanguage | Unset
        if isinstance(_language,  Unset):
            language = UNSET
        else:
            language = PostPublicContactCreateResponse200ContactsItemLanguage(_language)




        job_title = d.pop("jobTitle", UNSET)

        company = d.pop("company", UNSET)

        address_line_1 = d.pop("addressLine1", UNSET)

        address_line_2 = d.pop("addressLine2", UNSET)

        zip_code = d.pop("zipCode", UNSET)

        city = d.pop("city", UNSET)

        country = d.pop("country", UNSET)

        post_public_contact_create_response_200_contacts_item = cls(
            uuid=uuid,
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            language=language,
            job_title=job_title,
            company=company,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            zip_code=zip_code,
            city=city,
            country=country,
        )

        return post_public_contact_create_response_200_contacts_item

