# Retail Order Analysis App

## Overview

This project is a multi-page web application developed using [Streamlit](https://streamlit.io/) for analyzing retail order data. The app connects to a PostgreSQL database hosted on AWS RDS and provides insights into business operations and performance metrics. Each page of the app addresses different analytical questions to help derive actionable insights from the data.

## Features

- **Multi-Page Functionality:** Includes a main page and multiple sub-pages, each dedicated to specific analytical questions.
- **Business Insights:** Provides answers to 10 key business questions on the `Business Insights` page.
- **Database Connection:** Seamless integration with PostgreSQL on AWS RDS for real-time data access.
- **Streamlit-Based Interface:** Intuitive and interactive UI for easy navigation and data exploration.

## Pages

1. **Main Page (streamlit_app.py):**
   - Entry point for the application.
   - Provides an overview and navigation to other pages.

2. **Business Insights:**
   - Explores 5 analytical questions related to retail business performance.
   - Code implementation is in `pages/business_insights.py`.

3. **Additional Pages:**
   - Two more pages, each addressing 10 unique analytical questions.
   - Located in the `pages/` folder.
   - Designed to provide specialized insights and detailed data exploration.

## Prerequisites

To run this application, ensure the following are set up:

1. **Python Environment:**
   - Python 3.8 or later.
   - Install required packages using `requirements.txt`.
2. **PostgreSQL Database:**
   - Configure connection settings to the AWS RDS instance.
3. **Streamlit Installation:**
   - Install Streamlit using pip:
     ```bash
     pip install streamlit
     ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```bash
   cd retail-order-analysis-app
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Open the provided URL in your browser to access the application.

## Configuration

- **Database Settings:** Update the database connection details in the appropriate sections of the code (e.g., `streamlit_app.py`). Example:
  ```python
  DATABASE = {
      "host": "<AWS_RDS_ENDPOINT>",
      "port": 5432,
      "user": "<USERNAME>",
      "password": "<PASSWORD>",
      "dbname": "<DATABASE_NAME>"
  }
  ```

## Dependencies

Key Python packages used in this project:

- `streamlit`
- `psycopg2-binary`
- `pandas`
- `numpy`

Refer to `requirements.txt` for a complete list.

## File Structure

```
retail-order-analysis-app/
│
├── streamlit_app.py          # Main entry point for the app
├── pages/                    # Folder containing additional pages
│   ├── business_insights.py  # Code for the Business Insights page
│   ├── own_questions.py      # Additional analysis pages
│   ├── questions-by-guvi.py  # Additional analysis pages
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Future Enhancements

- Add visualizations to enhance data representation.
- Implement user authentication for secure access.
- Expand analysis with additional datasets.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Contact

For questions or feedback, please reach out to:

- **Name:** Arun
- **LinkedIn:** www.linkedin.com/in/arunkumar1811
