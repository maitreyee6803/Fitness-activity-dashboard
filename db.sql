CREATE DATABASE fitness_tracker;
USE fitness_tracker;
CREATE TABLE workouts (
     id INT AUTO_INCREMENT PRIMARY KEY,
     workout_date DATE,
     exercise_type VARCHAR(100),
     duration_minutes INT,
     calories_burned INT
     );
SELECT * from workouts; 
SELECT * from workouts;    