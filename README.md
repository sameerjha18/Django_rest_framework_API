# Django_Rest_Framework_API

#### Project Overview
The goal of this project is to develop a secure and efficient API system for user authentication using email and One-Time Password (OTP). This system will enable users to log in by providing their email address, receiving an OTP, and verifying the OTP to gain access.

#### Objectives
1. **User Authentication**: Create a seamless authentication process that uses email and OTP.
2. **Security**: Ensure the authentication process is secure and resilient against common threats such as brute-force attacks and unauthorized access.

#### Key Features
1. **Email Registration**:
   - Endpoint to register a new user with an email address.
   - Validate the email format and check for duplicates.

2. **OTP Generation and Sending**:
   - Endpoint to request an OTP.
   - Generate a secure OTP.
   - Send the OTP to the user's registered email address.

3. **OTP Verification**:
   - Endpoint to verify the OTP.
   - Authenticate the user if the OTP is valid and within the time limit.

4. **Session Management**:
   - Generate and manage user sessions upon successful OTP verification.
   - Provide secure session tokens for authenticated users.

#### API Endpoints

1. **User Registration**:
   - `POST /api/register`
     - Request: `{ "email": "user@example.com" }`
     - Response: `{ "message": "Registration successful. Please verify your email." }`

2. **Request OTP**:
   - `POST /api/send-otp`
     - Request: `{ "email": "user@example.com" }`
     - Response: `{ "message": "OTP sent to your email." }`

3. **Verify OTP**:
   - `POST /api/verify-otp`
     - Request: `{ "email": "user@example.com", "otp": "123456" }`
     - Response: `{ "message": "Login successful.", "token": "jwt_token" }`

