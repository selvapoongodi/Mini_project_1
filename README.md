# Mini_project_1
Client Query Management System: Organizing, Tracking, and Closing Support Queries

# Introduction
**Project:** Client Query Management Portal.

**Technologies:** Streamlit, MySQL, Python.

**Presenter:** Selvapoongodi U

# Problem Statement
The Client Query Management System aims to provide a real-time interface for clients to submit queries and for support teams to manage them efficiently. The system uses userlist in MySQL table to simulate initial query logs, stores them in MySQL, and displays/query/modify them using Streamlit dashboards. The primary goal is to enhance communication between clients and support agents, improve query resolution speed, and track query status and performance metrics.

# Business Use Cases:
**Query Submission Interface:** Allow clients to submit new queries in real-time.

**Query Tracking Dashboard:** Enable support teams to monitor and manage open/closed queries.

**Service Efficiency:** Measure how quickly support queries are resolved.

**Customer Satisfaction:** Faster query response leads to improved satisfaction.

**Support Load Monitoring:** Identify the most common types of queries and backlogs.

# Objective/Project Goal
Develop a secure, web-based, role-separated portal to streamline the submission and management of support queries.

**Client Goal:** Easy, instant query submission.

**Support Goal:** Clear, actionable queue management.

# Solution Architecture
## 3-Tier Architecture:
**Frontend** (Presentation Layer): Streamlit UI.

**Backend** (Application Logic): Python.

**Database** (Data Layer): MySQL (first_schema with user selva).

# Security
hashlib (SHA-256 for password hashing).

# Technical Implementation
## MySQL Database:
"userlist" table stores username, password_hash, and the key field role (client or support).
"queries" table created to submit the query raised by client and enable the support team to fetch and close the query.

## One-time hashing of passwords:
Text passwords from "userlist" table converted to hashed password (sql.ipynb)

## Secure authentication logic:
**Function:** validate_user(username, password, role):

1. Client password is run through hashlib.sha256().
2. The hashed value is compared to the password_hash column in the database table "userlist".
3. Access is granted only if all three parameters (username, hash, role) match.

## Session and Role Management
**Concept:** Streamlit's st.session_state is critical for continuity.

After login, we set: st.session_state.logged_in = True, st.session_state.role = role.

**Role Separation:** The entire UI logic is driven by simple if st.session_state.role == "client": blocks.

## Client Query Submission
Function: submit_new_query(query_data)

Query Type: INSERT statement.

## Support: Queue Management
**Function 1 (View):** fetch_open_queries() uses a SELECT statement: SELECT * FROM queries WHERE status='Open'.
The results are displayed cleanly using st.dataframe powered by Pandas.

**Function 2 (Action):** close_query(query_id) uses an UPDATE statement: Sets status='Closed' and records the exact closed_time.

# Live Demonstration
## Demo for Client workflow:
1. Login: Log in using a client credential.
2. Submit: Fill in heading, description, etc. (using new data).
3. Confirmation: Show the successful submission and the new Query ID.

## Demo for Support workflow:
1. Login: Log in using a support credential.
2. View Queue: Show the main table with the newly submitted query visible.
3. Close Query: Click "Close Query" and show the resulting table update (query disappears/status changes).

# Summary and Benefits
## Key Achievements:
**Security:** Successful use of password hashing.

**Efficiency:** Streamlined data entry (Client) and queue management (Support).

**Usability:** Intuitive, web-accessible interface via Streamlit.
