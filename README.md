# Project Title

This project is a Flask application that integrates with GitHub webhooks to retrieve repository data and store it in a MySQL database.

## Prerequisites

- Python 3.x
- MySQL
- GitHub account and repository
- NGINX (for deployment)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure the MySQL database:
    ```ini
    [CONFIG]
    MYSQL_USER=root
    MYSQL_PW=yourpassword
    MYSQL_HOST=localhost
    MYSQL_DB=yourdatabase
    MYSQL_PORT=3306
    GIT_TOKEN=your_github_token
    ```

4. Update the `config.ini` file with your MySQL and GitHub credentials.

## Usage

1. Run the Flask application:
    ```sh
    python flask/app.py
    ```

2. Set up GitHub webhook to point to your Flask application endpoint:
    ```
    http://yourdomain.com/webhook
    ```

3. Test the connection by accessing:
    ```
    http://yourdomain.com/test
    ```

## File Structure

- `config.ini`: Configuration file for MySQL and GitHub credentials.
- `library/db_connection.py`: Contains the `DBConnect` class for database operations.
- `library/git_retrieve.py`: Contains the `GitRetrieve` class for interacting with the GitHub API.
- `flask/app.py`: Main Flask application file.
- `flask/templates/test.html`: HTML template for testing the connection.
