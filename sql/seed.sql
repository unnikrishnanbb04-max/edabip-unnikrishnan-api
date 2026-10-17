
USE reports_db;

INSERT INTO report_templates (template_name, module, description)
VALUES
('Sales Summary', 'Sales', 'Sales performance summary'),
('Finance Summary', 'Finance', 'Financial performance summary'),
('Employee Summary', 'HR', 'Employee information report'),
('Inventory Summary', 'Inventory', 'Stock and inventory report');

INSERT INTO reports
(report_name, module, report_type, template_id, owner, status, run_time)
VALUES
('Daily Sales', 'Sales', 'Scheduled', 1, 'admin', 'Completed', 1.2),
('Monthly Sales', 'Sales', 'Scheduled', 1, 'admin', 'Completed', 2.4),
('Quarterly Sales', 'Sales', 'On Demand', 1, 'admin', 'Failed', 0.8),
('Annual Sales', 'Sales', 'Scheduled', 1, 'admin', 'Scheduled', 0),
('Regional Sales', 'Sales', 'On Demand', 1, 'admin', 'Completed', 1.7),
('Customer Sales', 'Sales', 'Scheduled', 1, 'admin', 'Completed', 1.1),
('Product Sales', 'Sales', 'On Demand', 1, 'admin', 'Failed', 0.9),
('Sales Forecast', 'Sales', 'Scheduled', 1, 'admin', 'Scheduled', 0),
('Sales Targets', 'Sales', 'On Demand', 1, 'admin', 'Completed', 1.5),
('Sales Returns', 'Sales', 'Scheduled', 1, 'admin', 'Completed', 1.3),
('Profit and Loss', 'Finance', 'Scheduled', 2, 'admin', 'Completed', 2.5),
('Balance Sheet', 'Finance', 'Scheduled', 2, 'admin', 'Completed', 1.9),
('Cash Flow', 'Finance', 'On Demand', 2, 'admin', 'Failed', 0.7),
('Expense Report', 'Finance', 'Scheduled', 2, 'admin', 'Scheduled', 0),
('Tax Summary', 'Finance', 'On Demand', 2, 'admin', 'Completed', 1.4),
('Budget Analysis', 'Finance', 'Scheduled', 2, 'admin', 'Completed', 2.1),
('Invoice Summary', 'Finance', 'On Demand', 2, 'admin', 'Completed', 1.2),
('Payment Status', 'Finance', 'Scheduled', 2, 'admin', 'Failed', 0.6),
('Payroll Summary', 'HR', 'Scheduled', 3, 'admin', 'Completed', 1.8),
('Employee Attendance', 'HR', 'Scheduled', 3, 'admin', 'Completed', 1.1),
('Leave Summary', 'HR', 'On Demand', 3, 'admin', 'Scheduled', 0),
('Employee Directory', 'HR', 'On Demand', 3, 'admin', 'Completed', 0.9),
('Recruitment Summary', 'HR', 'Scheduled', 3, 'admin', 'Failed', 0.8),
('Training Report', 'HR', 'On Demand', 3, 'admin', 'Completed', 1.3),
('Stock Summary', 'Inventory', 'Scheduled', 4, 'admin', 'Completed', 1.6),
('Low Stock Alert', 'Inventory', 'Scheduled', 4, 'admin', 'Scheduled', 0),
('Warehouse Report', 'Inventory', 'On Demand', 4, 'admin', 'Completed', 1.4),
('Stock Movement', 'Inventory', 'Scheduled', 4, 'admin', 'Failed', 0.9),
('Purchase Summary', 'Inventory', 'On Demand', 4, 'admin', 'Completed', 1.7),
('Expired Products', 'Inventory', 'Scheduled', 4, 'admin', 'Completed', 1.0);
