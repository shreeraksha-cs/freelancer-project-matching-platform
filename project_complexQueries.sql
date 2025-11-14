
USE freelancer_database;

-- 1. FIVE COMPLEX QUERIES
-- Query 1: Freelancer Earning Ranks and Tiers
SELECT 
    freelancer_name, 
    total_earned, 
    earning_rank,
    CASE 
        WHEN earning_rank = 1 THEN 'Top Earner'
        WHEN earning_rank <= 3 THEN 'Mid Tier Earner'
        ELSE 'Standard Earner'
    END AS earning_tier
FROM (
    SELECT 
        f.name AS freelancer_name, 
        SUM(p.amount) AS total_earned,
        ROW_NUMBER() OVER (ORDER BY SUM(p.amount) DESC) AS earning_rank
    FROM Freelancers f
    JOIN Payments p ON f.freelancer_id = p.freelancer_id
    WHERE p.status = 'paid'
    GROUP BY f.freelancer_id, f.name
) AS RankedFreelancers;

-- Query 2: Projects Where the Average Bid is Below Budget
SELECT
    p.title,
    p.budget,
    AVG(a.bid_amount) AS average_bid
FROM
    Projects p
JOIN
    Applications a ON p.project_id = a.project_id
GROUP BY
    p.project_id, p.title, p.budget
HAVING
    AVG(a.bid_amount) < p.budget;

-- Query 3: Client's Project Budget vs. Their Average
WITH ClientAvgBudget AS (
    SELECT
        client_id,
        AVG(budget) AS avg_client_budget
    FROM
        Projects
    GROUP BY
        client_id
)
SELECT
    p.title,
    c.name AS client_name,
    p.budget,
    cab.avg_client_budget,
    (p.budget - cab.avg_client_budget) AS budget_difference
FROM
    Projects p
JOIN
    Clients c ON p.client_id = c.client_id
JOIN
    ClientAvgBudget cab ON p.client_id = cab.client_id
ORDER BY
    client_name, budget_difference DESC;

-- Query 4: Freelancers Without "Python" Skill
SELECT
    f.name,
    f.email
FROM
    Freelancers f
WHERE
    NOT EXISTS (
        SELECT 1
        FROM Freelancer_Skills fs
        JOIN Skills s ON fs.skill_id = s.skill_id
        WHERE fs.freelancer_id = f.freelancer_id
          AND s.skill_name = 'Python'
    );

-- Query 5: Top Experienced Freelancer per Skill
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

-- TRIGGERS
DELIMITER //

-- Trigger 1: Update Freelancer's Average Rating
CREATE TRIGGER trg_UpdateFreelancerRating
AFTER INSERT ON Reviews
FOR EACH ROW
BEGIN
    UPDATE Freelancers f
    SET f.average_rating = (
        SELECT AVG(r.rating)
        FROM Reviews r
        WHERE r.freelancer_id = NEW.freelancer_id
    )
    WHERE f.freelancer_id = NEW.freelancer_id;
END//

-- Trigger 2: Prevent Application to Closed Projects
CREATE TRIGGER trg_check_project_status_before_apply
BEFORE INSERT ON Applications
FOR EACH ROW
BEGIN
    DECLARE proj_status ENUM('open', 'in_progress', 'completed', 'cancelled');
    
    SELECT status
    INTO proj_status
    FROM Projects
    WHERE project_id = NEW.project_id;
    
    IF proj_status IN ('completed', 'cancelled') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot apply to a project that is already completed or cancelled.';
    END IF;
END//

--FUNCTIONS
-- Function 1: Get Project Application Count
CREATE FUNCTION fn_get_project_app_count(p_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE app_count INT;
    
    SELECT COUNT(*)
    INTO app_count
    FROM Applications
    WHERE project_id = p_id;
    
    RETURN app_count;
END//

-- Function 2: Check if Freelancer Has a Specific Skill
CREATE FUNCTION fn_HasSkill(f_id INT, s_name VARCHAR(100))
RETURNS BOOLEAN
DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE skill_count INT;
    
    SELECT COUNT(*) INTO skill_count
    FROM Freelancer_Skills fs
    JOIN Skills s ON fs.skill_id = s.skill_id
    WHERE fs.freelancer_id = f_id AND s.skill_name = s_name;
    
    RETURN skill_count > 0;
END//

--PROCEDURES
-- Procedure 1: Get Top Freelancers by Skill
CREATE PROCEDURE sp_GetFreelancersBySkill(IN s_name VARCHAR(100))
BEGIN
    SELECT 
        f.name, 
        f.email, 
        f.average_rating, 
        fs.experience_years
    FROM Freelancers f
    JOIN Freelancer_Skills fs ON f.freelancer_id = fs.freelancer_id
    JOIN Skills s ON fs.skill_id = s.skill_id
    WHERE s.skill_name = s_name
    ORDER BY fs.experience_years DESC, f.average_rating DESC;
END//

-- Procedure 2: Takes a client's ID as input and returns a list of all projects associated with that client.
CREATE PROCEDURE sp_GetClientProjects(IN input_client_id INT)
BEGIN
    SELECT 
        project_id,
        title,
        description,
        budget,
        status,
        deadline
    FROM 
        Projects
    WHERE 
        client_id = input_client_id
    ORDER BY 
        deadline DESC;
END//

DELIMITER ;

-- Part 5: User Permissions Demonstration
CREATE USER 'admin_user'@'localhost' IDENTIFIED BY 'admin_password';
CREATE USER 'client_user'@'localhost' IDENTIFIED BY 'client_password';
CREATE USER 'freelancer_user'@'localhost' IDENTIFIED BY 'freelancer_password';

-- 1. Admin User: Full privileges on the entire database
GRANT ALL PRIVILEGES ON freelancer_database.* TO 'admin_user'@'localhost';

-- 2. Client User:
GRANT SELECT ON freelancer_database.* TO 'client_user'@'localhost';
GRANT INSERT, UPDATE ON freelancer_database.Projects TO 'client_user'@'localhost';
GRANT INSERT ON freelancer_database.Reviews TO 'client_user'@'localhost';
GRANT INSERT, UPDATE ON freelancer_database.Payments TO 'client_user'@'localhost';
GRANT EXECUTE ON PROCEDURE freelancer_database.sp_GetClientProjects TO 'client_user'@'localhost';
GRANT EXECUTE ON PROCEDURE freelancer_database.sp_GetFreelancersBySkill TO 'client_user'@'localhost';
GRANT EXECUTE ON FUNCTION freelancer_database.fn_get_project_app_count TO 'client_user'@'localhost';

-- 3. Freelancer User:
-- Limited SELECT access
GRANT SELECT ON freelancer_database.Projects TO 'freelancer_user'@'localhost';
GRANT SELECT ON freelancer_database.Skills TO 'freelancer_user'@'localhost';
GRANT SELECT (client_id, name, company_name) ON freelancer_database.Clients TO 'freelancer_user'@'localhost'; -- Can see client names, but not email/phone
GRANT SELECT ON freelancer_database.Reviews TO 'freelancer_user'@'localhost'; -- Can read all reviews
GRANT INSERT, UPDATE (proposal_text, bid_amount) ON freelancer_database.Applications TO 'freelancer_user'@'localhost';
GRANT SELECT ON freelancer_database.Payments TO 'freelancer_user'@'localhost';
GRANT EXECUTE ON PROCEDURE freelancer_database.sp_GetClientProjects TO 'freelancer_user'@'localhost';
GRANT EXECUTE ON FUNCTION freelancer_database.fn_get_project_app_count TO 'freelancer_user'@'localhost';
GRANT EXECUTE ON FUNCTION freelancer_database.fn_HasSkill TO 'freelancer_user'@'localhost';

-- Apply the new permissions
FLUSH PRIVILEGES;
