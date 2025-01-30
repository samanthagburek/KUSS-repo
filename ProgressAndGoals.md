# User Requirements

## Already Completed

- Working endpoints for people, roles, text, journal titles using CRUD functionality
- Working referee review flow through the manuscripts
- Set up database both locally, and in the cloud
- Deployed in Python Anywhere
- Start of a GUI the basic skeleton

## General

- The journal will have:
    - A title
    - A masthead page
    - An about page
    - A submissions guidelines page
		- Submission guideline providing authors w/ submission instructions including plagiarism policies

## People

- Submitting a manuscript creates an account with the role of author.
	- Prepare database with account information and create endpoints for submitting manuscript
	- Will implement to assign the role of author when creating account.
- Users can edit and delete their own accounts.
	- Create endpoints for updating account info and deleting, making sure to verify authenticity
- Assigning a referee to a manuscript adds the referee role to that person.
	- Prepare sections in database for referees, create referee endpoints and permissions.
- Only the editor and managing editor(s) have create / update / delete permissions for the accounts of others.
	- Add signing in, account authentication, and ensure only certain roles have permissions.
- Advanced: record a history of each user's interactions with the system.
	- Create a table with columns for user, action, and timestamp
- A listing of all people is available, but only to the editor and managing editor(s).
	- Endpoint to fetch people, only available upon successful authentication
- A journal masthead can be generated from the database and displayed by the frontend.
	- We use REACT to prepare a frontend and ensure proper integration between frontend and backend.

## Text

- All large runs of text in the system, such as "About this Journal" or "Submission Guidelines,"
    are stored in the database.
  	- Designated entries in Text database for large texts, with editor/managing editor(s) having WRITE permission
- Also the journal title can be edited.
	- Endpoint to edit journal title, permission to view/use endpoint given only to journal admin, i.e. editor
- These texts can be edited from the client application, but only by the editor and managing editor(s).
	- Frontend feature to access and edit texts, integrated with backend and database, while authenticating users. Ideally, frontend feature is only visible after authentication.

## Manuscripts

- Manuscripts can flow through the system according to [this chart](https://github.com/AthenaKouKou/journal/blob/main/docs/Manuscript_FSM.jpg).
	- Follow manuscript flow chart using functions, checking user status for certain actions.
- A dashboard will present the manuscripts in visual form.
	- Frontend dashboard that displays manuscripts along with their metadata and status, using REACT and connecting with manuscript database
- Only the editor and managing editor(s) see all manuscripts; everyone else only sees "their own." That means
    manuscripts for which they are the author or referee.
	- After user authentication, filter manuscripts from database by author / referee


## More Goals

- Encryption for sensitive data
- Automated email for changes in review (acceptance/rejection) 