from django.db import models
from typing import List
from pydantic import BaseModel,Field

# class Item(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

# class ItemImage(models.Model):
#     item = models.ForeignKey(Item, related_name="images", on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="item_images/")
import uuid

class Todo(models.Model):
   id=models.UUIDField(primary_key=True, default=uuid.uuid4)
   title=models.CharField(max_length=200)
   description=models.TextField()
   steps=models.JSONField(default=list)
#    steps=models.JSONField()
   completed=models.BooleanField(default=False)

class AITodoItemSteps(BaseModel):
   steps: List[str] = Field([], description="List of steps for the todo item")