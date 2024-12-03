# Overview

This API allows you to manage phone number verifications and user referrals.</b>
It provides endpoints for creating and updating phone number verifications, retrieving user details, and listing referrals.</b>
[Swagger](#swagger-integration) is integrated for easy API documentation and testing.

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
**Method:** `PUT`</b>
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

**Endpoint - 1:** `/api/user/`
**Endpoint - 1:** `/api/user/<int:id>/`
**Method:** `GET`</b>
**Description:** `Retrieves the details of the authenticated user.`

**Response:**

```json
{
  "username": "user1",
  "email": "user1@example.com"
}
```

## User Referrals

**Endpoint - 1:** `/api/profile-referals/`
**Endpoint - 2:** `/api/profile-referals/<int:id>/`
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

- _Fields:_

  username: String, required

  email: String, required, unique

**PhoneNumberVerification**

- _Fields:_

  phone_number: String, required, unique

  auth_code: String, required

  referal_number: String, required, unique

  activated_referal_number: String, optional

  country_code: String, required

  user: User, optional

#### Serializers

**UserSerializer**

- _Fields:_

  username

  email

**PhoneNumberVerificationSerializer**

- _Fields:_

  phone_number

  auth_code

  referal_number

  activated_referal_number

  country_code

  user (read-only)

##### Views

**UserDetailAPIView**

_Description:_ Retrieves the details of the authenticated user.

**ProfileRefgeralsAPIView**

_Description:_ Retrieves the list of users who used the authenticated user's referral code.

**PhoneNumberVerificationCreateAPIView**

_Description:_ Creates a phone number verification entry.

**PhoneNumberVerificationUpdateAPIView**

_Description:_ Updates a phone number verification entry.

##### Swagger Integration

_Swagger is integrated for easy API documentation and testing. You can access the Swagger UI at the /swagger/ endpoint._
