import uuid
from django.shortcuts import render,redirect
import ollama
# from .models import Item, ItemImage
from .models import Todo,AITodoItemSteps
from .forms import*
from django.shortcuts import get_object_or_404

# Create your views here.


# class Learnmore:
#     pass




# def upload(request):
#     if request.method == "POST":
#         name = request.POST["name"]
#         description = request.POST["description"]
#         files = request.FILES.getlist("images")

#         item = Item.objects.create(name=name, description=description)

#         for file in files:
#             ItemImage.objects.create(item=item, image=file)

#         return redirect("list")

#     return render(request, "upload.html")

# def list(request):
#     items = Item.objects.all().order_by("-created_at")
#     return render(request, "list.html", {"items": items})


def index(request):
    todos = Todo.objects.all()
    return render(request, "index.html", {"todos": todos})

def add(request):
    if request.method == "GET":
        form=TodoForm()
        return render(request, "add_todo.html", {"form": form})
    elif request.method == "POST":
        form=TodoForm(request.POST)
        if form.is_valid():
            tittle=form.cleaned_data['title']
            description=form.cleaned_data['description']
           

            ai_todo_Item_steps=AITodoItemSteps(steps=[])

            example_todo_steps=AITodoItemSteps(steps=[  

                'Example 1',
                'Example 2',
                'Example 3',
                'Example 4',
                'Example 5',
            ])
            ai_prompt=f""" 
   Generate the steps required to complete the following tasks and return them as a JSON object:

   The following is the tittle of the task
   <task_tittle>
   {tittle}
   </task_tittle>

   The following is the description of the task
   <task_description>
   {description}
   </task_description>

   The following is an example of the exact format your JSON response should be in:
   <example>
   {example_todo_steps.model_dump_json()}  
    </example>

    Instructions:
    - Create a list of steps to complete the task based on the tittle and description provided.
    -Generate a valid JSON object that matches the above schema.
    - Return only a valid JSON object with no additional text,markdown or explanation.
    -Your output must be structured as shown in the example above with different, and real values.
    - Do not include '''or''' JSON in your response.
    -Do not wrap anything around JSON object.

"""          
            print(ai_prompt)
            responce=ollama.chat(model="llama3.2:1b",messages=[
                {"role": "user", "content": ai_prompt}
            ])
            content = responce['message']['content'].strip()

            print(content)

            ai_todo_Item_steps=AITodoItemSteps.model_validate_json(content)

            todo=Todo.objects.create(id=uuid.uuid4(),title=tittle, 
                                     description=description, 
                                     steps=[step for step in ai_todo_Item_steps.steps])
            return redirect('index')
         
    
def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.completed = True
    todo.save()
    return redirect('index')


def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return redirect('index')