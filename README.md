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

**Mattermark API will expire after 1 year,** check your plan in https://mattermark.com/app/account/api.
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

## Database
Used Firebase Cloud Firestore as the database. Firestore is based on collections and documents to store data as NoSQL. The database contains users, parameters and projects functions. Collections are “runtime” and “users”. For “runtime” there are two documents “functionalities” and “parameters”. Fields under “functionalities” are used to as a switch (ex. trello: false would shut the trello assignments). Fields under “parameters” are used for customizing queries. The collection “users” contains the mails of the recipients.

### Database – Python worker
Firebase admin credentials are needed to run. Database elements are available as dictionaries from [/Database/firebase_db_conn.py]( Database/firebase_db_conn.py ).

### Database-Web
Firebase Web API is needed. [/DBServer/index.html]( DBServer/index.html ) connects to Firebase to as a web interface to change values inside “parameters”. 

### Mailing
A google mail is needed for sending mails. [/Mailling/send_mail.py](Mailing/send_mail.py) is responsible the responsible file. Pulls the mailing information from the file query_results.txt. 

### How to add information to Mail
Html mails relies on having nested tables to form the mail. [/Mailing/mail_form_adapter.py](Mailing/mail_form_adapter.py) contains the class MailAdapter to form the html table form. 
Example usage; 
```
mail_adaptor = mailing.MailAdapter()
mail_adaptor.open_file("query_results.txt")
mail_adaptor.open_table(<table title>, 5)
mail_adaptor.open_row()
mail_adaptor.add_header_data(<element>, 5)
columns = ["col1", "col2", "col3", "col4", "col5"]
mail_adaptor.add_row_data(columns)
values = ["va1", "val2", "val3", "val4", "val5"]
mail_adaptor.add_row_data(values)
mail_adaptor.close_row()
mail_adaptor.close_table()
mail_adaptor.close_file()
```

### Mattermark
Uses the GraphQL API and MSFL for querying over Mattermark. Refer to https://docs.mattermark.com/graphql_api/schema/index.html and https://docs.mattermark.com/graphql_api/msfl/index.html for more information about the API.  Query.py is a parent class that indicates which company information is going to be retrieved. It should be extended by a class that calls its base_query(msfl) method with the filtering and sorting information indicated by the MSFL structure. 

### Trello
Specify Trello API as well as board and list ID’s for using Trello assignments. To get the ID’s, go to your board url and type .json (such as https://trello.com/b/ZpEiFgBX/board.json). Id is the ID of the board and you can navigate through the lists field for the list id. 

### Logging
Logs are kept in a file called log, you can call the log function from utils. 
