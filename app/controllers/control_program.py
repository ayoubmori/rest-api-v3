from fastapi import APIRouter, HTTPException
from app.constants.http_responces import ExampleResponseServerError,ResponseOK
from app.config.db import user
from app.models.user import Program
from bson import ObjectId
from bson.errors import InvalidId



control_prog= APIRouter(tags=["Control Program"])

@control_prog.post('/control-program',
        responses={
        200: {"model": ResponseOK
              , "description": "Successful response"},
        500: {
            "model": ExampleResponseServerError,
            "description": "Internal Server Error",
        },
    })
async def add_program(program: Program):
    try:
        # Convert string "_id" to ObjectId
        program_dict = program.dict()
        
        # Insert document into MongoDB collection
        result = user.insert_one(program_dict)
        print(program_dict)
        print(result)
        # Check if document was inserted successfully
        if result.inserted_id:
            return {"message": "Program added successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to add program")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@control_prog.get(
    "/control-program",
        responses={
        200: {"model": ResponseOK
              , "description": "Successful response"},
        500: {
            "model": ExampleResponseServerError,
            "description": "Internal Server Error",
        },
    }
)
async def get_all_programs():
    try:
        # Retrieve all documents from the MongoDB collection
        programs = list(user.find({}))
        
        # Convert ObjectId to string format
        for program in programs:
            program["_id"] = str(program["_id"])
        
        # Return the programs
        return programs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@control_prog.get(
    "/control-program/{id}",
    summary="Get Program by id ",
        responses={
        200: {"model": ResponseOK
              , "description": "Successful response"},
        500: {
            "model": ExampleResponseServerError,
            "description": "Internal Server Error",
        },
    }
)
async def get_program(program_id: str):
    try:
        # Attempt to convert the program_id to ObjectId
        program_id = ObjectId(program_id)
    except InvalidId:
        return {
            'status_code': 400,
            'message': 'Invalid program ID format'
        }

    program = user.find_one({"_id": program_id})
    if program :
        program["_id"] = str(program["_id"])
        return program
    else :
        return {
            'status_code':404,
            'message': 'Program does not exist'}
        
    
    
    
    
@control_prog.delete(
        "/control-program/{id}",
        summary="Delete Program by id ",
        responses={
        200: {"model": ResponseOK
              , "description": "Successful response"},
        500: {
            "model": ExampleResponseServerError,
            "description": "Internal Server Error",
        },
    }
)
async def delete_program(program_id: str):
    try:
        # Attempt to convert the program_id to ObjectId
        program_id = ObjectId(program_id)
    except InvalidId:
        return {
            'status_code': 400,
            'message': 'Invalid program ID format'
        }
    # Query the collection for the document with the specified _id
    program = user.find_one({"_id": program_id})
    if program :
        result = user.delete_one({"_id": program_id})
        if result.deleted_count == 1 :
            return {
                'status_code':200,
                'message': 'program deleted successfully'}
        else : 
            return {
                'status_code':500,
                'message': 'failed to deleted program'}
    else :
        return {
            'status_code':404,
            'message': 'program does not exist'}
