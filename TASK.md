[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/085htE_I)
## ![Dive logo](https://user-images.githubusercontent.com/424487/219708981-f0416526-ba48-4b01-b5b3-c0eb73362718.png) Dive 
<!-- ![Company Logo](https://example.org) -->

| Octernship info  | Timelines and Stipend |
| ------------- | ------------- |
| Assignment Deadline  | 19th June 2023  |
| Octernship Duration  | 3rd July 2023 - 3rd October 2023 |
| Monthly Stipend  | $500 USD  |

## Assignment


# Write a REST API for the input of calories in Python

### Task Instructions
- API Users must be able to create an account and log in.
- All API calls must be authenticated.
- Implement at least three roles with different permission levels: a regular user would only be able to CRUD on their owned records, a user manager would be able to CRUD only users, and an admin would be able to CRUD all records and users.
- Each entry has a date, time, text, and number of calories.
- If the number of calories is not provided, the API should connect to a Calories API provider (for example, https://www.nutritionix.com) and try to get the number of calories for the entered meal.
- User setting – Expected number of calories per day.
- Each entry should have an extra boolean field set to true if the total for that day is less than the expected number of calories per day, otherwise should be false.
- The API must be able to return data in the JSON format.
- The API should provide filter capabilities for all endpoints that return a list of elements, as well should be able to support pagination.
- Write unit and e2e tests.
- Use any *Python* web framework
- Use *SQLite* as the database

### Task Expectations
- API Design Best Practices
- Documentation of any assumptions or choices made and why
- Links as citation to any article / code referred to or used
- Unit tests covering the core calories logic
- Appropriate exception handling and error messages
- Code Quality - remove any unnecessary code, avoid large functions
- Good commit history - we won’t accept a repo with a single giant commit 🙅‍♀️


