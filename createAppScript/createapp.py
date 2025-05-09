import os
from pathlib import Path
import subprocess
import sys
import pyppeteer
import asyncio
from dotenv import load_dotenv

load_dotenv()
# Your GitHub credentials
USERNAME = os.getenv('GITHUB_USERNAME')  # Make sure to set this environment variable
PASSWORD = os.getenv('GITHUB_PASSWORD')  # Make sure to set this environment variable
# print(f"Username: {USERNAME}")
# print(f"Password: {PASSWORD}")

# Check if the script is run with an argument
if len(sys.argv) < 2:
    print("Usage: python3 create_folder.py <folder_name>")
    sys.exit(1)

# Get the desktop path
project = Path.home() / "personal"/"appAutomation"

# Define the folder name
folder_name = sys.argv[1] if len(sys.argv[1]) > 1 else input("Enter the folder name: ")

# Create the folder path
folder_path = project / folder_name

# Create the folder if it doesn't exist
if not folder_path.exists():
    folder_path.mkdir()
    print(f"Folder '{folder_name}' created on your desktop.")
else:
    folder_name = input("Enter the folder name: ")
    folder_path = desktop / folder_name
    if not folder_path.exists():
        folder_path.mkdir()
        print(f"Folder '{folder_name}' created on your desktop.")
    else:
        print(f"Folder '{folder_name}' already exists on your desktop.")

# Change the current working directory to the created folder
os.chdir(folder_path)
print(f"Changed working directory to '{folder_path}'.")

# Run the npx create-react-app command with the folder name
os.system(f"npx create-react-app {folder_name}")

# Change the current working directory to the created folder
os.chdir(folder_name)
print(f"Changed working directory to '{folder_name}'.")

#Add a readme file
readme_path = folder_path / "README.md"
if not readme_path.exists():
    with open(readme_path, "w") as readme_file:
        readme_file.write(f"# {folder_name}\n\n")
        readme_file.write("This is a README file for the React app.\n")
    print(f"README file created at '{readme_path}'.")
else:
    print(f"README file already exists at '{readme_path}'.")

#run the gihublogin.py script with the github username and password as arguments

# os.chdir(desktop/"createAppScript")
# os.system(f"python3 githublogin.py {folder_name}")

#run the pyppeteer script to login to github

async def github_login():
    # Launch the browser
    browser = await pyppeteer.launch(headless=False)  # Set headless to True if you don't want to see the browser
    page = await browser.newPage()

    # Navigate to GitHub login page
    await page.goto('https://github.com/login')

    # Wait for the username input field to appear
    await page.waitForSelector('#login_field')

    # Fill in the username and password
    await page.type('#login_field', USERNAME)
    await page.type('#password', PASSWORD)

    # Click the login button
    await page.click('[name="commit"]')

    # Wait for navigation to complete
    await page.waitForNavigation()

    # Keep the browser open for 10 seconds to verify login
    await asyncio.sleep(5)
    print("Login successful. Creating repository...")

    await page.goto('https://github.com/new')
    print("Navigated to new repository page.")  
    await page.waitForSelector('.prc-Button-Label-pTQ3x')
    submitElements = await page.querySelectorAll('.prc-Button-Label-pTQ3x')
    print(f"Found {len(submitElements)} elements with the specified selector.")


    await page.waitForSelector('.prc-components-Input-Ic-y8')
    elements = await page.querySelectorAll('.prc-components-Input-Ic-y8')
    print(f"Found {len(elements)} elements with the specified selector.")
    print("Repository name input field is visible.")

    # Fill in the repository name and description
    await elements[0].type(folder_name)  # Get the repository name from command line argument
    await elements[1].type('This is a test repository created using pyppeteer.')
    await page.waitFor(1000)
    print("Filled in the repository name and description.")
    print("looking for the submit button")
    
    # # Wait for the create repository button to appear
    await page.waitForXPath('//button//span[text()="Create repository"]')
    create_button = await page.xpath('//button//span[text()="Create repository"]')
    await create_button[0].click()
    # Wait for the repository to be created
    await page.waitForNavigation()  
    # Wait for the repository page to load

    # Close the browser
    await browser.close()

# Run the async function
asyncio.run(github_login())

os.chdir(folder_path)

#run the git init command
os.system("git init")
print("Git repository initialized.")

try:
    subprocess.run(["git", "remote", "add", "origin", f"git@github.com:dreedsanders/{folder_name}.git"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Failed to add remote: {e}")

os.system("git branch -M main")
#run the git add command
os.system("git add .")
os.system('git commit -m "first commit"')
os.system("git push -u origin main")