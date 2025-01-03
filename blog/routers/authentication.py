from .. import schemas, database, models, token
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request:schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credential")
    if not Hash.verify(user.password, request.paswword):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub":user.email}
    )
    return {"access_token":access_token,"token_type":"bearer"}