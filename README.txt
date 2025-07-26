Placement Eligibility Streamlit App
===================================

Overview:
---------
This is a simple and interactive Streamlit web application designed to manage and view student placement eligibility data.

The app connects to a TiDB cloud database and allows users to:

- Search for students by name
- View detailed student information across:
  - Student Info
  - Programming Skills
  - Soft Skills
  - Placement Info
- Download individual student details in Excel format

Folder Structure:
-----------------
Placement_Eligibility_App/
│
├── app.py                -> Main Streamlit application
├── db_config.py          -> Database configuration (credentials)
├── db_connector.py       -> Handles all database interactions and queries
├── student_manager.py    -> Provides business logic for managing student data (optional abstraction layer)
├── exporter.py           -> Exports selected student data into Excel format
├── Certs/                -> SSL certificate for TiDB (e.g., isrgrootx1.pem)
└── README.txt            -> Project documentation (this file)

Setup Instructions:
-------------------
1. Clone the repository:
   git clone https://github.com/your-username/Placement_Eligibility_App.git
   cd Placement_Eligibility_App

2. Install required Python packages:
   pip install streamlit pandas xlsxwriter mysql-connector-python

3. Ensure you have your TiDB SSL certificate:
   Place it in the `Certs/` folder as `isrgrootx1.pem`

4. Check your database configuration in `db_config.py`:
   Example:
   db_config = {
       'host': 'your_tidb_host',
       'user': 'your_tidb_user',
       'password': 'your_password',
       'database': 'Student_Info',
       'port': 4000,
       'ssl_ca': 'Certs/isrgrootx1.pem'
   }

How to Run:
-----------
Run the application using:
   streamlit run app.py

Once it launches, the app will open in your browser at http://localhost:8501

Features:
---------
- Search for students by name using the sidebar
- View:
  - 🎓 Student Info
  - 💻 Programming Skills
  - 🧠 Soft Skills
  - 📈 Placement Info
- Export selected student’s data into an Excel file with one click
  (handled via `ExcelExporter` in `exporter.py`)
- Clean separation of logic using `student_manager.py` (used for future enhancements or data validations)
- Show top 10 performers by programming, soft skills, and placement


Future Enhancements:
--------------------
- Add charts or visualizations
- Placement statistics and analytics
- Batch-wise filtering

Contributing:
-------------
Pull requests are welcome. If you wish to make major changes, open an issue first to discuss it.


