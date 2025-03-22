# About

RecyclingProject is a web application designed to help users learn about and engage with recycling. It's built using the Django web framework.

## Features

-   **Homepage:** A public-facing landing page.
-   **Portal:** A section of the application likely for user accounts and more detailed recycling information.
-   **Admin Interface:** A Django admin interface for managing the application.

## Getting Started

### Prerequisites

-   Python 3.9+
-   pip (Python package installer)

### Installation

1.  Clone the repository:
    ```bash
    [git clone https://github.com/your-username/RecyclingProject.git](https://github.com/HokKwan1/recyclingProject.git)
    ```
2.  Navigate to the project directory:
    ```bash
    cd RecyclingProject/recyclingApplication
    ```
3.  Create a virtual environment (recommended):
    ```bash
    python3 -m venv venv
    ```
4.  Activate the virtual environment:
    -   On Windows:
        ```bash
        venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
5.  Install dependencies:
    ```bash
    pip install -r requirements.txt # you need to create this file
    ```
6.  Apply migrations:
    ```bash
    python manage.py migrate
    ```
7.  Start the development server:
    ```bash
    python manage.py runserver
    ```
8. Open your browser and go to `http://127.0.0.1:8000/`

## Usage

-   Visit the homepage to learn about the project.
-   Explore the portal(Admins and Volunteers) section for more features.

## Contributing

Contributions are welcome! Please see the `CONTRIBUTING.md` file for details.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact

Godfrey Kwan - hokkwanuol@gmail.com
