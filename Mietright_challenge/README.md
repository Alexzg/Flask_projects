# Mietright code challenge
## Content
* [Challenge overview](#challenge-overview)
* [Languages/Frameworks](#languages-and-frameworks)
* [Directory structure](#directory-structure)
* [Code overview](#code-overview)
  * [Burgeramt app](#burgeramt-app)
  * [Signaturit app](#signaturit-app)
  * [Database](#database)
  * [Console commands](#console-commands)
  * [Email configuration](#email-configuration)
  * [Tests](#tests)

## Challenge overview
- User is just an email
- After registration, will be connected to a service called "signaturit"
- An email will be sent from "signaturit" including:
  - Greeting
  - Logo
  - Button to redirect the user to sign a document

## Languages and Frameworks
### (Python has been used for the backend, in order to make future Machine Learning implementation easier to be intruduced)
- Python (Flask, Flask-mail, jwt)
- React
- HTML
- Bootstrap
- SQL (SQLite)

## Directory structure
```bash
│   README.md
│   requirements.txt
│
├───burgeramt
│   │   auth.py
│   │   db.py
│   │   schema.sql
│   │   __init__.py
│   │
│   └───templates
│       ├───auth
│       │       register.html
│       │
│       └───signaturit
│               welcome.html
│
├───instance
│       burgeramt_config.py
│       signaturit_config.py
│
└───signaturit
    │   auth.py
    │   mail.py
    │   signaturit.py
    │   __init__.py
    │
    └───static
        ├───documents
        │       Muster_Schutzbrief_Mieterhöhung.pdf
        │
        ├───images
        │   │   logo_200_200.png
        │   │
        │   └───templates
        │       └───error
        │               error_404.png
        │
        └───templates
            ├───error
            │       error_404.html
            │
            ├───form
            │       main_form.html
            │
            └───mail
                    mail_not_sent.html
                    mail_sent.html
                    message.html
```

## Code overview
There are two different apps. The apps are produced by Factories and Blueprints using Flask(Python) for Backend.
React and Bootstrap are only implemented on "Signaturit", only in two rendered '.html' files as a suggestion.
Both are included using 'CDN links', to minimize the complexity needed in order to use them together with the Backend.
- The "Burgeramt" creates a database for saving the email of a user. 
- The "Signaturit" is the main app.

  ### Burgeramt app
  * Create an 'sqlite' database (User & Document tables, but the latter is not used for now)
  * Register a User
  * Check if User already exists

  ### Signaturit app
  #### (It is considered as a fact that the service will be triggered by another application)
  * Read the URL: .../token/mail
  * Exctract from 'token' the 'User's email' and Send the email (the email includes a button for redirection)
  * The User is redirected to 'URL: .../token/form' when presses the button included in the email
  * From there, two options are available to the User:
   * Download the document
   * Upload an image of the document with signature
  
  ### Database
  #### (Currently only used for the [Burgeramt app](#burgeramt-app))
  * For simplicity the sqlite has been used, because no configuration is needed (it works ok for small applications).
  * Table 1: User
  * Table 2: Document (Not used in apps currently)
  
  ### Console Commands
  #### (Windows)
  * Create and Activate Virtual Environment
  * Install python dependencies from 'requirements.txt'
  * Run Flask app:
    * cmd: ...projectFilePath>set FLASK_APP=signaturit <i>or</i> set FLASK_APP=burgeramt
    * cmd: ...projectFilePath>set FLASK_ENV=development
    * cmd: ...projectFilePath>flask run
    * (For production, these commands do not imply. 'flask run' starts a server that is not secure)
  * Initialize database
    * cmd: flask init-db
    
  ### Email configuration
  * instance/signaturit_config.py
  * signaturit/mail.py
  
  ### Tests
  #### (No automatic tests until now)
  * <b>test Token</b>: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InVzZXJAZG1uZG1uLmNvbSJ9.19AapUepRB9q61XuRhDN9WoYbE32JDzA4lSnuU2v_AA
    * the encoded user email = 'user@dmndmn.com'
  * <b>test URL</b>: .../signaturit/token/mail 
    * Send email
    * Because the html data loaded to the email do not exist online, images cannot be displayed from email providers)
  * <b>test URL</b>: .../signaturit/token/form 
    * UI for download/upload
  * <b>test any wrong_URL</b>: error 404 page
