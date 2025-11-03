# Tauha Imran| Buildables AI Fellowship – Week 6 Task 1  
# [LinkedIn](https://www.linkedin.com/in/tauha-imran-6185b3280/) 
# [GitHub](https://github.com/tauhaimran)
# [Portfolio](https://tauhaimran.github.io/)  

# *** Task 1 — Basic RESTful API in Flask ***
from flask import Flask , request , jsonify

app = Flask(__name__)
todos = [{"id": 1, "task": "Buy groceries"}] # this thingy creates a database in the memory

#define a route - GET/todos
#apparently this runs whenever someone opens this route/webpage
@app.route("/todos" , methods=["GET"])
def get_todos(): # my function to get the todos
    return jsonify( todos) , 200 # 200 is the status code for success

#define a route - POST/todos
@app.route("/todos" , methods=["POST"])
def add_todo(): # function to add a todo
    data = request.get_json() # get the data from the request
    if not data or "task" not in data:# if no data or no task field
        return jsonify({"error": "Missing 'task' field"}) , 400 # return error message with status code 400 (bad request)
    new_todo = {"id": len(todos) + 1 , "task": data["task"]} # if data is valid - create a new todo item
    todos.append(new_todo) # add the new todo to the list
    return jsonify(new_todo) , 201 # return the new todo with status code 201 (created)


if __name__ == "__main__":
    app.run(debug=True)
