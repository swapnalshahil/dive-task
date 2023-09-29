## ![Dive logo](https://user-images.githubusercontent.com/424487/219708981-f0416526-ba48-4b01-b5b3-c0eb73362718.png) Dive 
## Work summary of the Octernship Task

### Task Instructions
- API Users can create an account and log in. Users are given access token using jwt
- Three roles given
    - Admin - CRUD operation on all users(admin, regular and manager role) as well as entries(records)
    - Manager - CRUD operation on users only with role 'regular'. They cannot access records of other users and cannot Delete any admin and manager.
    - Regular - CRUD operation on their own records
- Each entry can be made with what they have in their food, they can add date, time, and calorie of those food. However, here I take an assumption that very less people remember calorie of the food they are taking. So by giving only food items will work and it will add into the records with calories, date and time at which entry is done with the help of Calories API by (https://www.nutritionix.com/)
- Each user can set their expected daily calorie consumption. It is default set to 2000
- On each entry of user having access can see if the calorie intake is less than the expected number of calories per day through boolean.
- API's giving data through GET method having lists have filter capabilities and supports pagination.
- All API's are authenticated. Without access token it will not work.
- All API's return data in JSON format.
- Python Framework(FLASK) and SQLite Database which will be in instance/database.db after installing application properly.
- Maintained code quality, added comments and handled exceptions and error messages properly.

### Work Demonstration Video - [Youtube Link](https://www.youtube.com/watch?v=zb459GNLEeg)
### Installation and Setup

```
# Clone the repository
> git clone https://github.com/DiveHQ-Octernships/dive-backend-engineering-octernship-swapnalshahil.git
> cd dive-backend-engineering-octernship-swapnalshahil
# Create and activate virtual environment
> python -m venv myenv
> myenv\Scripts\activate
# Install dependencies
> pip install -r requirements.txt
# Set up environment variables .envsample file is given
> set FLASK_APP=app
# create database
> flask db upgrade
> flask run
# Application will run on http://localhost:5000 by default
# For API testing you can use Postman or any other API testing tool
```
### Endpoints

| Endpoints               | Methods | Access                                       | Rule                           |
|-------------------------|---------|----------------------------------------------|--------------------------------|
| register                | POST    | All                                          | /register                      |
| login                   | POST    | All                                          | /login                         |
| users.create            | POST    | admin & manager                              | /users/create                  |
| users.user_id           | GET     | admin & manager                              | /users/<user_id>               |
| users.user_id           | PUT     | admin & manager                              | /users/<user_id>               |
| users.user_id           | DELETE  | admin & manager(with cond.)                  | /users/<user_id>               |
| users.list              | GET     | admin & manager                              | /users/list                    |
| users.list              | GET     | admin & manager                              | /users/list?role=admin         |
| users.expected-calories | PUT     | All                                          | /users/expected-calories       |
| entries                 | GET     | admin(access all), others(their own entries) | /entries                       |
| entries                 | GET     | admin(access all), others(their own entries) | /entries?username=ram&food=tea |
| entries                 | POST    | All                                          | /entries                       |
| entries.entry_id        | GET     | admin(access all), others(their own entries) | /entries/<entry_id>            |
| entries.entry_id        | PUT     | admin(access all), others(their own entries) | /entries/<entry_id>            |
| entries.entry_id        | DELETE  | admin(access all), others(their own entries) | /entries/<entry_id>            |


### References
- [OpenMF by SCoRe Lab organization](https://github.com/scorelab/OpenMF) worked in this organization in Google Summer of Code [(Link)](https://summerofcode.withgoogle.com/archive/2021/projects/6260374466199552/)
- Flask Documentation [Link](https://flask.palletsprojects.com/en/2.3.x/)
- Python Environment [Link](https://docs.python.org/3/library/venv.html)
- Pythonist Youtube Channel [Playlist](https://youtube.com/playlist?list=PLMOobVGrchXN5tKYdyx-d2OwwgxJuqDVH)