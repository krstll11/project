from fastapi import FastAPI, Depends
from database import get_db
import models
from routers import ads, auth,category,user,role,response,favorite,make_admin

app = FastAPI()


app.include_router(auth)
app.include_router(ads)
app.include_router(category)
app.include_router(user)
app.include_router(role)
app.include_router(response)
app.include_router(favorite)
app.include_router(make_admin)
