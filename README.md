# Bloggitt

Bloggitt is a basic blogging application which allows user to post and view blogs.

## Tech Stack
- **Frontend:** HTML/CSS, Bootstrap
- **Backend:** Django


## Quick Start :

- **Fork it** :

Get your own Fork/Copy of repository by clicking `Fork` button right upper corner.<br><br>

- **Clone**:

```sh
$ git clone https://github.com/diyajaiswal11/Bloggitt.git
```

- **Branching**
```
$ git checkout -b [your_branch_name]
```

- **Make Changes in Source Code**

#### Setting up Project

- Create a Virtual Environment
```
python3 -m venv env
```

- Activate the Virtual Environment
  - On Windows
    ``` 
    env\Scripts\activate
    ```
  - On Linux or MAC
    ```
    source env/bin/activate
    ```
    
- Headover to Project 
```
cd bloggitt
```
- Install dependencies using
```
pip install -r requirements.txt
```
- Make migrations using
```
python manage.py makemigrations
```
- Migrate Database
```
python manage.py migrate
```
- Create a superuser
```
python manage.py createsuperuser
```
- Run server using
```
python manage.py runserver
```

- **Stage your Changes and Commit**
```
# For adding/Staging Changes

$ git add .


# For Commiting Changes

$ git commit -m "<your commit message>"

```

- **Push your Commit to Repo**
```
$ git push origin <branch_name>
```
