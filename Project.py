
import streamlit as st
import mysql.connector as db
from mysql.connector import Error 
import hashlib
import pandas as pd
from datetime import datetime

# ------------------------------- HASH PASSWORD -------------------------------
def hash_password(password):
    """Return SHA-256 hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------------------- DB CONNECTION -------------------------------
def get_db():
    return db.connect(
        host="localhost",
        user="selva",
        password="guru",
        database="first_schema"
    )

# ------------------------------- VALIDATE USER -------------------------------
def validate_user(username, password, role):
    """Check if username, hashed password, and role exist in the database"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    hashed = hash_password(password)

    query = """
        SELECT * FROM userlist
        WHERE username = %s AND password_hash = %s AND role = %s
    """
    cursor.execute(query, (username, hashed, role))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result

# ------------------------------- SUBMIT QUERY (CLIENT) -------------------------------
def submit_new_query(query_data):
    """
    Submits a new query record to the 'queries' table using MySQL.
    
    The connection is handled inside the function to be robust to Streamlit reruns.
    
    :param query_data: A dictionary containing the query details.
    """
    # Note the use of %s placeholders for parameterization
    sql_query = """
        INSERT INTO queries 
        (username, email, mobile, heading, description, status, created_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    # Prepare the data tuple in the correct order for the placeholders
    data_tuple = (
        query_data['username'],
        query_data['email'],
        query_data['mobile'],
        query_data['heading'],
        query_data['description'],
        query_data['status'],
        query_data['created_time'] # Formatted as a string
    )

    conn = None # Initialize outside try block
    try:
        conn = get_db() # Get connection inside the function
        cursor = conn.cursor()
        cursor.execute(sql_query, data_tuple)
        conn.commit()
        last_id = cursor.lastrowid
        print(f"\n✅ Query submitted successfully!")
        print(f"New Query ID: {last_id}")
        return last_id
    except Error as e:
        print(f"\n❌ Error submitting query: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        # Always close the cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ------------------------------- FETCH OPEN QUERIES (SUPPORT) -------------------------------
def fetch_open_queries():
    """Return all open queries as a pandas DataFrame"""
    conn = get_db()
    df = pd.read_sql("SELECT * FROM queries WHERE status='Open' ORDER BY id DESC", con=conn)
    conn.close()
    return df

# ------------------------------- CLOSE QUERY (SUPPORT) -------------------------------
def close_query(query_id):
    """Mark a query as closed"""
    conn = get_db()
    cursor = conn.cursor()
    closed_time = datetime.now()
    cursor.execute(
        "UPDATE queries SET status='Closed', closed_time=%s WHERE id=%s",
        (closed_time, query_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

 # =============================================================================
def logout():
    """Reset session state and rerun"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    # We clear all other session state variables related to the app as well
    st.session_state.pop("email", None)

# =============================================================================
# 8. STREAMLIT UI + SESSION STATE SETUP
# =============================================================================
st.title("Client Query Self-Portal 🎫")

# ---- Initialize Session State ----
default_state = {
    "logged_in": False,
    "username": None,
    "role": None
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =============================================================================
# 9. LOGIN PAGE
# =============================================================================
if not st.session_state.logged_in:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", ["client", "support"])

    if st.button("Login"):
        user = validate_user(username, password, role)

        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username, password, or role.")

# =============================================================================
# 10. MAIN APP (After Login)
# =============================================================================
else:
    username = st.session_state.username
    role = st.session_state.role

    col1, col2 = st.columns([6, 1])
    col1.success(f"Welcome {username}! You are logged in as {role}")
    col2.button("Logout", on_click=logout)

    st.markdown("---")

    # =========================================================================
    # 10A. CLIENT PANEL
    # =========================================================================
    if role == "client":
        st.header("Client Panel - Submit a Query")
        st.write(f"Logged in as: **{username}**") 
        email = st.text_input("Email ID (Required for response)")
        mobile = st.text_input("Mobile Number (Optional)")
        heading = st.text_input("Type a suitable heading")
        description = st.text_area("Enter your query details")
        
        if st.button("Submit Query"):
            if not email.strip():
                st.warning("Email ID is required!")
            elif not heading.strip():
                st.warning("Heading is required!")
            elif not description.strip():
                st.warning("Query description cannot be empty!")
            else:
                query_data = {
                    'username': username,
                    'email': email,
                    'mobile': mobile,
                    'heading': heading,
                    'description': description,
                    'status': 'Open', # Set initial status
                    'created_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                query_id = submit_new_query(query_data)
                
                if query_id:
                    st.success(f"Query submitted successfully! Your tracking ID is: **{query_id}**")
                    st.balloons()
                else:
                    st.error("Failed to submit query. Check the database connection/logs.")


    # =========================================================================
    # 10B. SUPPORT PANEL
    # =========================================================================
    elif role == "support":
        st.header("Support Panel - View & Close Open Queries")

        df_queries = fetch_open_queries()

        if df_queries.empty:
            st.info("No open queries.")
        else:
            # Display relevant columns
            st.dataframe(df_queries[['id', 'username', 'heading', 'created_time', 'status', 'description', 'email', 'mobile']])

            query_id_options = [0] + df_queries['id'].tolist()
            # Default to 0 (Select an option)
            query_id = st.selectbox("Select Query ID to close", query_id_options) 

            if st.button("Close Query") and query_id != 0:
                if query_id in df_queries['id'].values:
                    close_query(query_id)
                    st.success(f"Query {query_id} marked as closed!")
                    st.rerun() # Refresh the page to show the updated table
                else:
                    st.error("Invalid Query ID selected!")