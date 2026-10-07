CREATE DATABASE IF NOT EXISTS reports_db;

USE reports_db;

DROP TABLE IF EXISTS report_activity;
DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS report_templates;


CREATE TABLE report_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    template_name VARCHAR(150) NOT NULL,
    module VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_name VARCHAR(200) NOT NULL,
    module VARCHAR(100) NOT NULL,

    report_type ENUM('Scheduled', 'On Demand') NOT NULL,

    template_id INT,

    owner VARCHAR(100) NOT NULL,

    status ENUM('Completed', 'Failed', 'Scheduled') NOT NULL DEFAULT 'Scheduled',

    last_run DATETIME NULL,

    run_time_seconds DECIMAL(10,2) DEFAULT 0,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reports_template
        FOREIGN KEY (template_id)
        REFERENCES report_templates(id)
        ON DELETE SET NULL
);


CREATE TABLE report_activity (
    id INT AUTO_INCREMENT PRIMARY KEY,

    report_id INT NOT NULL,

    action VARCHAR(100) NOT NULL,

    status ENUM('Completed', 'Failed', 'Scheduled') NOT NULL,

    message VARCHAR(500),

    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    completed_at DATETIME NULL,

    run_time_seconds DECIMAL(10,2) DEFAULT 0,

    CONSTRAINT fk_activity_report
        FOREIGN KEY (report_id)
        REFERENCES reports(id)
        ON DELETE CASCADE
);