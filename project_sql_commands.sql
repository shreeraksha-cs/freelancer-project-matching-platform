CREATE DATABASE IF NOT EXISTS freelancer_database;

USE freelancer_database;

-- Table: Clients
CREATE TABLE IF NOT EXISTS Clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    company_name VARCHAR(50),
    email VARCHAR(50) NOT NULL UNIQUE,
    phone_number VARCHAR(15)
);

-- Table: Freelancers
CREATE TABLE IF NOT EXISTS Freelancers (
    freelancer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    phone_number VARCHAR(15),
    -- The overall rating can be calculated via a view or trigger from the Reviews table.
    -- For simplicity, we omit it from the base table as it's derived data.
    average_rating DECIMAL(3, 2) DEFAULT 0.00
);

-- Table: Skills
CREATE TABLE IF NOT EXISTS Skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE
);

-- Table: Freelancer_Skills (Junction Table)
CREATE TABLE IF NOT EXISTS Freelancer_Skills (
    freelancer_id INT NOT NULL,
    skill_id INT NOT NULL,
    experience_years INT NOT NULL,
    PRIMARY KEY (freelancer_id, skill_id),
    FOREIGN KEY (freelancer_id) REFERENCES Freelancers(freelancer_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES Skills(skill_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table: Projects
CREATE TABLE IF NOT EXISTS Projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    budget DECIMAL(10, 2) NOT NULL,
    deadline DATETIME,
    status ENUM('open', 'in_progress', 'completed', 'cancelled') NOT NULL DEFAULT 'open',
    FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table: Applications
CREATE TABLE IF NOT EXISTS Applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    freelancer_id INT NOT NULL,
    proposal_text TEXT,
    bid_amount DECIMAL(10, 2) NOT NULL,
    application_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'accepted', 'rejected') NOT NULL DEFAULT 'pending',
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (freelancer_id) REFERENCES Freelancers(freelancer_id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (project_id, freelancer_id) -- A freelancer can apply to a project only once.
);

-- Table: Payments
CREATE TABLE IF NOT EXISTS Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    freelancer_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATETIME NOT NULL,
    status ENUM('pending', 'paid', 'failed') NOT NULL DEFAULT 'pending',
    FOREIGN KEY (project_id) REFERENCES Projects(project_id),
    FOREIGN KEY (freelancer_id) REFERENCES Freelancers(freelancer_id)
);

-- Table: Reviews
CREATE TABLE IF NOT EXISTS Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    client_id INT NOT NULL,
    freelancer_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    review_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (freelancer_id) REFERENCES Freelancers(freelancer_id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (project_id, client_id, freelancer_id) -- A client can only review a freelancer once per project.
);


INSERT INTO Clients (name, company_name, email, phone_number) VALUES
('Anitha', 'Innovatech Solutions', 'anitha@innovatech.com', '8734567898'),
('Paru', 'Solutions LLC', 'paru@solutions.llc', '6789874537'),
('Charlie', 'DesignWorks', 'charlie@designworks.com', '9830987654'),
('Ram', 'DataCorp', 'ram@datacorp.net', '87654321098'),
('Sara', 'MobileFirst Dev', 'sara@mobilefirst.dev', '9876543210');

INSERT INTO Freelancers (name, email, phone_number, average_rating) VALUES
('Mani', 'mani.chen@email.com', '9838764546', 4.80),
('Shivesh', 'shivesh.kim@email.com', '8763350044', 4.95),
('Tarun', 'tarun@email.com', '6644329873', 4.50),
('Naina', 'naina.patel@email.com', '7895093612', 0.00),
('Omar Ali', 'omar.ali@email.com', '9096543325', 4.75);

INSERT INTO Skills (skill_name) VALUES
('Python'),
('React'),
('SQL'),
('Graphic Design'),
('Project Management');

INSERT INTO Freelancer_Skills (freelancer_id, skill_id, experience_years) VALUES
(1, 1, 5), 
(1, 3, 4), 
(2, 2, 6),
(3, 4, 3), 
(5, 5, 8); 

INSERT INTO Projects (client_id, title, description, budget, deadline, status) VALUES
(1, 'AI Chatbot Integration', 'Integrate a Python-based AI chatbot into our customer service portal.', 5000.00, '2025-12-31 23:59:59', 'open'),
(2, 'E-commerce Frontend', 'Build a responsive e-commerce frontend using React.', 8000.00, '2026-01-15 23:59:59', 'open'),
(3, 'Company Logo Redesign', 'Create a modern and minimalist logo for DesignWorks.', 1500.00, '2025-11-30 23:59:59', 'in_progress'),
(4, 'Data Warehouse Migration', 'Migrate our existing sales data to a new SQL server.', 12000.00, '2026-03-01 23:59:59', 'completed'),
(5, 'Mobile App Marketing Plan', 'Develop a comprehensive marketing plan for our new mobile app.', 3000.00, '2025-12-20 23:59:59', 'cancelled');

INSERT INTO Applications (project_id, freelancer_id, proposal_text, bid_amount, application_date, status) VALUES
(1, 1, 'I am a Python expert with 5 years of experience and have built 3 chatbots.', 4800.00, '2025-10-25 10:30:00', 'pending'),
(2, 2, 'As a senior React developer, I can deliver this frontend project efficiently. See my portfolio.', 7900.00, '2025-10-26 11:00:00', 'accepted'),
(3, 3, 'My graphic design portfolio matches the minimalist style you are looking for.', 1450.00, '2025-10-20 14:00:00', 'accepted'),
(4, 1, 'I have 4 years of experience with SQL database migrations and ETL processes.', 11000.00, '2025-08-01 09:15:00', 'accepted'),
(1, 2, 'I can build the frontend interface for your Python chatbot using React.', 5000.00, '2025-10-26 12:00:00', 'rejected');

INSERT INTO Payments (project_id, freelancer_id, amount, payment_date, status) VALUES
(4, 1, 6000.00, '2025-09-15 10:00:00', 'paid'), -- Milestone 1 for Warehouse
(4, 1, 5000.00, '2025-10-10 11:30:00', 'paid'), -- Final payment for Warehouse
(3, 3, 700.00, '2025-10-22 16:45:00', 'paid'), -- Deposit for Logo
(2, 2, 4000.00, '2025-10-27 08:00:00', 'pending'), -- Milestone 1 for E-commerce
(3, 3, 750.00, '2025-11-01 12:00:00', 'pending'); -- Milestone 2 for Logo

INSERT INTO Reviews (project_id, client_id, freelancer_id, rating, comments, review_date) VALUES
(4, 4, 1, 5, 'Mani did an outstanding job on the data migration. Flawless execution and great communication.', '2025-10-11 09:00:00'),
(3, 3, 3, 4, 'Good creative direction for the logo, though the final delivery was a bit delayed.', '2025-12-05 17:00:00'),
(2, 2, 2, 5, 'Shivesh is a top-tier React developer. The frontend is fast, clean, and exactly what we wanted.', '2026-01-20 10:00:00'),
(1, 1, 1, 5, 'Great work on the chatbot!', '2026-01-05 14:30:00'),
(5, 5, 5, 3, 'The project was cancelled, but Omar provided a solid initial framework and was very professional.', '2025-12-22 11:00:00');

ALTER TABLE Projects 
MODIFY COLUMN status ENUM('open', 'in_progress', 'pending_approval', 'completed', 'cancelled') NOT NULL DEFAULT 'open';

-- Creates a simple table for admin users
CREATE TABLE IF NOT EXISTS Admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE
);

-- (Optional) Add a test admin so you can log in
INSERT INTO Admins (name, email) 
VALUES ('Admin User', 'admin@platform.com');


ALTER TABLE Clients
ADD COLUMN password VARCHAR(100) NOT NULL;

ALTER TABLE Freelancers
ADD COLUMN password VARCHAR(100) NOT NULL;

ALTER TABLE Admins
ADD COLUMN password VARCHAR(100) NOT NULL;

update Admins set password="adminpass" where admin_id=1;

update clients set password="anitha123" where client_id=1;
update clients set password="paru123" where client_id=2;
update clients set password="charlie123" where client_id=3;
update clients set password="Ram123" where client_id=4;
update clients set password="sara123" where client_id=5;

update freelancers set password="mani#xyz" where freelancer_id=1;
update freelancers set password="shivu#xyz" where freelancer_id=2;
update freelancers set password="tarun#xyz" where freelancer_id=3;
update freelancers set password="naina#xyz" where freelancer_id=4;
update freelancers set password="ali#xyz" where freelancer_id=5;