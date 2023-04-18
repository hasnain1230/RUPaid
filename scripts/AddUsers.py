import mariadb
import getpass
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import gc


def insert_user(company_name, company_id, user_name, password, connection):
    cursor = connection.cursor()

    try:
        user_data = (company_name, company_id, user_name, password)
        cursor.execute("INSERT INTO users (company_name, company_id, user_name, password) VALUES (?, ?, ?, ?)", user_data)
        connection.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return

    # Check if the user was successfully added
    if cursor.rowcount == 1:
        print("User successfully added.")
    else:
        print("Error adding user.")
        return


def main():
    # Connect to MariaDB Platform
    try:
        connection = mariadb.connect(
            user='lucidity',
            password='lucidity',
            host='lucidityarch.com',
            port=3306,
            database='RUPaid'
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return

    cursor = connection.cursor()

    while True:
        company_name = input("Enter company name: ")
        company_id = input("Enter company ID: ")
        username = input("Enter username: ")

        cursor.execute("SELECT * FROM users WHERE user_name = ?", (username,))

        while cursor.fetchone() is not None:
            print("Username already exists. Please try again.")
            username = input("Enter username: ")
            cursor.execute("SELECT * FROM users WHERE user_name = ?", (username,))

        password = getpass.getpass("Enter password: ")
        password_hash = hashes.Hash(hashes.SHA3_512(), backend=default_backend())
        password_hash.update(password.encode())
        password = password_hash.finalize().hex()

        print("Adding user...")

        insert_user(company_name, company_id, username, password, connection)

        gc.collect()


if __name__ == '__main__':
    main()
