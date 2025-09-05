#!/bin/bash

export PGPASSWORD="postgres"
psql -h localhost -p 5434 -U postgres -d postgres -f Department.sql
psql -h localhost -p 5434 -U postgres -d postgres -f Course.sql
psql -h localhost -p 5434 -U postgres -d postgres -f User.sql
psql -h localhost -p 5434 -U postgres -d postgres -f Student.sql
psql -h localhost -p 5434 -U postgres -d postgres -f Teacher.sql
# Create teacher with id DBT before running this
psql -h localhost -p 5434 -U postgres -d postgres -f Class.sql
psql -h localhost -p 5434 -U postgres -d postgres -f Session.sql
psql -h localhost -p 5434 -U postgres -d postgres -f Record.sql
psql -h localhost -p 5434 -U postgres -d postgres -f Enrollment.sql