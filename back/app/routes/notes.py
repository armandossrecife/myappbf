from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import banco
from app import seguranca
from app import entidades

router = APIRouter()

@router.post("/users/{username}/notes", dependencies=[Depends(seguranca.get_current_user)])
async def create_note(username: str, nota: entidades.Note, db: Session = Depends(banco.get_db)):
    """ Creates a new note for the user identified by username.
    Args:
        username: Username of the user creating the note.
        description: Note object containing the note description.
    Returns:
        The created Note object.
    Raises:
        HTTPException: If note creation fails.
    """
    user_dao = banco.UserDAO(db)
    user = user_dao.get_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        notes_dao = banco.NotesDAO(db)
        created_note = notes_dao.create_note(user.id, nota.description)
        return created_note
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating note: {str(e)}")

@router.get("/users/{username}/notes", dependencies=[Depends(seguranca.get_current_user)])
async def get_all_notes(username: str, db: Session = Depends(banco.get_db)):
    """ Retrieves all notes for the user identified by username.
    Requires authentication of the requesting user.
    Args:
        username: Username of the user for whom to retrieve notes.
    Returns:
        A list of Note objects belonging to the specified user.
    Raises:
        HTTPException: If user is not found or unauthorized to access notes.
    """
    user_dao = banco.UserDAO(db)
    user = user_dao.get_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        notes_dao = banco.NotesDAO(db)
        all_notes = notes_dao.get_all_notes_by_user(user.id)
        return all_notes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving notes: {str(e)}")

@router.get("/users/{username}/notes/{note_id}", dependencies=[Depends(seguranca.get_current_user)])
async def get_note_by_id(username: str, note_id: int, db: Session = Depends(banco.get_db)):
    """ Retrieves a specific note for the user identified by username.
    Requires authentication of the requesting user.
    Args:
        username: Username of the user for whom to retrieve the note.
        note_id: ID of the specific note to retrieve.
    Returns:
        The Note object with the specified ID belonging to the user.
    Raises:
        HTTPException: If user is not found, unauthorized to access notes, or note is not found.
    """
    user_dao = banco.UserDAO(db)
    user = user_dao.get_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        notes_dao = banco.NotesDAO(db)
        specific_note = notes_dao.get_note_by_id(note_id)
        if not specific_note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        return specific_note
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving note: {str(e)}")

@router.put("/users/{username}/notes/{note_id}", dependencies=[Depends(seguranca.get_current_user)])
async def update_note(username: str, note_id: int, description: str, db: Session = Depends(banco.get_db)):
    """ Updates a specific note for the user identified by username.
    Requires authentication of the requesting user.
    Args:
        username: Username of the user for whom to update the note.
        note_id: ID of the specific note to update.
        updated_note: Note object containing the updated description for the note.
    Returns:
        The updated Note object.
    Raises:
        HTTPException: If user is not found, unauthorized to access notes, or note is not found.
    """
    user_dao = banco.UserDAO(db)
    user = user_dao.get_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        notes_dao = banco.NotesDAO(db)
        existing_note = notes_dao.get_note_by_id(db, note_id)
        if not existing_note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

        updated_note = banco.update_note(db, note_id, user.id, description)

        return updated_note
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error updating note: {str(e)}")

@router.delete("/users/{username}/notes/{note_id}", dependencies=[Depends(seguranca.get_current_user)])
async def delete_note(username: str, note_id: int, db: Session = Depends(banco.get_db)):
    """ Deletes a specific note for the user identified by username.
    Requires authentication of the requesting user.
    Args:
        username: Username of the user for whom to delete the note.
        note_id: ID of the specific note to delete.
    Returns:
        A success message upon deletion.
    Raises:
        HTTPException: If user is not found, unauthorized to access notes, or note is not found.
    """
    user_dao = banco.UserDAO(db)
    user = user_dao.get_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        # Call the delete function from banco (assuming it exists)
        notes_dao = banco.NotesDAO(db)
        deleted = notes_dao.delete_note(db, note_id, user.id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

        return {"message": "Note deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting note: {str(e)}")