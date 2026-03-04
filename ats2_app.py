import streamlit as st # type: ignore
import sqlite3
import pandas as pd # type: ignore
import os
from datetime import datetime, date

st.set_page_config(page_title="Jailaxmi Group ATS System", layout="wide")

# ================= PROFESSIONAL UI CSS =================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    color: white;
}

.login-card {
    background: white;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.3);
    color: black;
}

.metric-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    text-align: center;
    color: black;
}
    .metric-card h4 {
    font-size: 16px;
    margin-bottom: 10px;
    font-weight: 600;
}
.metric-card h2 {
    font-size: 34px;
    margin: 0;
    font-weight: bold;
}

.stButton>button {
    background: linear-gradient(90deg, #1d976c, #93f9b9);
    border: none;
    color: black;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("ats.db", check_same_thread=False)
c = conn.cursor()

# ---------------- CREATE TABLES ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    marital_status TEXT,
    father_name TEXT,
    father_employment_status TEXT,
    father_salary TEXT,
    mother_name TEXT,
    mother_employment_status TEXT,
    mother_salary TEXT,
    brother_name TEXT,
    brother_employment_status TEXT,
    brother_salary TEXT,
    sister_name TEXT,
    sister_employment_status TEXT,
    sister_salary TEXT,
    gender TEXT,
    dob TEXT,
    mobile TEXT,
    email TEXT,
    permanent_address TEXT,
    city TEXT,
    pincode TEXT,
    aadhaar TEXT,
    pan TEXT,
    blood_group TEXT,
    emergency_name TEXT,
    emergency_number TEXT,
    experience_type TEXT,
    years_experience TEXT,
    previous_company TEXT,
    previous_designation TEXT,
    employment_from TEXT,
    employment_to TEXT,
    current_salary TEXT,
    expected_salary TEXT,
    source TEXT,
    referer_name TEXT,
    referer_branch TEXT,
    referer_designation TEXT,
    status TEXT,
    added_by TEXT,
    date_added TEXT,
    resume TEXT
)
""")

conn.commit()

# ---------------- DEFAULT USERS ----------------
users = [
    ("admin", "admin123", "Admin"),
    ("HR1", "Hr123", "User"),
    ("HR2", "Hr123", "User"),
    ("HR3", "Hr123", "User"),
    ("HR4", "Hr123", "User"),
]

for user in users:
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", user)
    except:
        pass

conn.commit()

# ---------------- RESUME FOLDER ----------------
if not os.path.exists("resumes"):
    os.makedirs("resumes")

st.title("Jailaxmi Group Applicant Tracking System (ATS)")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]
            st.rerun()
        else:
            st.error("Invalid Credentials")

# ---------------- MAIN SYSTEM ----------------
else:

    # Show logged in user
    st.sidebar.write(f"👤 {st.session_state.username} ({st.session_state.role})")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Main Menu")

    # MAIN MENU SESSION
    if "menu" not in st.session_state:
        st.session_state.menu = "Dashboard"

    # SIDEBAR MENU BUTTONS
    if st.sidebar.button("🏠 Dashboard"):
        st.session_state.menu = "Dashboard"

    if st.sidebar.button("➕ Add Candidate"):
        st.session_state.menu = "Add Candidate"

    if st.sidebar.button("📋 View Candidates"):
        st.session_state.menu = "View Candidates"

    if st.sidebar.button("🚪 Logout"):
        st.session_state.menu = "Logout"

    menu = st.session_state.menu  
     
# ================= DASHBOARD =================
    if menu == "Dashboard":

        if st.session_state.role == "Admin":
            total = c.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
            interviewed = c.execute("SELECT COUNT(*) FROM candidates WHERE status='Interviewed'").fetchone()[0]
            shortlisted = c.execute("SELECT COUNT(*) FROM candidates WHERE status='Shortlisted'").fetchone()[0]
            selected = c.execute("SELECT COUNT(*) FROM candidates WHERE status='Selected'").fetchone()[0]
            rejected = c.execute("SELECT COUNT(*) FROM candidates WHERE status='Rejected'").fetchone()[0]
        else:
            total = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by=?", 
                              (st.session_state.username,)).fetchone()[0]
            interviewed = c.execute("SELECT COUNT(*) FROM candidates WHERE status='Interviewed' AND added_by=?", 
                                    (st.session_state.username,)).fetchone()[0] 
            shortlisted = c.execute("SELECT COUNT(*) FROM candidates WHERE status='Shortlisted' AND added_by=?", 
                                    (st.session_state.username,)).fetchone()[0]
            selected = c.execute("SELECT COUNT(*) FROM candidates WHERE status='Selected' AND added_by=?", 
                                 (st.session_state.username,)).fetchone()[0]
            rejected = c.execute("SELECT COUNT(*) FROM candidates WHERE status='Rejected' AND added_by=?", 
                                 (st.session_state.username,)).fetchone()[0]

        st.markdown("## 📊 STATUS Dashboard Overview")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f"<div class='metric-card'><h4>TOTAL</h4><h2>{total}</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><h4>INTERVIEWED</h4><h2>{interviewed}</h2></div>", unsafe_allow_html=True)       
        with col3:
            st.markdown(f"<div class='metric-card'><h4>SHORTLISTED</h4><h2>{shortlisted}</h2></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-card'><h4>SELECTED</h4><h2>{selected}</h2></div>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"<div class='metric-card'><h4>REJECTED</h4><h2>{rejected}</h2></div>", unsafe_allow_html=True)
    if menu == "Dashboard":

        if st.session_state.role == "Admin":
            Walkin = c.execute("SELECT COUNT(*) FROM candidates WHERE source='Walk-in'").fetchone()[0]
            Consultancy = c.execute("SELECT COUNT(*) FROM candidates WHERE source='Consultancy'").fetchone()[0]
            Employee_Reference = c.execute("SELECT COUNT(*) FROM candidates WHERE source='Employee Reference'").fetchone()[0]
            Website = c.execute("SELECT COUNT(*) FROM candidates WHERE source='Website'").fetchone()[0]
            Job_Portal = c.execute("SELECT COUNT(*) FROM candidates WHERE source='Job Portal'").fetchone()[0]
        else:
            Walkin = c.execute("SELECT COUNT(*) FROM candidates WHERE source='Walk-in' AND added_by=?", 
                                (st.session_state.username,)).fetchone()[0]
            Consultancy = c.execute("SELECT COUNT(*) FROM candidates WHERE source='Consultancy' AND added_by=?", 
                                    (st.session_state.username,)).fetchone()[0]
            Employee_Reference = c.execute("SELECT COUNT(*) FROM candidates WHERE source='Employee Reference' AND added_by=?", 
                                            (st.session_state.username,)).fetchone()[0]
            Website = c.execute("SELECT COUNT(*) FROM candidates WHERE source='Website' AND added_by=?", 
                                (st.session_state.username,)).fetchone()[0]
            Job_Portal = c.execute("SELECT COUNT(*) FROM candidates WHERE source='Job Portal' AND added_by=?", 
                                    (st.session_state.username,)).fetchone()[0]
        st.markdown("## 📊 Candidate Source Distribution")

        col1, col2, col3, col4, col5 = st.columns(5)     

        with col1:
            st.markdown(f"<div class='metric-card'><h4>WALK-IN</h4><h2>{Walkin}</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><h4>CONSULTANCY</h4><h2>{Consultancy}</h2></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><h4>REFERENCE</h4><h2>{Employee_Reference}</h2></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-card'><h4>WEBSITE</h4><h2>{Website}</h2></div>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"<div class='metric-card'><h4>JOB PORTAL</h4><h2>{Job_Portal}</h2></div>", unsafe_allow_html=True)
    if menu == "Dashboard":

        if st.session_state.role == "Admin":
            admin = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by='admin'").fetchone()[0]
            HR1 = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by='HR1'").fetchone()[0]
            HR2 = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by='HR2'").fetchone()[0]
            HR3 = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by='HR3'").fetchone()[0]
            HR4 = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by='HR4'").fetchone()[0]
        else:
            admin = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by='admin' AND added_by=?",
                              (st.session_state.username,)).fetchone()[0]
            HR1 = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by='HR1' AND added_by=?", 
                            (st.session_state.username,)).fetchone()[0]
            HR2 = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by='HR2' AND added_by=?", 
                            (st.session_state.username,)).fetchone()[0]
            HR3 = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by='HR3' AND added_by=?", 
                            (st.session_state.username,)).fetchone()[0]
            HR4 = c.execute("SELECT COUNT(*) FROM candidates WHERE added_by='HR4' AND added_by=?", 
                            (st.session_state.username,)).fetchone()[0]
        st.markdown("## 📊 HR Performance Overview")

        col1, col2, col3, col4, col5 = st.columns(5)      

        with col1:
            st.markdown(f"<div class='metric-card'><h4>ADMIN</h4><h2>{admin}</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><h4>HR1</h4><h2>{HR1}</h2></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><h4>HR2</h4><h2>{HR2}</h2></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-card'><h4>HR3</h4><h2>{HR3}</h2></div>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"<div class='metric-card'><h4>HR4</h4><h2>{HR4}</h2></div>", unsafe_allow_html=True)

    # ---------------- ADD CANDIDATE ----------------
    elif menu == "Add Candidate":

        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input("Full Name")
            marital_status = st.selectbox("Marital Status", ["Single", "Married"])

            spouse_name = ""
            spouse_employment_status = ""
            spouse_salary = ""

            if marital_status == "Married":
                spouse_name = st.text_input("Spouse Name")
                spouse_employment_status = st.selectbox("Spouse Employment", ["Employed", "Unemployed"])
                spouse_salary = st.text_input("Spouse Salary")

            father_name = st.text_input("Father Name")
            father_employment_status = st.selectbox("Father Employment", ["Employed", "Unemployed"])
            father_salary = st.text_input("Father Salary")
            mother_name = st.text_input("Mother Name")
            mother_employment_status = st.selectbox("Mother Employment", ["Employed", "Unemployed"])
            mother_salary = st.text_input("Mother Salary")
            brother_name = st.text_input("Brother Name")
            brother_employment_status = st.selectbox("Brother Employment", ["Employed", "Unemployed"])
            brother_salary = st.text_input("Brother Salary")
            sister_name = st.text_input("Sister Name")
            sister_employment_status = st.selectbox("Sister Employment", ["Employed", "Unemployed"])
            sister_salary = st.text_input("Sister Salary")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            dob = st.date_input("Date of Birth", value=date(1995, 1, 1))
            mobile = st.text_input("Mobile")
            email = st.text_input("Email")

        with col2:
            permanent_address = st.text_area("Permanent Address")
            city = st.text_input("City")
            pincode = st.text_input("Pincode")
            aadhaar = st.text_input("Aadhaar")
            pan = st.text_input("PAN")
            blood_group = st.selectbox("Blood Group",
                                       ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            emergency_name = st.text_input("Emergency Contact Name")
            emergency_number = st.text_input("Emergency Contact Number")
            experience_type = st.selectbox("Experience", ["Fresher", "Experienced"])

            years_experience = previous_company = previous_designation = ""
            employment_from = employment_to = ""
            current_salary = ""

            if experience_type == "Experienced":
                years_experience = st.text_input("Years of Experience")
                previous_company = st.text_input("Previous Company")
                previous_designation = st.text_input("Previous Designation")
                employment_from = st.text_input("Employment From")
                employment_to = st.text_input("Employment To")
                current_salary = st.text_input("Current Salary")

            expected_salary = st.text_input("Expected Salary")
            source = st.selectbox("Source",
                                  ["Walk-in", "Consultancy", "Employee Reference",
                                   "Website", "Job Portal"])
            referer_name = st.text_input("Referer Name")
            referer_branch = st.text_input("Referer Branch")
            referer_designation = st.text_input("Referer Designation")
            status = st.selectbox("Status",
                                  ["Applied", "Shortlisted", "Interviewed",
                                   "Selected", "Rejected"])

        resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

        if st.button("Save Candidate"):

            # Duplicate Check
            duplicate = c.execute(
                "SELECT id FROM candidates WHERE mobile=? OR aadhaar=?",
                (mobile, aadhaar)
            ).fetchone()

            if duplicate:
                st.error("⚠ Candidate already exists with same Mobile or Aadhaar!")
            else:
                resume_path = ""
                if resume:
                    resume_path = os.path.join("resumes", resume.name)
                    with open(resume_path, "wb") as f:
                        f.write(resume.getbuffer())

                c.execute("""
                INSERT INTO candidates (
                    full_name, marital_status, father_name, father_employment_status, father_salary,
                    mother_name, mother_employment_status, mother_salary,
                    brother_name, brother_employment_status, brother_salary,
                    sister_name, sister_employment_status, sister_salary,
                    gender, dob, mobile, email, permanent_address,
                    city, pincode, aadhaar, pan,
                    blood_group,
                    emergency_name, emergency_number,
                    experience_type, years_experience,
                    previous_company, previous_designation,
                    employment_from, employment_to,
                    current_salary, expected_salary,
                    source, referer_name, referer_branch, referer_designation,
                    status, added_by, date_added, resume
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    full_name, marital_status, father_name, father_employment_status, father_salary,
                    mother_name, mother_employment_status, mother_salary,
                    brother_name, brother_employment_status, brother_salary,
                    sister_name, sister_employment_status, sister_salary,
                    gender, str(dob), mobile, email, permanent_address,
                    city, pincode, aadhaar, pan,
                    blood_group,
                    emergency_name, emergency_number,
                    experience_type, years_experience,
                    previous_company, previous_designation,
                    employment_from, employment_to,
                    current_salary, expected_salary,
                    source, referer_name, referer_branch, referer_designation,
                    status, st.session_state.username,
                    datetime.now().strftime("%Y-%m-%d"), resume_path
                ))

                conn.commit()
                st.success("Candidate Added Successfully")
                st.rerun()

            # ---------------- VIEW ----------------
    elif menu == "View Candidates":

        st.subheader("🔍 Search Candidates")

        col1, col2, col3 = st.columns(3)

        with col1:
            search_id = st.text_input("Search by ID")

        with col2:
            search_name = st.text_input("Search by Name")

        with col3:
            search_mobile = st.text_input("Search by Mobile")

        search_status = st.selectbox(
            "Filter by Status",
            ["All", "Applied", "Shortlisted", "Interviewed", "Selected", "Rejected"]
        )

        # -------- BASE QUERY --------
        query = "SELECT * FROM candidates WHERE 1=1"
        params = []

        # Role restriction
        if st.session_state.role != "Admin":
            query += " AND added_by=?"
            params.append(st.session_state.username)

        # Apply filters
        if search_id:
            query += " AND id=?"
            params.append(search_id)

        if search_name:
            query += " AND full_name LIKE ?"
            params.append(f"%{search_name}%")

        if search_mobile:
            query += " AND mobile=?"
            params.append(search_mobile)

        if search_status != "All":
            query += " AND status=?"
            params.append(search_status)

        df = pd.read_sql_query(query, conn, params=params)

        if not df.empty:
            st.dataframe(df, use_container_width=True)

            # ---------------- STATUS UPDATE ----------------
            st.markdown("---")
            st.subheader("🔄 Update Candidate Status")

            candidate_id = st.selectbox(
                "Select Candidate ID",
                df["id"].tolist()
            )

            new_status = st.selectbox(
                "Change Status To",
                ["Applied", "Shortlisted", "Interviewed", "Selected", "Rejected"]
            )

            if st.button("Update Status"):

                if st.session_state.role == "Admin":
                    c.execute(
                        "UPDATE candidates SET status=? WHERE id=?",
                        (new_status, candidate_id)
                    )
                else:
                    c.execute(
                        "UPDATE candidates SET status=? WHERE id=? AND added_by=?",
                        (new_status, candidate_id, st.session_state.username)
                    )

                conn.commit()
                st.success("✅ Status Updated Successfully")
                st.rerun()

        else:
            st.info("No candidates found")

    # ---------------- LOGOUT ----------------
    elif menu == "Logout":
        # Clear session
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()