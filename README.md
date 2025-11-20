# Freelancer Project Matching Platform

This project is a comprehensive, multi-user freelancer platform built with **Streamlit** and **MySQL**. It provides a full-featured web interface for three distinct user roles:
* **Clients:** Can post projects, review applications, and manage payments.
* **Freelancers:** Can browse projects, submit proposals, and manage their skills.
* **Admins:** Can view platform-wide analytics and manage users.

The application is designed to showcase a robust backend, moving significant business logic into the MySQL database using **stored procedures**, **functions**, and **triggers** to ensure data integrity and efficiency.

## ✨ Features

### 🤵 Client Dashboard
* **Create Projects:** Post new projects with a title, description, budget, and deadline.
* **Manage Projects:** View all personal projects and the number of applications received (using a SQL function `fn_get_project_app_count`).
* **Review Applications:** View all proposals for a project, with options to **Accept** or **Reject**.
* **Approve Work:** Mark "pending_approval" projects as "completed."
* **Make Payments:** Submit payments for hired projects.
* **Leave Reviews:** Submit a star rating (1-5) and comments for completed projects.
* **Find Freelancers:**
    * Search for freelancers by a specific skill (using `sp_GetFreelancersBySkill`).
    * Verify if a specific freelancer has a certain skill (using `fn_HasSkill`).

### 🧑‍💻 Freelancer Dashboard
* **Browse Projects:** View all projects on the platform, color-coded by status (Open, In Progress, Completed).
* **Submit Proposals:** Apply to "open" projects with a proposal message and a bid amount.
* **Block Applications:** The backend prevents applications on projects that are not "open" (this is handled by a database trigger).
* **Manage Active Projects:** View all accepted projects and submit them for client approval when finished.
* **Track Applications:** See a list of all submitted applications and their status (Pending, Accepted, Rejected).
* **Manage Profile:** Add, update, or remove skills and list years of experience.

### 🛡️ Admin Dashboard
* **Run Complex Analytics:** Execute and view results from several complex SQL queries with joins, aggregations, and window functions (e.g., "Freelancer Earning Ranks," "Budget vs. Average Bid").
* **Advanced Search:** Find users based on complex criteria (e.g., "Find freelancers *without* a specific skill").
* **Monitor Ratings:** Check any freelancer's current average rating. This rating is updated automatically by the `trg_UpdateFreelancerRating` trigger in the database every time a new review is submitted.

## 🗃️ Advanced Database Features

A key goal of this project is to demonstrate the power of a "smart" database. Business logic is not just in the Python code but is also enforced at the database level.

* **Stored Procedures (SPs)**
    * `sp_GetClientProjects(client_id)`: Securely fetches all projects owned by a specific client.
    * `sp_GetFreelancersBySkill(skill_name)`: Returns a ranked list of freelancers who possess a specific skill, ordered by their experience and average rating.

* **SQL Functions (FNs)**
    * `fn_get_project_app_count(project_id)`: A reusable function that returns the total application count for any given project.
    * `fn_HasSkill(freelancer_id, skill_name)`: A boolean function that quickly checks if a freelancer has a specific skill in their profile.

* **Triggers (TRGs)**
    * `trg_UpdateFreelancerRating`: An `AFTER INSERT` trigger on the `Reviews` table. When a new review is added, this trigger automatically recalculates the freelancer's `average_rating` and updates the `Freelancers` table. The admin dashboard reads this live value.
    * `trg_Prevent_Application_On_Closed_Project`: A `BEFORE INSERT` trigger on the `Applications` table. It checks the target project's status. If the status is not 'open', it blocks the insert and returns an error message to the user, ensuring data integrity.

## 🛠️ Tech Stack

* **Frontend:** **Streamlit** — For the interactive web UI.
* **Backend:** **Python**
* **Database:** **MySQL**
* **Core Python Libraries:**
    * `streamlit`
    * `mysql-connector-python`
    * `pandas` (for displaying analytics in the admin dashboard)

## ⚙️ Installation & Setup

Follow these steps to get the application running locally.

### 1. Prerequisites
* Python 3.8+
* A running MySQL Server (on `localhost` or a remote server)
* A MySQL client (like MySQL Workbench or a CLI)

### 2. Clone the Repository
```bash
git clone "shreeraksha-cs/freelancer-project-matching-platform"
cd freelancer-project-matching-platform
```

### 3. Run the app.py file
```bash
streamlit run app.py
```
