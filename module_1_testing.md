# Module 1 – Authentication Testing

## 1. Server Start Test

The FastAPI server was started successfully and the root endpoint was tested from PowerShell.

### Command

```powershell
curl.exe http://127.0.0.1:8000/
```

### Result

```json
{"message":"Session Authentication API is running"}
```

**Status: PASS**

---

## 2. User Registration Test

A new user was registered using the `/auth/register` endpoint.

### Command

```powershell
$body = @{
    name = "Gayatri"
    email = "gayatri@test.com"
    password = "Test@123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/register" -Method Post -ContentType "application/json" -Body $body
```

### Result

```text
Registration successful
User:
ID = 1
Name = Gayatri
Email = gayatri@test.com
Role = user
```

**Status: PASS**

---

## 3. Login Test – Valid Credentials

The registered user was tested with the correct email and password.

### Command

```powershell
$loginBody = @{
    email = "gayatri@test.com"
    password = "Test@123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/login" -Method Post -ContentType "application/json" -Body $loginBody
```

### Result

```text
Login successful
User:
ID = 1
Name = Gayatri
Email = gayatri@test.com
Role = user
```

**Status: PASS**

---

## 4. Login Test – Invalid Password

Negative testing was performed by providing an incorrect password.

### Command

```powershell
$loginBody = @{
    email = "gayatri@test.com"
    password = "WrongPassword"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/login" -Method Post -ContentType "application/json" -Body $loginBody
```

### Result

```text
Invalid email or password
```

**Status: PASS – Invalid credentials correctly rejected**

---

## 5. Module 1 Testing Summary

| Test Case         | Expected Result                           | Status |
| ----------------- | ----------------------------------------- | ------ |
| Server Start      | API should be running                     | PASS   |
| User Registration | User should be registered successfully    | PASS   |
| Valid Login       | User should be authenticated successfully | PASS   |
| Invalid Login     | Incorrect credentials should be rejected  | PASS   |

## Conclusion

Module 1 Registration and Login functionality has been successfully implemented and tested using PowerShell. Both valid and invalid authentication scenarios were verified successfully.
