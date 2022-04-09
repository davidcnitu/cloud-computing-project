# cloud-computing-project
ECS781P Cloud Computing Mini Project

## Project Demonstration
https://www.youtube.com/watch?v=MJDKouYt0g0

## Project Description

The purpose of this project is to provide a RESTful API service. Our service allows users to perform the basic CRUD functionality to retrieve, create, update, and delete products stored in the database. The products will consist of a product id, a colour attribute, and a price attribute, and the user also has the option to add additional attributes of their choosing thanks to our schemeless database. The service also offers a health check, that is connected to an external API. When a health check is performed, the service should return a status code 200 if healthy, as well as fetch a product via an external API. While this is a contrived example, it demonstrates how one would use such a service to interact with an external API. The client will send a request to the following URL:
https://e4dlouavza.execute-api.us-east-1.amazonaws.com/prod
with one of the three endpoint, a /product path, and a /products path, and a /health path. To get, update, delete, or create an individual product, the user should send the client request to the /product path, and to retrieve all product, they should send the request to the /products. It is worth noting that in order to retrieve all products within the database, the user must be authenticated using an AWS Cognito User Pool authentication token. They can obtain the authentication token by signing up to the service using the following link:
https://ecs781pgroup1.auth.us-east-1.amazoncognito.com/login?client_id=3gek6r2mh1n9dbgc720jlr8585&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https://example.com/callback
For post requests, API accepts JSON for the body of the request, and the API also returns JSON for all responses.
Furthermore, the API has been secured by https.

## System Architecture 

This project was implemented using Amazon Web Services’ (AWS) serverless architecture, with the Lambda functions being the core logic for this architecture. We used DymamoDB for the database, AWS Identity and Access Management (IAM) for adding role-based policies, Cognito user pool for user authentication, and API gateway as an API management tool that sits between the client and the backend services. Please refer to the diagram below to see the flow of the architecture.

![Cloud project diagram](https://user-images.githubusercontent.com/76735699/162539184-27d54528-b2a3-4ba4-87ff-715365594d33.png)

## How to Use the Project

This service can be used most effectively through Postman.

The URL to send a request to / to use this API is as follows:
https://e4dlouavza.execute-api.us-east-1.amazonaws.com/prod

In order to retrieve all products from the database, you must include an authentication token from the header. To obtain an authentication token, please sign up or login using the following link:
https://ecs781pgroup1.auth.us-east-1.amazoncognito.com/login?client_id=3gek6r2mh1n9dbgc720jlr8585&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https://example.com/callback

Once signed in, the id token and the access token can be found in the URL parameters, with an example highlighted below (please note the id token and access token that are used are invalid and used for demonstration purposes only):

https://example.com/callback#id_token=eyJraWQiOiJUYXhPS2lvUU5OcTlqOThWWlBjaGc2OWgwMVBORERpQUhvOXFCU1JvOFVjPSIsImFsZyI6IlJTM&access_token=eyJraWQiOiJkRnpmVUlZM2lxTkRwdythbURKTHpWNzFtY0EwcEQ5cDB6TXUwc0dFRW5FPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI3MzhjODgyMy1hMzBjLTRlNTctO&expires_in=3600&token_type=Bearer

Once you have retrieved the access token, insert it into the header under the key “Authorization”. Please see image below for an example of how to do this on Postman:

<img width="800" alt="postman_header" src="https://user-images.githubusercontent.com/76735699/162539825-0ecc7bba-23ad-42b8-89ba-b61a438ace6e.png">

The API accepts JSON for the body of the post request and returns JSON in the response for all other requests.

All available requests with their respective endpoints are displayed below:

Health Check: <GET /Health/> Description: Performs a health check and external REST API interaction

Get Products: <GET /Products/> Description: Fetches all products from the database

Get Product: <GET /Product/:id/> Description: Fetches a product with ID number from the database

Update Product <PATCH /Product/:id/> Description: Updates a product in the database

Delete Product <DELETE /Product/:id/> Description: Deletes a product from the database

Create Product <POST /Product/> Description: Creates a new product in the database

An example of the type of body to use in the POST request can be seen below:

<img width="800" alt="postman_body" src="https://user-images.githubusercontent.com/67503181/162568821-47f8453a-3a43-49f4-9faa-4260e9437f67.png">

## Credits
[Chris Hui](https://github.com/chrishui)

[Yusuf Sindi](https://github.com/yysindi)

[Fanging Tan](https://github.com/fangningtan)

[David Nitu](https://github.com/davidcnitu)


