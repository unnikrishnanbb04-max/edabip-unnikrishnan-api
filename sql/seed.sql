USE reports_db;

INSERT INTO report_templates
(template_name, module, description)
VALUES
('Sales Summary Template', 'Sales', 'Daily sales summary'),
('Inventory Status Template', 'Inventory', 'Inventory availability report'),
('Customer Activity Template', 'Customers', 'Customer activity analysis'),
('Financial Summary Template', 'Finance', 'Financial performance report'),
('Employee Performance Template', 'HR', 'Employee performance report'),
('Order Analysis Template', 'Orders', 'Order analysis report'),
('Revenue Dashboard Template', 'Finance', 'Revenue dashboard report'),
('Product Performance Template', 'Products', 'Product performance report'),
('Attendance Template', 'HR', 'Employee attendance report'),
('Customer Support Template', 'Support', 'Customer support analysis');


INSERT INTO reports
(report_name, module, report_type, template_id, owner, status, last_run, run_time_seconds)
VALUES

('Daily Sales Report', 'Sales', 'Scheduled', 1, 'Arun', 'Completed', '2026-10-07 08:00:00', 35.50),

('Weekly Sales Report', 'Sales', 'Scheduled', 1, 'Priya', 'Completed', '2026-10-06 09:00:00', 42.30),

('Monthly Sales Report', 'Sales', 'Scheduled', 1, 'Karthik', 'Completed', '2026-10-01 10:00:00', 55.20),

('Inventory Stock Report', 'Inventory', 'Scheduled', 2, 'Divya', 'Scheduled', NULL, 0),

('Low Stock Report', 'Inventory', 'On Demand', 2, 'Arun', 'Completed', '2026-10-07 10:30:00', 22.10),

('Customer Activity Report', 'Customers', 'Scheduled', 3, 'Priya', 'Completed', '2026-10-07 07:30:00', 31.40),

('Inactive Customer Report', 'Customers', 'On Demand', 3, 'Karthik', 'Failed', '2026-10-06 14:00:00', 18.20),

('Financial Summary Report', 'Finance', 'Scheduled', 4, 'Divya', 'Completed', '2026-10-07 06:00:00', 65.80),

('Expense Report', 'Finance', 'On Demand', 4, 'Arun', 'Failed', '2026-10-05 11:00:00', 48.50),

('Employee Performance Report', 'HR', 'Scheduled', 5, 'Priya', 'Completed', '2026-10-07 08:30:00', 38.60),

('Employee Attendance Report', 'HR', 'Scheduled', 9, 'Karthik', 'Scheduled', NULL, 0),

('Order Analysis Report', 'Orders', 'Scheduled', 6, 'Divya', 'Completed', '2026-10-06 12:00:00', 52.40),

('Pending Orders Report', 'Orders', 'On Demand', 6, 'Arun', 'Completed', '2026-10-07 09:15:00', 27.80),

('Cancelled Orders Report', 'Orders', 'On Demand', 6, 'Priya', 'Failed', '2026-10-04 16:30:00', 21.60),

('Revenue Dashboard', 'Finance', 'Scheduled', 7, 'Karthik', 'Completed', '2026-10-07 07:00:00', 70.20),

('Quarterly Revenue Report', 'Finance', 'Scheduled', 7, 'Divya', 'Completed', '2026-10-01 07:00:00', 82.10),

('Product Performance Report', 'Products', 'Scheduled', 8, 'Arun', 'Completed', '2026-10-07 06:30:00', 44.70),

('Top Products Report', 'Products', 'On Demand', 8, 'Priya', 'Scheduled', NULL, 0),

('Product Sales Report', 'Products', 'Scheduled', 8, 'Karthik', 'Completed', '2026-10-06 13:00:00', 39.30),

('Attendance Summary', 'HR', 'Scheduled', 9, 'Divya', 'Completed', '2026-10-07 08:45:00', 29.50),

('Late Attendance Report', 'HR', 'On Demand', 9, 'Arun', 'Failed', '2026-10-05 09:30:00', 17.80),

('Customer Support Report', 'Support', 'Scheduled', 10, 'Priya', 'Completed', '2026-10-07 05:30:00', 46.20),

('Support Ticket Report', 'Support', 'On Demand', 10, 'Karthik', 'Completed', '2026-10-06 15:00:00', 33.10),

('Unresolved Tickets Report', 'Support', 'Scheduled', 10, 'Divya', 'Scheduled', NULL, 0),

('Daily Revenue Report', 'Finance', 'Scheduled', 7, 'Arun', 'Completed', '2026-10-07 09:00:00', 61.40),

('Regional Sales Report', 'Sales', 'On Demand', 1, 'Priya', 'Completed', '2026-10-06 17:00:00', 36.90),

('North Region Sales', 'Sales', 'Scheduled', 1, 'Karthik', 'Failed', '2026-10-05 18:00:00', 41.30),

('South Region Sales', 'Sales', 'Scheduled', 1, 'Divya', 'Completed', '2026-10-07 09:30:00', 39.80),

('Customer Growth Report', 'Customers', 'Scheduled', 3, 'Arun', 'Completed', '2026-10-06 10:00:00', 47.60),

('Customer Retention Report', 'Customers', 'On Demand', 3, 'Priya', 'Scheduled', NULL, 0),

('Inventory Movement Report', 'Inventory', 'Scheduled', 2, 'Karthik', 'Completed', '2026-10-07 04:30:00', 58.70),

('Inventory Valuation Report', 'Inventory', 'On Demand', 2, 'Divya', 'Failed', '2026-10-06 11:30:00', 49.20),

('Monthly Employee Report', 'HR', 'Scheduled', 5, 'Arun', 'Completed', '2026-10-01 08:00:00', 54.60),

('Order Revenue Report', 'Orders', 'Scheduled', 6, 'Priya', 'Completed', '2026-10-07 07:45:00', 43.90),

('Product Inventory Report', 'Products', 'On Demand', 8, 'Karthik', 'Scheduled', NULL, 0);