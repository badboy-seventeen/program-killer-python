# program-killer-python
A windows based program killer written in python. Used to kill running programs in windows by storing their name in a sqlite3 database.

# Usage
### 1. First run the ' kill.py ' file.
### 2. Add
##### Add program names with extension ( e.g .exe ) to database by using main.py commands.
```
main.py -a | --add ( name )
```
---

### 3. Show 
##### To see added programs in database use:
```
main.py -s | --show
```
---

### 4. Remove
##### To remove a program from database use:
```
main.py -r | --remove
```
---

### 5. Delete All
##### To remove all programs from database use:
```
main.py --del-all
```
---

### 6. Delete Database
##### To delete the database itself use:
```
main.py --del-db
```
---
### 7. Create Database
##### To create the database use:
```
main.py --create-db
```
---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
