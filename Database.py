import pyodbc

# SSMS Configuration
SERVER = r"YEMINENIBALAJI\SQLEXPRESS"
DATABASE = "SQL PDF analysis"
USERNAME = "sa"
PASSWORD = "yemineni@123"

def get_connection():
    installed_drivers = pyodbc.drivers()
    if "ODBC Driver 17 for SQL Server" in installed_drivers:
        driver = "ODBC Driver 17 for SQL Server"
    elif "ODBC Driver 18 for SQL Server" in installed_drivers:
        driver = "ODBC Driver 18 for SQL Server"
    else:
        driver = "SQL Server" 

    # SSMS login main creditionals code
    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={SERVER};"
        f"DATABASE={{{DATABASE}}};" 
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        "TrustServerCertificate=yes;" 
    )

    try:
        return pyodbc.connect(connection_string)
    except Exception as e:
        print(f"❌ Database Connection Failed: {e}")
        return None


#registeration details
def register_user(username, email, password):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            check_query = "SELECT * FROM UserRegistration WHERE Username = ?"
            cursor.execute(check_query, (username,))
            if cursor.fetchone():
                return {"status": False, "message": "Username already exists!"}
            
            
            query = "INSERT INTO UserRegistration (Username, Email, Password) VALUES (?, ?, ?)"
            cursor.execute(query, (username, email, password))
            conn.commit()
            return {"status": True, "message": "Registration Successful!"}
        except Exception as e:
            print(f"SQL Error: {e}")
            return {"status": False, "message": str(e)}
        finally:
            conn.close()
    return {"status": False, "message": "Connection failed"}


# login details
def login_user(username, password):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT Username FROM UserRegistration WHERE Username = ? AND Password = ?"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            if user:
                return {"status": True, "username": user[0]}
            else:
                return {"status": False, "message": "Invalid credentials"}
        except Exception as e:
            print(f"SQL Error: {e}")
            return {"status": False, "message": str(e)}
        finally:
            conn.close()
    return {"status": False, "message": "Connection failed"}