# Medical Office Database Queries

Python application to query a medical office database using SQLAlchemy with raw SQL queries. The application connects to an Oracle database and performs various analytical queries.

## Prerequisites

- Python 3.7 or higher
- Oracle database connection details
- `pipenv` (`pip install pipenv` if not already installed)

## Installation

1. Download and enter the repository:
```bash
cd medical-office-sql
```

2. Install dependencies using pipenv:
```bash
pipenv install
```

This will create a virtual environment and install the following packages:
- sqlalchemy: SQL toolkit and ORM
- oracledb: Oracle database adapter for Python

## Configuration

1. Create your configuration file:
```bash
cp config.ini.example config.ini
```

2. Edit `config.ini` with your Oracle database connection details:
```ini
[database]
username = your_username
password = your_password
host = your_host
port = 1521
service_name = your_service
```

## Running the Application

1. Activate the virtual environment:
```bash
pipenv shell
```

2. Run the script:
```bash
python medical_queries.py
```

## Available Queries

The script executes four queries:

1. **Internal doctors named 'Daniel'**
   - Returns a list of doctors sorted by ID
   - Includes name, surname, and specialization

2. **Visits before 2002**
   - Returns the total count of visits before January 1st, 2002

3. **Doctors for patient "David Hill"**
   - Lists both internal and external doctors who visited this patient
   - Includes full names of all doctors

4. **Most frequent diagnosis**
   - Shows the diagnosis text that appears most often
   - Includes the number of occurrences

## Project Structure

```
medical_queries/
│
├── db # Scripts for database creation and data insertion
├── medical_queries.py   # Main application script
├── config.ini          # Database configuration (create from example)
├── config.ini.example  # Example configuration file
├── Pipfile            # Pipenv dependencies file
└── README.md          # Documentation
```

## Troubleshooting

Common issues and solutions:

1. **Database connection errors**
   - Verify your database credentials in `config.ini`
   - Ensure the database is accessible from your network
   - Check if the service name is correct

2. **Import errors**
   - Make sure you're running the script from within the pipenv environment
   - Verify all dependencies are installed: `pipenv install`

3. **Configuration errors**
   - Ensure `config.ini` exists and contains all required fields
   - Check file permissions

## Security Notes

- Never commit `config.ini` with real credentials
- Keep your `Pipfile.lock` in version control
- Consider using environment variables for sensitive data in production