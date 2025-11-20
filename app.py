import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Freelancer Platform",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Updated to match screenshot
st.markdown("""

    <style>

    /* MAIN CONTAINER (light lavender background) */

    .main {

        padding: 0rem 1rem;

        background-color: #f6f0fb;

    }



    /* SIDEBAR */

    [data-testid="stSidebar"] {

        background-color: #f3ebfc !important;

    }

    [data-testid="stSidebar"] > div:first-child {

        padding: 2rem 1rem;

    }



    /* NAVIGATION HEADER */

    .sidebar-title {

        color: #5a5a5a;

        font-size: 0.9rem;

        font-weight: 600;

        text-transform: uppercase;

        letter-spacing: 0.5px;

        margin-bottom: 1.5rem;

    }



    /* USER AVATAR */

    .user-avatar {

        width: 50px;

        height: 50px;

        border-radius: 50%;

        background: linear-gradient(135deg, #c6a7f3, #a685e2);

        display: flex;

        align-items: center;

        justify-content: center;

        color: white;

        font-size: 1.5rem;

        font-weight: 600;

        margin: 0 auto 1rem;

    }



    .user-name {

        text-align: center;

        font-size: 1.1rem;

        font-weight: 600;

        color: #2d2d2d;

        margin-bottom: 0.3rem;

    }

    .user-role {

        text-align: center;

        font-size: 0.85rem;

        color: #666;

    }



    /* BUTTONS (light purple gradient) */

    .stButton>button {

        width: 100%;

        background: linear-gradient(135deg, #a685e2, #c6a7f3);

        color: white;

        border-radius: 8px;

        padding: 0.6rem 1rem;

        margin: 0.5rem 0;

        border: none;

        font-weight: 500;

        transition: all 0.3s ease;

    }

    .stButton>button:hover {

        transform: translate(-2px);

        box-shadow: 0 4px 12px rgba(166, 133, 226, 0.4);

    }



    /* INPUT FIELDS */

    .stTextInput>div>div>input,

    .stTextArea>div>div>textarea,

    .stNumberInput>div>div>input {

        border-radius: 8px;

        border: 1px solid #ddd;

        padding: 0.75rem;

        background-color: #fff;

    }



    /* HEADER CARD */

    .welcome-header {

        background: #ffffff;

        padding: 2rem 2.5rem;

        border-radius: 12px;

        margin-bottom: 2rem;

        box-shadow: 0 2px 8px rgba(0,0,0,0.05);

    }

    .welcome-header h1 {

        color: #3a2b63;

        font-size: 2.5rem;

        font-weight: 700;

        margin-bottom: 0.5rem;

    }

    .welcome-header p {

        color: #8b78b3;

        font-size: 1.1rem;

        margin: 0;

    }



    /* TABS */

    .stabs [data-baseweb="tab-list"] {

        gap: 1rem;

        background-color: transparent;

    }

    .stabs [data-baseweb="tab"] {

        background-color: #eadef9;

        border-radius: 8px;

        padding: 0.75rem 1.5rem;

        color: #6b5d9a;

        font-weight: 500;

        border: none;

    }

    .stabs [aria-selected="true"] {

        background: #c6a7f3;

        color: white;

    }



    /* CONTENT CARDS */

    .content-card {

        background: white;

        padding: 2rem;

        border-radius: 12px;

        box-shadow: 0 2px 8px rgba(0,0,0,0.05);

        margin-bottom: 1.5rem;

    }

    .content-card h2, .content-card h3 {

        color: #3a2b63;

        margin-bottom: 1rem;

    }



    /* PROJECT CARDS */

    .project-card {

        background-color: #faf7ff;

        padding: 1.5rem;

        border-radius: 10px;

        margin: 1rem 0;

        border: 1px solid #e1d6f5;

    }



    /* FORM SECTION */

    .form-section {

        background: white;

        padding: 2rem;

        border-radius: 12px;

        margin-top: 1rem;

        box-shadow: 0 2px 8px rgba(0,0,0,0.05);

    }

    .form-section h3 {

        color: #3a2b63;

        font-size: 1.5rem;

        margin-bottom: 0.5rem;

    }

    .form-section .subtitle {

        color: #8a7ea7;

        font-size: 0.95rem;

        margin-bottom: 2rem;

    }



    label {

        color: #3a2b63 !important;

        font-weight: 500 !important;

    }

    </style>

    """, unsafe_allow_html=True)

# --- Database Connection ---
def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Jahnavi21",
        database="freelancer_database"
    )

# --- Session State ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None

# --- Database Functions (Keeping all existing functions) ---

def login(email, password, user_type):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    clean_email_input = email.strip().lower()
    
    try:
        if user_type == "client":
            cursor.execute("""
                SELECT client_id as user_id, name as username, 'client' as user_type, password
                FROM Clients 
                WHERE TRIM(LOWER(email)) = %s
            """, (clean_email_input,))
        elif user_type == "freelancer":
            cursor.execute("""
                SELECT freelancer_id as user_id, name as username, 'freelancer' as user_type, password
                FROM Freelancers 
                WHERE TRIM(LOWER(email)) = %s
            """, (clean_email_input,))
        else:
            cursor.execute("""
                SELECT admin_id as user_id, name as username, 'admin' as user_type, password
                FROM Admins 
                WHERE TRIM(LOWER(email)) = %s
            """, (clean_email_input,))
        
        user = cursor.fetchone()
        if user and user['password'] == password:
            return user
        else:
            return None
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def register_user(name, email, password, phone_number, user_type, company_name=None):
    conn = get_database_connection()
    cursor = conn.cursor()
    clean_email = email.strip().lower()
    
    try:
        if user_type == 'client':
            cursor.execute("""
                INSERT INTO Clients (name, company_name, email, phone_number, password)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, company_name, clean_email, phone_number, password))
        else:
            cursor.execute("""
                INSERT INTO Freelancers (name, email, phone_number, password)
                VALUES (%s, %s, %s, %s)
            """, (name, clean_email, phone_number, password))
        
        conn.commit()
        success = True
        message = "Registration successful! 🎉 Please login."
    except mysql.connector.Error as err:
        success = False
        message = f"Registration failed: {err}"
    
    cursor.close()
    conn.close()
    return success, message

def create_project(client_id, title, description, budget, deadline):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Projects (client_id, title, description, budget, deadline, status)
            VALUES (%s, %s, %s, %s, %s, 'open')
        """, (client_id, title, description, budget, deadline))
        conn.commit()
        success = True
        message = "Project created successfully! 🚀"
    except mysql.connector.Error as err:
        success = False
        message = f"Failed to create project: {err}"
    cursor.close()
    conn.close()
    return success, message

def get_projects(status=None):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT p.*, c.name as client_name, 
               DATE_FORMAT(p.deadline, '%Y-%m-%d') as formatted_deadline
        FROM Projects p
        JOIN Clients c ON p.client_id = c.client_id
    """
    params = ()
    
    if status:
        query += " WHERE p.status = %s"
        params = (status,)
        
    query += " ORDER BY p.deadline DESC"
    
    cursor.execute(query, params)
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return projects

def call_sp_get_client_projects(client_id):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Call the stored procedure
        cursor.callproc('sp_GetClientProjects', (client_id,))
        
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
            
        # Manually format the deadline to match what the old function did
        for res in results:
            if 'deadline' in res and res['deadline']:
                res['formatted_deadline'] = res['deadline'].strftime('%Y-%m-%d')
        return results
        
    except mysql.connector.Error as err:
        st.error(f"Error calling sp_GetClientProjects: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def call_fn_get_project_app_count(project_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        # Call the SQL function
        cursor.execute("SELECT fn_get_project_app_count(%s)", (project_id,))
        count = cursor.fetchone()[0]
        return count
        
    except mysql.connector.Error as err:
        st.error(f"Error calling fn_get_project_app_count: {err}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_all_skills():
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT skill_name FROM Skills ORDER BY skill_name")
        skills = [row['skill_name'] for row in cursor.fetchall()]
        return skills
    except mysql.connector.Error as err:
        st.error(f"Error fetching skills: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def call_sp_get_freelancers_by_skill(skill_name):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('sp_GetFreelancersBySkill', (skill_name,))
        
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
            
        return results
        
    except mysql.connector.Error as err:
        st.error(f"Error calling sp_GetFreelancersBySkill: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_all_freelancers():
    """[NEW] Gets a list of all freelancers to populate a dropdown."""
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT freelancer_id, name FROM Freelancers ORDER BY name")
        freelancers = cursor.fetchall()
        return freelancers
    except mysql.connector.Error as err:
        st.error(f"Error fetching freelancers: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def call_fn_has_skill(freelancer_id, skill_name):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        # Call the SQL function and get the boolean result
        cursor.execute("SELECT fn_HasSkill(%s, %s)", (freelancer_id, skill_name))
        has_skill = cursor.fetchone()[0]
        return bool(has_skill) # Convert 1/0 to True/False
        
    except mysql.connector.Error as err:
        st.error(f"Error calling fn_HasSkill: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_freelancers_with_ratings():
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT freelancer_id, name, average_rating FROM Freelancers ORDER BY name")
        freelancers = cursor.fetchall()
        return freelancers
    except mysql.connector.Error as err:
        st.error(f"Error fetching freelancers: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def submit_proposal(project_id, freelancer_id, proposal_text, bid_amount):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Applications (project_id, freelancer_id, proposal_text, bid_amount, status)
            VALUES (%s, %s, %s, %s, 'pending')
        """, (project_id, freelancer_id, proposal_text, bid_amount))
        conn.commit()
        success = True
        message = "Proposal submitted successfully! 🎯"
    except mysql.connector.Error as err:
        success = False
        message = f"Failed to submit proposal: {err}"
    cursor.close()
    conn.close()
    return success, message

def get_applications_for_project(project_id):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, f.name as freelancer_name, f.email as freelancer_email
        FROM Applications a
        JOIN Freelancers f ON a.freelancer_id = f.freelancer_id
        WHERE a.project_id = %s
    """, (project_id,))
    applications = cursor.fetchall()
    cursor.close()
    conn.close()
    return applications

def update_application_status(application_id, status):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Applications SET status = %s WHERE application_id = %s", (status, application_id))
        conn.commit()
        success = True
    except mysql.connector.Error as err:
        st.error(f"DB Error: {err}")
        success = False
    cursor.close()
    conn.close()
    return success

def update_project_on_hire(project_id, freelancer_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Projects 
            SET status = 'in_progress' 
            WHERE project_id = %s
        """, (project_id,))
        conn.commit()
        
        cursor.execute("""
            UPDATE Applications 
            SET status = 'rejected' 
            WHERE project_id = %s AND status = 'pending'
        """, (project_id,))
        conn.commit()
        success = True
    except mysql.connector.Error as err:
        st.error(f"DB Error: {err}")
        success = False
    cursor.close()
    conn.close()
    return success

def get_my_applications(freelancer_id):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.proposal_text, a.bid_amount, a.status, p.title as project_title
        FROM Applications a
        JOIN Projects p ON a.project_id = p.project_id
        WHERE a.freelancer_id = %s
        ORDER BY a.application_id DESC
    """, (freelancer_id,))
    applications = cursor.fetchall()
    cursor.close()
    conn.close()
    return applications

def get_freelancer_skills(freelancer_id):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.skill_name, fs.experience_years
        FROM Freelancer_Skills fs
        JOIN Skills s ON fs.skill_id = s.skill_id
        WHERE fs.freelancer_id = %s
    """, (freelancer_id,))
    skills = cursor.fetchall()
    cursor.close()
    conn.close()
    return skills

def add_freelancer_skill(freelancer_id, skill_name, experience_years):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT IGNORE INTO Skills (skill_name) VALUES (%s)", (skill_name,))
        conn.commit()
        
        cursor.execute("SELECT skill_id FROM Skills WHERE skill_name = %s", (skill_name,))
        skill_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO Freelancer_Skills (freelancer_id, skill_id, experience_years)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE experience_years = %s
        """, (freelancer_id, skill_id, experience_years, experience_years))
        
        conn.commit()
        success = True
        message = f"Skill '{skill_name}' added/updated!"
    except mysql.connector.Error as err:
        success = False
        message = f"Failed to add skill: {err}"
    cursor.close()
    conn.close()
    return success, message

def remove_freelancer_skill(freelancer_id, skill_name):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE fs
            FROM Freelancer_Skills fs
            JOIN Skills s ON fs.skill_id = s.skill_id
            WHERE fs.freelancer_id = %s AND s.skill_name = %s
        """, (freelancer_id, skill_name))
        conn.commit()
        success = True
        message = f"Skill '{skill_name}' removed."
    except mysql.connector.Error as err:
        success = False
        message = f"Failed to remove skill: {err}"
    cursor.close()
    conn.close()
    return success, message

def get_my_active_projects(freelancer_id):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.project_id, p.title, c.name as client_name, p.status
        FROM Projects p
        JOIN Applications a ON p.project_id = a.project_id
        JOIN Clients c ON p.client_id = c.client_id
        WHERE 
            a.freelancer_id = %s 
            AND a.status = 'accepted'
            AND (p.status = 'in_progress' OR p.status = 'pending_approval')
    """, (freelancer_id,))
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return projects

def mark_project_for_approval(project_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Projects SET status = 'pending_approval' 
            WHERE project_id = %s AND status = 'in_progress'
        """, (project_id,))
        conn.commit()
        success = True
        message = "Project submitted for client approval! 🏁"
    except mysql.connector.Error as err:
        success = False
        message = f"Error: {err}"
    cursor.close()
    conn.close()
    return success, message

def approve_project_completion(project_id):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Projects SET status = 'completed' 
            WHERE project_id = %s AND status = 'pending_approval'
        """, (project_id,))
        conn.commit()
        success = True
        message = "Project approved and marked as complete! ✅"
    except mysql.connector.Error as err:
        success = False
        message = f"Error: {err}"
    cursor.close()
    conn.close()
    return success, message

def get_hired_projects(client_id):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            p.project_id, p.title, p.status, 
            a.freelancer_id as freelancer_id, 
            f.name as freelancer_name
        FROM Projects p
        JOIN Applications a ON p.project_id = a.project_id
        JOIN Freelancers f ON a.freelancer_id = f.freelancer_id
        WHERE 
            p.client_id = %s 
            AND a.status = 'accepted'
            AND (p.status = 'in_progress' OR p.status = 'completed' or p.status = 'pending_approval')
    """, (client_id,))
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return projects

def make_payment(project_id, freelancer_id, amount):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Payments (project_id, freelancer_id, amount, payment_date, status)
            VALUES (%s, %s, %s, %s, 'paid')
        """, (project_id, freelancer_id, amount, datetime.now()))
        
        conn.commit()
        success = True
        message = "Payment submitted successfully! 💸"
    except mysql.connector.Error as err:
        success = False
        message = f"Payment failed: {err}"
    
    cursor.close()
    conn.close()
    return success, message

def submit_review(project_id, client_id, freelancer_id, rating, comments):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Reviews (project_id, client_id, freelancer_id, rating, comments, review_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (project_id, client_id, freelancer_id, rating, comments, datetime.now()))
        
        conn.commit()
        success = True
        message = "Review submitted successfully! ⭐"
    except mysql.connector.Error as err:
        success = False
        message = f"Failed to submit review: {err}"
        if "UNIQUE constraint" in str(err) or "Duplicate entry" in str(err):
             message = "You have already submitted a review for this project."

    cursor.close()
    conn.close()
    return success, message

def get_reviews_for_project(project_id):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT 1 FROM Reviews WHERE project_id = %s", (project_id,))
    review = cursor.fetchone()
    cursor.close()
    conn.close()
    return review is not None

def run_complex_query_1():
    conn = get_database_connection()
    query = """
    SELECT 
        f.name AS freelancer_name, 
        SUM(p.amount) AS total_earned,
        ROW_NUMBER() OVER (ORDER BY SUM(p.amount) DESC) AS earning_rank
    FROM Freelancers f
    LEFT JOIN Payments p ON f.freelancer_id = p.freelancer_id AND p.status = 'paid'
    GROUP BY f.freelancer_id, f.name
    ORDER BY total_earned DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def run_complex_query_2():
    conn = get_database_connection()
    query = """
    SELECT
        p.title,
        p.budget,
        AVG(a.bid_amount) AS average_bid
    FROM Projects p
    JOIN Applications a ON p.project_id = a.project_id
    GROUP BY p.project_id, p.title, p.budget
    HAVING AVG(a.bid_amount) < p.budget;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def run_complex_query_3():
    conn = get_database_connection()
    query = """
    WITH ClientAvgBudget AS (
        SELECT
            client_id,
            AVG(budget) AS avg_client_budget
        FROM Projects
        GROUP BY client_id
    )
    SELECT
        p.title,
        c.name AS client_name,
        p.budget,
        cab.avg_client_budget,
        (p.budget - cab.avg_client_budget) AS budget_difference
    FROM Projects p
    JOIN Clients c ON p.client_id = c.client_id
    JOIN ClientAvgBudget cab ON p.client_id = cab.client_id
    ORDER BY client_name, budget_difference DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def run_complex_query_4(skill_name="Python"):
    conn = get_database_connection()
    query = f"""
    SELECT
        f.name,
        f.email
    FROM Freelancers f
    WHERE
        NOT EXISTS (
            SELECT 1
            FROM Freelancer_Skills fs
            JOIN Skills s ON fs.skill_id = s.skill_id
            WHERE fs.freelancer_id = f.freelancer_id
              AND s.skill_name = '{skill_name}'
        );
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def run_complex_query_5():
    conn = get_database_connection()
    query = """
    SELECT 
        s.skill_name, 
        f.name AS top_freelancer, 
        fs.experience_years
    FROM Skills s
    JOIN Freelancer_Skills fs ON s.skill_id = fs.skill_id
    JOIN Freelancers f ON fs.freelancer_id = f.freelancer_id
    WHERE fs.experience_years = (
        SELECT MAX(fs_inner.experience_years) 
        FROM Freelancer_Skills fs_inner 
        WHERE fs_inner.skill_id = s.skill_id
    );
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- Streamlit Pages (Updated UI) ---

def show_login_page():
    st.markdown('<h1 style="text-align: center; color: #2d2d2d; margin-top: 3rem;">Welcome to the Platform</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Login</h2>", unsafe_allow_html=True)
        
        user_type = st.selectbox("Login as:", ["client", "freelancer", "admin"])
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("Login 🔐"):
            if email and password:
                user = login(email, password, user_type)
                if user:
                    st.session_state.user_id = user['user_id']
                    st.session_state.user_type = user['user_type']
                    st.session_state.username = user['username']
                    st.success("Welcome back! ")
                    st.rerun()
                else:
                    st.error(f"Invalid email or password ❌")
            else:
                st.warning("Please enter your email and password ⚠️")
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_client_dashboard():
    st.markdown(f'<h1 class="page-header">Client Dashboard</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Create Project", 
        "My Projects & Apps",
        "Payments & Reviews",
        "Find Freelancers"
    ])
    
    with tab1:
        # This tab remains the same (Create Project)
        st.subheader("Post a New Project")
        st.markdown("Fill out the details below to find the perfect freelancer.")
        
        with st.form("create_project_form"):
            title = st.text_input("Project Title", placeholder="E.g., 'Build a React E-commerce Website'")
            description = st.text_area("Project Description", placeholder="Describe your project requirements, scope, and deliverables in detail.")
            col1, col2 = st.columns(2)
            with col1:
                budget = st.number_input("Budget ($)", min_value=0.0, step=100.0, format="%.2f")
            with col2:
                deadline = st.date_input("Deadline", min_value=datetime.now().date(), value=datetime.now().date() + timedelta(days=30))
            
            submitted = st.form_submit_button("Create Project ")
            
            if submitted:
                if title and description and budget and deadline:
                    success, message = create_project(
                        st.session_state.user_id,
                        title,
                        description,
                        budget,
                        deadline.strftime('%Y-%m-%d 23:59:59')
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill in all fields ⚠️")
    
    with tab2:
        # [MODIFIED] This tab now calls your stored procedures
        st.subheader("My Projects Management")
        st.markdown("Track the status of your projects and manage applications.")
            
        # Call the stored procedure
        client_projects = call_sp_get_client_projects(st.session_state.user_id)
        
        if not client_projects:
            st.info("You haven't created any projects yet. Go to the 'Create Project' tab to get started! 🎯")
        else:
            for project in client_projects:
                st.markdown(f"""
                    <div class='project-card'>
                        <h3>{project['title']}</h3>
                        <p><strong>Status:</strong> {project['status'].replace('_', ' ').title()}</p>
                        <p><strong>Budget:</strong> ${project['budget']}</p>
                        <p><small>Deadline: {project['formatted_deadline']}</small></p>
                        <p style='margin-top: 1rem;'>{project['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Call the SQL function for the count
                app_count = call_fn_get_project_app_count(project['project_id'])
                st.write(f"**Applications Received:** {app_count}")
                
                if app_count > 0:
                    applications = get_applications_for_project(project['project_id'])
                    with st.expander("View Applications"):
                        for app in applications:
                            st.markdown(f"**From:** {app['freelancer_name']} ({app['freelancer_email']})")
                            st.markdown(f"**Bid:** ${app['bid_amount']}")
                            st.markdown(f"**Status:** {app['status'].title()}")
                            st.info(f"**Proposal:** {app['proposal_text']}")
                            
                            if project['status'] == 'open' and app['status'] == 'pending':
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("Accept ✅", key=f"accept_{app['application_id']}"):
                                        if update_application_status(app['application_id'], 'accepted'):
                                            update_project_on_hire(project['project_id'], app['freelancer_id'])
                                            st.success(f"Accepted {app['freelancer_name']}!")
                                            st.rerun()
                                with col2:
                                    if st.button("Reject ❌", key=f"reject_{app['application_id']}"):
                                        if update_application_status(app['application_id'], 'rejected'):
                                            st.warning(f"Rejected {app['freelancer_name']}.")
                                            st.rerun()
                            st.markdown("---")
                st.markdown("<br>", unsafe_allow_html=True)
        
    with tab3:
        # This tab remains the same (Payments & Reviews)
        st.subheader("Payments & Reviews")
        st.markdown("Approve completed work, make payments, and leave feedback.")

        hired_projects = get_hired_projects(st.session_state.user_id)
        
        if not hired_projects:
            st.info("You have no 'In Progress' or 'Completed' projects to pay or review.")
            return

        # --- Approve Completion Section ---
        st.markdown("#### Approve Completed Work")
        approval_projects = [p for p in hired_projects if p['status'] == 'pending_approval']
        
        if not approval_projects:
            st.info("You have no projects awaiting your approval. ⌛")
        else:
            for project in approval_projects:
                st.markdown(f"""
                    <div class='project-card' style='border: 2px solid var(--primary-color);'>
                        <h4>{project['title']}</h4>
                        <p><strong>Freelancer:</strong> {project['freelancer_name']}</p>
                        <p>This project is finished and awaits your approval.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.button("Approve & Mark as Complete ✅", key=f"approve_{project['project_id']}"):
                    success, message = approve_project_completion(project['project_id'])
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)

        # --- Make Payment Form ---
        st.markdown("#### Make a Payment")
        payable_projects = [p for p in hired_projects if p['status'] != 'pending_approval']
        
        if not payable_projects:
            st.info("No projects are currently available for payment.")
        else:
            project_options = {p['project_id']: f"{p['title']} (Freelancer: {p['freelancer_name']})" for p in payable_projects}
            
            selected_project_id = st.selectbox(
                "Select a project to pay:", 
                options=project_options.keys(),
                format_func=lambda x: project_options[x]
            )
            
            if selected_project_id:
                selected_project = next(p for p in payable_projects if p['project_id'] == selected_project_id)
                
                with st.form(f"payment_form_{selected_project_id}"):
                    st.write(f"You are paying **{selected_project['freelancer_name']}** for the project **'{selected_project['title']}'**.")
                    amount = st.number_input("Payment Amount ($)", min_value=0.01, step=10.0, format="%.2f")
                    
                    submitted_payment = st.form_submit_button("Submit Payment ")
                    
                    if submitted_payment:
                        success, message = make_payment(
                            selected_project_id,
                            selected_project['freelancer_id'],
                            amount
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
        st.markdown("---")

        # --- Leave Review Form ---
        st.markdown("#### Leave a Review")
        completed_projects = [p for p in hired_projects if p['status'] == 'completed']
        
        if not completed_projects:
            st.info("You have no 'Completed' projects to review yet.")
        else:
            review_project_options = {p['project_id']: f"{p['title']} (Freelancer: {p['freelancer_name']})" for p in completed_projects}
            
            selected_review_project_id = st.selectbox(
                "Select a completed project to review:",
                options=review_project_options.keys(),
                format_func=lambda x: review_project_options[x],
                key="review_project_select"
            )
            
            if selected_review_project_id:
                if get_reviews_for_project(selected_review_project_id):
                    st.warning("You have already submitted a review for this project. ")
                else:
                    review_project = next(p for p in completed_projects if p['project_id'] == selected_review_project_id)
                    
                    with st.form(f"review_form_{selected_review_project_id}"):
                        st.write(f"You are reviewing **{review_project['freelancer_name']}** for **'{review_project['title']}'**.")
                        
                        rating = st.slider("Rating (1-5 Stars)", min_value=1, max_value=5, value=5)
                        comments = st.text_area("Comments", placeholder="Share your experience working with this freelancer...")
                        
                        submitted_review = st.form_submit_button("Submit Review ")
                        
                        if submitted_review:
                            if not comments:
                                st.warning("Please leave a comment.")
                            else:
                                success, message = submit_review(
                                    review_project['project_id'],
                                    st.session_state.user_id,
                                    review_project['freelancer_id'],
                                    rating,
                                    comments
                                )
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)

    with tab4:
        # [MODIFIED] This tab now has TWO features
        st.subheader("Find Freelancers by Skill")
        st.markdown("Use the dropdown to find freelancers with a specific skill, ranked by experience and rating.")
        
        all_skills = get_all_skills()
        
        if not all_skills:
            st.error("No skills found in the database. Please add skills.")
            # We don't return, so the next feature can still load
        else:
            selected_skill = st.selectbox("Select a skill to search for:", all_skills, key="skill_search_box")
            
            if st.button("Search Freelancers "):
                if selected_skill:
                    with st.spinner(f"Searching for '{selected_skill}' experts..."):
                        # Call the stored procedure
                        freelancers = call_sp_get_freelancers_by_skill(selected_skill)
                        
                        if not freelancers:
                            st.warning(f"No freelancers found with the skill '{selected_skill}'.")
                        else:
                            st.markdown(f"### Results for '{selected_skill}'")
                            
                            for f in freelancers:
                                st.markdown(f"""
                                <div class='project-card'>
                                    <h4>{f['name']}</h4>
                                    <p><strong>Email:</strong> {f['email']}</p>
                                    <p><strong>Experience:</strong> {f['experience_years']} years</p>
                                    <p><strong>Rating:</strong> {f['average_rating']} / 5.00 </p>
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    st.warning("Please select a skill.")

        st.markdown("---")
        
        # --- [NEW] Section using fn_HasSkill ---
        st.subheader("Check a Freelancer's Skill")
        st.markdown("Verify if a specific freelancer has a particular skill.")
        
        all_freelancers = get_all_freelancers()
        
        if not all_freelancers or not all_skills:
            st.info("Missing data to perform check (requires at least one freelancer and one skill).")
        else:
            # Create a dictionary for the freelancer selectbox
            freelancer_options = {f['freelancer_id']: f['name'] for f in all_freelancers}
            
            col1, col2 = st.columns(2)
            with col1:
                selected_freelancer_id = st.selectbox(
                    "Select a freelancer:",
                    options=freelancer_options.keys(),
                    format_func=lambda x: freelancer_options[x]
                )
            with col2:
                selected_skill_to_check = st.selectbox(
                    "Select a skill to check:",
                    options=all_skills,
                    key="skill_check_box"
                )
            
            if st.button("Check Skill "):
                freelancer_name = freelancer_options[selected_freelancer_id]
                
                with st.spinner(f"Checking if {freelancer_name} knows {selected_skill_to_check}..."):
                    # Call the SQL function
                    has_the_skill = call_fn_has_skill(selected_freelancer_id, selected_skill_to_check)
                
                if has_the_skill:
                    st.success(f"**Yes**, {freelancer_name} has the skill: **{selected_skill_to_check}**.")
                else:
                    st.error(f"**No**, {freelancer_name} does not have the skill: **{selected_skill_to_check}**.")


def show_freelancer_dashboard():
    st.markdown(f'''
        <div class="welcome-header">
            <h1>Welcome, {st.session_state.username}! </h1>
            <p>Manage your projects and track progress all in one place</p>
        </div>
    ''', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Browse Projects ", 
        "My Active Projects ",
        "My Applications ", 
        "Manage Profile "
    ])
    
    with tab1:
        projects = get_projects() 
        if projects:
            for project in projects:
                # Add a colored border based on status
                border_color = "#e1d6f5" # Default (open)
                if project['status'] == 'in_progress':
                    border_color = "#f3bf9c" # Orange
                elif project['status'] in ['completed', 'cancelled']:
                    border_color = "#d1d1d1" # Grey
                
                expander_title = f" {project['title']} by {project['client_name']} (Status: {project['status'].title()})"
                
                with st.expander(expander_title):
                    st.markdown(f"""
                        <div style='background-color: #f8f7fb; padding: 1rem; border-radius: 8px; border: 2px solid {border_color};'>
                            <p><strong>Description:</strong> {project['description']}</p>
                            <p><strong>Budget:</strong> ${project['budget']}</p>
                            <p><small>Deadline: {project['formatted_deadline']}</small></p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    
                    if project['status'] == 'open':
                        # This is an open project, show the normal form
                        st.markdown("### Submit Your Proposal")
                        with st.form(f"form_prop_{project['project_id']}"):
                            proposal_text = st.text_area("Proposal Details", 
                                                      placeholder="Describe why you're the best fit for this project",
                                                      key=f"proposal_{project['project_id']}")
                            bid_amount = st.number_input("Your Bid ($)", 
                                                      min_value=0.0, 
                                                      max_value=float(project['budget']),
                                                      step=10.0,
                                                      key=f"bid_{project['project_id']}")
                            
                            if st.form_submit_button("Submit Proposal "):
                                if proposal_text and bid_amount:
                                    success, message = submit_proposal(
                                        project['project_id'],
                                        st.session_state.user_id,
                                        proposal_text,
                                        bid_amount
                                    )
                                    if success:
                                        st.success(message)
                                    else:
                                        st.error(message) # This will show a normal error
                                else:
                                    st.warning("Please fill in all fields ")

                    elif project['status'] == 'in_progress':
                        # This project is in progress, block it with Python
                        st.info("This project is already in progress and not accepting applications.")
                    
                    else:
                        # This is 'completed' or 'cancelled'.
                        # We SHOW the form to let the user test the trigger.
                        #st.warning(f"This project is **{project['status']}**. Applications are closed.")
                        st.markdown(f"### Apply")
                        
                        with st.form(f"form_prop_{project['project_id']}"):
                            proposal_text = st.text_area("Proposal Details", 
                                                      placeholder="Test proposal",
                                                      key=f"proposal_{project['project_id']}")
                            bid_amount = st.number_input("Your Bid ($)", 
                                                      min_value=0.0, 
                                                      step=10.0,
                                                      key=f"bid_{project['project_id']}")

                            if st.form_submit_button("Apply "):
                                if proposal_text and bid_amount:
                                    success, message = submit_proposal(
                                        project['project_id'],
                                        st.session_state.user_id,
                                        proposal_text,
                                        bid_amount
                                    )
                                    if success:
                                        st.success(message) # This should never happen
                                    else:
                                        # This will display the error from your trigger
                                        st.error(message) 
                                else:
                                    st.warning("Please fill in all fields ")
        else:
            st.info("No projects found on the platform.")

    with tab2:
        # This tab (My Active Projects) remains unchanged
        active_projects = get_my_active_projects(st.session_state.user_id)
        
        if not active_projects:
            st.info("You have no 'In Progress' projects. Once a client accepts your application, it will appear here. ")
        else:
            for project in active_projects:
                st.markdown(f"""
                    <div class='project-card'>
                        <h4 style='color: #667eea;'>{project['title']}</h4>
                        <p><strong>Client:</strong> {project['client_name']}</p>
                        <p><strong>Status:</strong> {project['status'].replace('_', ' ').title()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if project['status'] == 'in_progress':
                    if st.button("Mark as Complete & Submit for Approval ", key=f"complete_{project['project_id']}"):
                        success, message = mark_project_for_approval(project['project_id'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                elif project['status'] == 'pending_approval':
                    st.info("This project is pending client approval. ")
                
                st.markdown("---")

    with tab3:
        # This tab (My Applications) remains unchanged
        applications = get_my_applications(st.session_state.user_id)
        
        if applications:
            for app in applications:
                st.markdown(f"""
                    <div class='project-card'>
                        <h4 style='color: #667eea;'>{app['project_title']}</h4>
                        <p><strong>Status:</strong> {app['status'].title()}</p>
                        <p><strong>My Bid:</strong> ${app['bid_amount']}</p>
                        <p><strong>My Proposal:</strong> {app['proposal_text']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("You haven't applied to any projects yet. ")
            
    with tab4:
        # This tab (Manage Profile) remains unchanged
        st.markdown('''
            <div class="content-card">
                <h2>Manage My Skills</h2>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.form("add_skill_form"):
            st.subheader("Add or Update Skill")
            skill_name = st.text_input("Skill Name (e.g., 'Python', 'Streamlit')")
            experience_years = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
            submitted_add = st.form_submit_button("Add/Update Skill")
            
            if submitted_add and skill_name:
                success, message = add_freelancer_skill(st.session_state.user_id, skill_name, experience_years)
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        st.markdown("---")
        
        st.subheader("My Current Skills")
        current_skills = get_freelancer_skills(st.session_state.user_id)
        
        if current_skills:
            for skill in current_skills:
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"**Skill:** {skill['skill_name']}")
                with col2:
                    st.write(f"**Experience:** {skill['experience_years']} years")
                with col3:
                    if st.button("Remove ", key=f"remove_{skill['skill_name']}"):
                        success, message = remove_freelancer_skill(st.session_state.user_id, skill['skill_name'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("You haven't added any skills to your profile yet.")

# def show_admin_dashboard():
#     st.markdown(f'<h1 class="page-header">Admin Dashboard</h1>', unsafe_allow_html=True)

#     st.subheader("Platform Analytics")
#         #st.markdown("High-level insights into platform activity based on your complex queries.")

#     query_options = {
#             "Freelancer Earning Ranks": {
#                 "function": run_complex_query_1,
#                 "description": "Shows all freelancers ranked by their total 'paid' earnings."
#             },
#             "Top Experienced Freelancer per Skill": {
#                 "function": run_complex_query_5,
#                 "description": "Shows the freelancer with the most experience for each skill."
#             },
#             "Projects Where Avg. Bid is Below Budget": {
#                 "function": run_complex_query_2,
#                 "description": "Shows projects where the average bid is lower than the client's budget."
#             },
#             "Client's Project Budget vs. Their Average": {
#                 "function": run_complex_query_3,
#                 "description": "Analyzes each client's project budgets compared to their personal average."
#             }
#         }

#     selected_query_name = st.selectbox(
#             "Select an analytics query to run:",
#             options=query_options.keys()
#         )

#     if selected_query_name:
#             selected_query = query_options[selected_query_name]
            
#             st.markdown(f"#### {selected_query_name}")
#             st.markdown(selected_query["description"])
            
#             with st.spinner("Running query..."):
#                 df = selected_query["function"]()
#                 st.dataframe(df, use_container_width=True)

#     st.markdown("---")
#     st.markdown("#### Advanced User Search")
#     st.markdown("Finds all freelancers who do NOT have a specific skill.")
#     skill_to_check = st.text_input("Find freelancers without skill:", "Python")
        
#     if st.button("Run Search", key="search_skill"):
#         if skill_to_check:
#             with st.spinner("Running search..."):
#                 st.dataframe(run_complex_query_4(skill_to_check), use_container_width=True)
#         else:
#             st.warning("Please enter a skill name.")

def show_admin_dashboard():
    st.markdown(f'<h1 class="page-header">Admin Dashboard</h1>', unsafe_allow_html=True)

    st.subheader("Platform Analytics (Complex Queries)")
    
    query_options = {
            "Query 1: Freelancer Earning Ranks": {
                "function": run_complex_query_1,
                "description": "Shows all freelancers ranked by their total 'paid' earnings."
            },
            "Query 5: Top Experienced Freelancer per Skill": {
                "function": run_complex_query_5,
                "description": "Shows the freelancer with the most experience for each skill."
            },
            "Query 2: Projects Where Avg. Bid is Below Budget": {
                "function": run_complex_query_2,
                "description": "Shows projects where the average bid is lower than the client's budget."
            },
            "Query 3: Client's Project Budget vs. Their Average": {
                "function": run_complex_query_3,
                "description": "Analyzes each client's project budgets compared to their personal average."
            }
        }

    selected_query_name = st.selectbox(
            "Select an analytics query to run:",
            options=query_options.keys()
        )

    if selected_query_name:
            selected_query = query_options[selected_query_name]
            
            st.markdown(f"#### {selected_query_name}")
            st.markdown(selected_query["description"])
            
            with st.spinner("Running query..."):
                df = selected_query["function"]()
                st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Advanced User Search")
    st.markdown("Finds all freelancers who do NOT have a specific skill.")
    skill_to_check = st.text_input("Find freelancers without skill:", "Python")
        
    if st.button("Run Search", key="search_skill"):
        if skill_to_check:
            with st.spinner("Running search..."):
                st.dataframe(run_complex_query_4(skill_to_check), use_container_width=True)
        else:
            st.warning("Please enter a skill name.")

     # --- [NEW] Section to Demonstrate Trigger ---
    st.subheader("Freelancer Rating Check")
    #st.markdown("Select a freelancer to view their *current* average rating. This value is ")
    
    all_freelancers = get_all_freelancers_with_ratings()
    
    if not all_freelancers:
        st.error("No freelancers found in the database.")
    else:
        # Create a dictionary for the selectbox
        freelancer_options = {f['freelancer_id']: f['name'] for f in all_freelancers}
        
        selected_freelancer_id = st.selectbox(
            "Select a freelancer to check their rating:",
            options=freelancer_options.keys(),
            format_func=lambda x: freelancer_options[x],
            key="admin_rating_check"
        )
        
        if selected_freelancer_id:
            # Find the full freelancer object
            freelancer = next(f for f in all_freelancers if f['freelancer_id'] == selected_freelancer_id)
            # Display their rating as a large metric
            st.metric(
                label=f"Current Rating for {freelancer['name']}", 
                value=f"{freelancer['average_rating']:.2f} / 5.00 "
            )
            
    st.markdown("---")
    # --- End of New Section --


def main():
    with st.sidebar:
        st.markdown('<p class="sidebar-title">Navigation</p>', unsafe_allow_html=True)
        
        if st.session_state.user_id is None:
            page = st.radio("", ["Login", "Register"], label_visibility="collapsed")
        else:
            # User avatar and info
            first_letter = st.session_state.username[0].upper() if st.session_state.username else "U"
            st.markdown(f'''
                <div class="user-avatar">{first_letter}</div>
                <div class="user-name">{st.session_state.username}</div>
                <div class="user-role">Role: {st.session_state.user_type.title()}</div>
            ''', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Logout "):
                st.session_state.user_id = None
                st.session_state.user_type = None
                st.session_state.username = None
                st.rerun()
    
    if st.session_state.user_id is None:
        if page == "Login":
            show_login_page()
        else:
            show_registration_page()
    else:
        if st.session_state.user_type == "client":
            show_client_dashboard()
        elif st.session_state.user_type == "freelancer":
            show_freelancer_dashboard()
        elif st.session_state.user_type == "admin":
            show_admin_dashboard()

if __name__ == "__main__":
    main()
