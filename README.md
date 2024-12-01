# Overview

This API allows you to manage phone number verifications and user referrals.</b>
It provides endpoints for creating and updating phone number verifications, retrieving user details, and listing referrals.</b>
Swagger is integrated for easy API documentation and testing.

## Endpoints

- [Create Phone Number Verification](#create-phone-number-verification)
- [Update Phone Number Verification](#update-phone-number-verification)
- [User Details](#user-details)
- [User Referrals](#user-referrals)

## Create Phone Number Verification

**Endpoint:** `/api/phone-number/create/`  
**Method:** `POST`  
**Description:** Creates a phone number verification entry.

**Request Body:**

```json
{
  "phone_number": "1234567890",
  "auth_code": "1234",
  "referal_number": "ABCD12",
  "activated_referal_number": "EFGH34",
  "country_code": "+375"
}
```

**Response:**

```json
{
  "phone_number": "1234567890",
  "auth_code": "1234",
  "referal_number": "ABCD12",
  "activated_referal_number": "EFGH34",
  "country_code": "+375",
  "user": {
    "username": "user1",
    "email": "user1@example.com"
  }
}
```

## Update Phone Number Verification

**Endpoint:** `/api/phone-number/update/<str:phone_number>/ `
**Method:** `PUT`
**Description:** `Updates a phone number verification entry.`

**Request Body:**

```json
{
  "auth_code": "5678",
  "referal_number": "WXYZ56",
  "activated_referal_number": "LMNOP78",
  "country_code": "+7"
}
```

**Response:**

```json
{
  "phone_number": "1234567890",
  "auth_code": "5678",
  "referal_number": "WXYZ56",
  "activated_referal_number": "LMNOP78",
  "country_code": "+7",
  "user": {
    "username": "user1",
    "email": "user1@example.com"
  }
}
```

## User Details

**Endpoint:** `/api/user/`
**Method:** `GET`
**Description:** `Retrieves the details of the authenticated user.`

**Response:**

```json
{
  "username": "user1",
  "email": "user1@example.com"
}
```

## User Referrals

**Endpoint:** /api/profile-referals/
**Method:** GET
**Description:** Retrieves the list of users who used the authenticated user's referral code.
**Response:**

```json
[
  {
    "phone_number": "0987654321",
    "auth_code": "5678",
    "referal_number": "ABCD12",
    "activated_referal_number": "EFGH34",
    "country_code": "+375",
    "user": {
      "username": "user2",
      "email": "user2@example.com"
    }
  }
]
```

### Models

**User**

- Fields:

  username: String, required

  email: String, required, unique

**PhoneNumberVerification**

- Fields:

  phone_number: String, required, unique

  auth_code: String, required

  referal_number: String, required, unique

  activated_referal_number: String, optional

  country_code: String, required

  user: User, optional

#### Serializers

**UserSerializer**

- Fields:

  username

  email

**PhoneNumberVerificationSerializer**

- Fields:

  phone_number

  auth_code

  referal_number

  activated_referal_number

  country_code

  user (read-only)

##### Views

**UserDetailAPIView**

**Description:** Retrieves the details of the authenticated user.

**ProfileRefgeralsAPIView**

**Description:** Retrieves the list of users who used the authenticated user's referral code.

**PhoneNumberVerificationCreateAPIView**

**Description:** Creates a phone number verification entry.
**PhoneNumberVerificationUpdateAPIView**

**Description:** Updates a phone number verification entry.

###### URL Configuration

**Endpoints:**

    api/profile-referals/: ProfileRefgeralsAPIView

    api/user/: UserDetailAPIView

    api/phone-number/create/: PhoneNumberVerificationCreateAPIView

    api/phone-number/update/<str:phone_number>/: PhoneNumberVerificationUpdateAPIView

    swagger/: Swagger UI for API documentation

###### Swagger Integration

Swagger is integrated for easy API documentation and testing. You can access the Swagger UI at the /swagger/ endpoint.
