# TitanicMessage 3.0

TitanicMessage 3.0 is hosted at http://titanicmessage.ddns.net
[PRODUCTION]
and http://uukelele.ddns.net:1234
[DEBUG]


# API Reference

**Base URL:** `/api`

**All 401 Errors will always be:**

```{"error": "unauthenticated"}```

## USER DATA
**URL:** `/api/users/<user_id>`

**Description:** Returns data about the given user in JSON format. Can be accessible by anyone, without authentication.

**Request Type:** `GET`

**Possible Response Codes:** `200`

**Sample Response:**

```
{
  "friends": [ "list of IDs in string format of each friend" ],
  "id": " user id ",
  "pending": [ "list of IDs in string format of each pending friend requester" ],
  "username": "username"
}
```

## GET USER ID BY USERNAME
**URL:** `/api/get_user_id/<username>`

**Description:** Returns the ID of the given user. The get_username_by_id is included with `/api/users/<user_id>` (see above)

**Request Type:** `GET`

**Possible Response Codes:** `200`

**Sample Response:**

```
{
  "id": "user id"
}
```


## SEND FRIEND REQUEST
**URL:** `/api/users/<id>/send_request`

**Description:** Sends a friend request to the user with given ID.

**Request Type:** `POST`

**Possible Response Codes:** `200, 401`

**Sample Body:**

```
{
  "username": "username",
  "password": "password"
}
```

**Sample Response:**

```
{"message":"request sent"}
```


## ACCEPT FRIEND REQUEST
**URL:** `/api/users/<id>/accept_request`

**Description:** Accepts any friend request sent by the user with the given ID.

**Request Type:** `POST`

**Possible Response Codes:** `200, 401`

**Sample Body:**

```
{
  "username": "username",
  "password": "password"
}
```

**Sample Response:**

```
{"message":"OK"}
```



## REJECT FRIEND REQUEST
**URL:** `/api/users/<id>/reject_request`

**Description:** Rejects any friend request sent by the user with the given ID.

**Request Type:** `POST`

**Possible Response Codes:** `200, 401`

**Sample Body:**

```
{
  "username": "username",
  "password": "password"
}
```

**Sample Response:**

```
{"message":"OK"}
```
