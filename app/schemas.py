from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    user_id: int
    has_station: bool
    
    model_config = ConfigDict(from_attributes=True)

# UserStation schemas
class UserStationBase(BaseModel):
    location: str = Field(..., max_length=100)

class UserStationCreate(UserStationBase):
    user_id: int

class UserStation(UserStationBase):
    station_id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)

# StationData schemas
class StationDataBase(BaseModel):
    temperature: float = Field(..., ge=-40, le=80, description="Temperature must be between -40 and 80°C")
    pressure: float = Field(..., ge=300, le=1100, description="Pressure in hPa")
    humidity: float = Field(..., ge=0, le=100, description="Humidity must be between 0 and 100%")

class StationDataCreate(StationDataBase):
    station_id: int

class StationData(StationDataBase):
    id: int
    station_id: int
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    device_id: Optional[str] = None