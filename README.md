# Welcome to the Inventory Management System

Congratulations on choosing the Inventory Management System! Whether you're managing a small inventory for a startup or a large warehouse for an enterprise, this Django-based application is here to make your life easier. Let's dive right in.

---

## What Can This App Do for You?

- **Manage Buildings and Materials**: Effortlessly add and organize inventory items across multiple buildings.
- **Track Stock Levels**: Keep an eye on your stock with real-time calculations for available, inward, and issued quantities.
- **Powerful Search and Sort**: Quickly find what you need with intuitive search and sorting features.
- **Generate Reports**: Get detailed insights on inventory consumption to make informed decisions.
- **User-Friendly Design**: Designed for everyone, from first-time users to seasoned professionals.

---

## Before You Begin

Here’s what you’ll need:

- Python (version 3.8 or higher).
- pip (it usually comes with Python).
- Git for cloning the repository.
- A browser (Chrome, Firefox, Edge — your choice).

### Optional But Helpful:

- A code editor like VS Code or PyCharm to explore the code.
- Virtualenv to keep your dependencies neat and tidy.

---

## How to Get This Up and Running?

Follow these foolproof steps:

### 1. Grab the Code
First things first, clone the repository to your local machine. Open your terminal and type:

```bash
git clone <repository-url>
cd Inventory-Management-System
```

### 2. Create Your Personal Workspace (Virtual Environment)
Make sure your workspace doesn’t interfere with your global Python setup:

```bash
python -m venv myenv
```

Now, activate the virtual environment:

- **Windows**:
  ```bash
  .\myenv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source myenv/bin/activate
  ```

You should see your virtual environment name in your terminal prompt now. Cool, right?

### 3. Load Up the Essentials
Install all the dependencies your app needs:

```bash
pip install -r requirements.txt
```

This step ensures Django and all other necessary libraries are ready to roll.

### 4. Set Up Your Database
Django comes with a built-in SQLite database. Let’s make sure it’s ready:

```bash
python manage.py migrate
```

This command creates all the tables and structures required.

### 5. Fire Up the Server
Run the development server and get your app online locally:

```bash
python manage.py runserver
```

Pop open your browser and type:

```
http://127.0.0.1:8000/
```

Your Inventory Management System is now live!

---

## How to Use It (For Beginners)

### Adding a Building
1. Navigate to the **Add Building** page (find it in the menu).
2. Fill out the details (Building Name, Address, etc.).
3. Hit **Save** and voilà — your building is added!

### Managing Inventory
- Use the **View All Inventory** page to see a list of all items.
- Search for materials using keywords like name, type, or supplier.
- Sort the list by quantity, name, or any other field.

### Tracking Stock
- View inward, issued, and available stock directly on the inventory page.
- Use the search and sort features to focus on specific materials or buildings.

### Generating Reports
Need insights? Head to the **Consumption Report** page to get detailed stats on your inventory.

---

## Troubleshooting for Beginners

### Activation Fails on Windows?

If you see an error about script execution, do this:

1. Open PowerShell as Admin.
2. Run:
   ```bash
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```
3. Retry activating your virtual environment.

### Something’s Not Working?
- Double-check your Python version.
- Make sure your virtual environment is activated.
- Re-run migrations:
  ```bash
  python manage.py migrate
  ```

---

## Contribute to the Project
Want to make this app better? Here’s how:

1. Fork the repo.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and test them.
4. Push your branch and submit a pull request!

---

## Shoutout to You
Thank you for using the Inventory Management System! Have feedback? Ideas? Bugs? Let us know and we’ll make it even better together.

---

## License

Happy Inventory Managing! 🚀

