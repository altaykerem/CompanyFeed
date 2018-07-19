# Company Feed

Receive weekly updates to your mail on most recently funded companies and add them to your trello to-do list to organize your research. 

## Table of contents
<!--ts-->
   * [Table of contents] (#Table-of-contents)
   * [Getting Started] (#Getting Started)
   * [Deployment] (#Deployment, Heroku)
      * [Dynos] (#Heroku – Dynos)
      * [Testing] (#Heroku – Testing)
      * [Envronment Variables] (#Heroku – Environment Variables)
<!--te-->

## Getting Started

You need to have a Mattermark, Trello, Firebase and Heroku accounts to run this project. You need python running on Heroku to recieve weekly mails. Also a web interface runs on Heroku for specifying query parameters. 

## Deployment, Heroku

Pipfile and package.json are needed for deployment in Heroku. This way it can install the dependencies to the virtual machine it uses.

### Heroku – Dynos

There are two dynos, one for periodic mails and the other for the web interface. Procfile commands as provided below;
```
clock: python main.py
web: npm start
```

### Heroku – Testing

Deploy the project to Heroku. From the command line run Heroku run bash –app daily-company-feed. This provides an SSH like connection the app. 
Mattermark sandbox configurations can be found in https://docs.mattermark.com/graphql_api/index.html. 

### Heroku – Environment Variables

**Mattermark API will expire after 1 year, check your plan in https://mattermark.com/app/account/api**
Before deploying the project check that the environment variables are set. 
```
mail_addr: Server email address
mail_pass: Server email password
firebase_cID: Firebase admin client ID
firebase_client_cert_url: Firebase admin client_x509_cert_url
firebase_private_key: Firebase admin private key
firebase_private_kID: Firebase admin private key ID
firebase_web_api: Firebase web API key
mm_api_key: Mattermark API key
mm_graphql_api: Mattermark request url
trello_api: Trello API key
trello_token: Trello token
trello_board: Trello board id
trello_list: Trello list id
```
