**Installation Manual for Enhanced Job Posting Website**  

This manual provides step-by-step instructions to install and set up the Enhanced Job Posting Website on a local server. Follow these steps carefully to ensure a smooth installation process.  

---

### **1. System Requirements**  
Ensure your system meets the following hardware and software specifications:  

#### **Hardware Requirements:**  
- **Processor:** Intel Pentium or equivalent (Intel Core i3 or higher recommended).  
- **RAM:** Minimum 2GB (4GB or more recommended).  
- **Disk Space:** At least 10GB of free space.  
- **Internet Connection:** Stable connection for downloading dependencies.  

#### **Software Requirements:**  
- **Operating System:** Windows 10/11 (64-bit).  
- **Python:** Version 3.11 or higher.  
- **Django:** Version 5.0 or later.  
- **PostgreSQL:** Version 17 or higher.  
- **Git:** For cloning the repository.  
- **Pip:** Python package manager.  

---

### **2. Installation Steps**  

#### **Step 1: Install Python**  
1. Download the latest Python installer from the [official Python website](https://www.python.org/downloads/).  
2. Run the installer and check the box **"Add Python to PATH"** during installation.  
3. Verify the installation by opening Command Prompt and running:  
   ```bash  
   python --version  
   ```  
   This should display the installed Python version (e.g., `Python 3.11.0`).  

#### **Step 2: Install PostgreSQL**  
1. Download PostgreSQL from the [official website](https://www.postgresql.org/download/).  
2. Follow the installation prompts. When prompted, set a secure password for the default `postgres` user.  
3. Verify the installation by running:  
   ```bash  
   psql --version  
   ```  
   This should display the installed PostgreSQL version (e.g., `psql (PostgreSQL) 17.0`).  

#### **Step 3: Install Git**  
1. Download Git from the [official website](https://git-scm.com/downloads).  
2. Verify the installation by running:  
   ```bash  
   git --version  
   ```  

#### **Step 4: Clone the Project Repository**  
1. Open Command Prompt and navigate to your desired directory (e.g., `cd C:\Projects`).  
2. Clone the repository using:  
   ```bash  
   git clone https://github.com/mirage4mira/fyp-myjobs-django.git  
   ```  
3. Navigate into the project folder:  
   ```bash  
   cd fyp-myjobs-django  
   ```  

#### **Step 5: Set Up a Virtual Environment**  
1. Create a virtual environment to isolate dependencies:  
   ```bash  
   python -m venv venv  
   ```  
2. Activate the virtual environment:  
   ```bash  
   venv\Scripts\activate  
   ```  
   *(Note: Your Command Prompt should now display `(venv)` at the beginning.)*  

#### **Step 6: Install Dependencies**  
1. Install required packages using:  
   ```bash  
   pip install -r requirements.txt  
   ```  

#### **Step 7: Configure the Database**  
1. Open **pgAdmin** (installed with PostgreSQL) and create a new database named `myjobs`.  
2. Update the database configuration in the project’s `settings.py` file:  
   - Locate the `DATABASES` section.  
   - Replace the default settings with:  
     ```python  
     DATABASES = {  
         'default': {  
             'ENGINE': 'django.db.backends.postgresql',  
             'NAME': 'myjobs',  
             'USER': 'postgres',  
             'PASSWORD': 'your_postgres_password',  # Replace with your password  
             'HOST': 'localhost',  
             'PORT': '5432',  
         }  
     }  
     ```  

#### **Step 8: Apply Database Migrations**  
1. Run the following commands to set up the database tables:  
   ```bash  
   python manage.py migrate  
   ```  

#### **Step 9: Run the Development Server**  
1. Start the server:  
   ```bash  
   python manage.py runserver  
   ```  
2. Access the website at:  
   ```  
   http://127.0.0.1:8000  
   ```  

---

### **3. Troubleshooting**  
- **Python not recognized:** Ensure Python is added to the system PATH during installation.  
- **PostgreSQL connection errors:** Verify credentials in `settings.py` and ensure the `myjobs` database exists.  
- **Port conflicts:** If port `8000` is in use, run:  
  ```bash  
  python manage.py runserver 8080  
  ```  
  Then access the site at `http://127.0.0.1:8080`.  

---

### **4. Conclusion**  
The Enhanced Job Posting Website is now installed and ready for use. For further assistance, refer to the project documentation or contact the development team.  

**Note:** This manual assumes a Windows environment. Adjust paths/commands for other operating systems as needed.  

---  
**End of Manual**  

Let me know if you'd like any modifications or additional details!