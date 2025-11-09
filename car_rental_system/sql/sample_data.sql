-- Sample seed data for Car Rental System

INSERT INTO car_class (class_name, daily_rate) VALUES
  ('Economy', 25.00),
  ('Sedan', 40.00),
  ('SUV', 70.00),
  ('Luxury', 150.00);

INSERT INTO branch (name, address) VALUES
  ('Main Branch', '123 Main Street'),
  ('Airport Branch', 'Airport Road');

INSERT INTO car (registration_no, vin, make, model, year, class_id, current_branch_id, status) VALUES
  ('MH12AB1234','VIN0001','Toyota','Corolla',2019,2,1,'available'),
  ('MH12CD5678','VIN0002','Hyundai','i20',2018,1,1,'available'),
  ('MH12EF9012','VIN0003','MG','Hector',2020,3,2,'available'),
  ('MH12GH3456','VIN0004','BMW','5 Series',2021,4,2,'available');

INSERT INTO customer (full_name, phone, email, license_no, address) VALUES
  ('Aman Kumar','+919876543210','aman@example.com','DL123456789','Mumbai'),
  ('Priya Sharma','+919812345678','priya@example.com','DL987654321','Pune');

-- One sample reservation
INSERT INTO reservation (customer_id, car_id, branch_id, start_dt, end_dt, status, total_amount) VALUES
  (1, 1, 1, '2025-11-10 10:00:00', '2025-11-12 10:00:00', 'booked', 80.0);
