document.getElementById("addTaskBtn").addEventListener("click", function() {
    var taskInput = document.getElementById("taskInput").value;
    if (taskInput) {
        var li = document.createElement("li");
        li.textContent = taskInput;
        li.addEventListener("click", function() {
            li.classList.toggle("completed");
        });
        document.getElementById("taskList").appendChild(li);
        document.getElementById("taskInput").value = ;
    }
}); 

