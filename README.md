# Endpoints

• `[/api/phone-number/create/](#/api/phone-number/create/)`

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

### Update Phone Number Verification

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
