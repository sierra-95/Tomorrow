use Tomorrow

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    dob DATE,
    password VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    event_name VARCHAR(255),
    event_date DATE,
    event_description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS FutureMeLetters (
    letter_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    letter_name VARCHAR(50),
    letter_content TEXT,
    delivery_date DATE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Goals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    writer_id INT,
    goal_content TEXT,
    due_date DATE,
    FOREIGN KEY (writer_id) REFERENCES users(id) ON DELETE CASCADE
);


