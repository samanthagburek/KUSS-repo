# User Requirements

## Already Completed

- Working endpoints for people, roles, text, journal titles
- Working referee review flow through the manuscripts
- Start of a GUI the basic skeleton

## General

- The journal will have:
    - A title
    - A masthead page
    - An about page
    - A submissions guidelines page

## People

- Submitting a manuscript creates an account with the role of author.
	- Prepare database with account information and create endpoints for submitting manuscript
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
- Also the journal title can be edited.
- These texts can be edited from the client application, but only by the editor and managing editor(s).

## Manuscripts

- Manuscripts can flow through the system according to [this chart](https://github.com/AthenaKouKou/journal/blob/main/docs/Manuscript_FSM.jpg).
- A dashboard will present the manuscripts in visual form.
- Only the editor and managing editor(s) see all manuscripts; everyone else only sees "their own." That means
    manuscripts for which they are the author or referee.