-- no Create the database
-- CREATE DATABASE IF NOT EXISTS expense_tracker;
-- USE expense_tracker;

-- no Drop tables if they already exist
-- DROP TABLE IF EXISTS expenses;
-- DROP TABLE IF EXISTS categories;

-- no Create categories table
-- CREATE TABLE categories (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(50) UNIQUE NOT NULL
-- );

-- "no" Insert default categories
-- INSERT INTO categories (name) VALUES 
-- ('Food'), 
-- ('Travel'), 
-- ('Utilities'), 
-- ('Others');

-- "no" Create expenses table with 'description' column
-- CREATE TABLE expenses (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     date DATE NOT NULL,
--     category_id INT NOT NULL,
--     amount DECIMAL(10, 2) NOT NULL,
--     description TEXT,
--     FOREIGN KEY (category_id) REFERENCES categories(id)
-- );

-- Optional: View the expenses table (will be empty initially)
 -- USE expense_tracker;
-- SELECT * FROM expenses;
-- SELECT * FROM categories;
-- USE expense_tracker;
-- ALTER TABLE categories ADD COLUMN budget_limit DECIMAL(10, 2) DEFAULT 0.00;
-- UPDATE categories
-- SET budget_limit = 10000
-- WHERE name = 'Food';
-- UPDATE categories SET budget_limit = 8000 WHERE name = 'Travel';
-- UPDATE categories SET budget_limit = 5000 WHERE name = 'Utilities';
-- UPDATE categories SET budget_limit = 2000 WHERE name = 'Others';
-- USE expense_tracker;
-- SELECT * FROM expenses;

-- DELETE e FROM expenses e
-- JOIN categories c ON e.category_id = c.id
-- WHERE c.name = 'utilities';




