from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas

def create(db: Session, recipe: schemas.RecipeCreate):
    # Create a new instance of the Recipe model with the provided data
    db_recipe = models.Recipe(
        name=recipe.name,
        description=recipe.description,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions
    )
    # Add the newly created Recipe object to the database session
    db.add(db_recipe)
    # Commit the changes to the database
    db.commit()
    # Refresh the Recipe object to ensure it reflects the current state in the database
    db.refresh(db_recipe)
    # Return the newly created Recipe object
    return db_recipe

def read_all(db: Session):
    # Retrieve all rows in the Recipe table
    return db.query(models.Recipe).all()

def read_one(db: Session, recipe_id: int):
    # Retrieve a specific Recipe by its id
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return db_recipe

def update(db: Session, recipe_id: int, recipe: schemas.RecipeUpdate):
    # Query the database for the specific recipe to update
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    if not db_recipe.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    # Extract the update data from the provided 'recipe' object
    update_data = recipe.model_dump(exclude_unset=True)
    # Update the database record with the new data
    db_recipe.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated recipe record
    return db_recipe.first()

def delete(db: Session, recipe_id: int):
    # Query the database for the specific recipe to delete
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    if not db_recipe.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    # Delete the database record
    db_recipe.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
