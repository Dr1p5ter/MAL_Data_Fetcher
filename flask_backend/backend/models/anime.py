# native imports

from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSONB

# local imports

from .base import BaseModel, db

from MAL_api.MAL_classes import (
    AnimeDetails, AnimeDetailsGetAttributeError, HTTPError,
    InvalidAnimeDetailsAnimeIdError
)
from MAL_api.constants import ANIMEDETAILSNODE_ATTRIBUTES

class Anime(BaseModel):
    """
    (class object)

    A model for keeping track of anime data.
    """
    __tablename__ : str = 'anime'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column(
        db.Text, 
        nullable=False
    )
    main_picture = db.Column(
        JSONB,
        nullable=True
    )
    alternative_titles = db.Column(
        JSONB, 
        nullable=True
    )
    start_date = db.Column(
        db.DateTime,
        nullable=True
    )
    end_date = db.Column(
        db.DateTime,
        nullable=True
    )
    synopsis = db.Column(
        db.Text,
        nullable=True
    )
    mean = db.Column(
        db.Float,
        nullable=True
    )
    rank = db.Column(
        db.Integer,
        nullable=True
    )
    popularity = db.Column(
        db.Integer,
        nullable=True
    )
    num_list_users = db.Column(
        db.Integer, 
        nullable=True
    )
    num_scoring_users = db.Column(
        db.Integer,
        nullable=True
    )
    nsfw = db.Column(
        db.Text,
        nullable=True
    )
    genres = db.Column(
        JSONB,
        nullable=True
    )
    created_at = db.Column(
        db.DateTime,
        nullable=True
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=True
    )
    media_type = db.Column(
        db.Text,
        nullable=True
    )
    status = db.Column(
        db.Text,
        nullable=True
    )
    num_episodes = db.Column(
        db.Integer,
        nullable=True
    )
    start_season = db.Column(
        JSONB,
        nullable=True
    )
    broadcast = db.Column(
        JSONB,
        nullable=True
    )
    source = db.Column(
        db.Text,
        nullable=True
    )
    average_episode_duration = db.Column(
        db.Integer,
        nullable=True
    )
    rating = db.Column(
        db.Text,
        nullable=True
    )
    studios = db.Column(
        JSONB,
        nullable=True
    )
    pictures = db.Column(
        JSONB,
        nullable=True
    )
    background = db.Column(
        db.Text,
        nullable=True
    )
    related_anime = db.Column(
        JSONB,
        nullable=True
    )
    related_manga = db.Column(
        JSONB,
        nullable=True
    )
    recommendations = db.Column(
        JSONB,
        nullable=True
    )
    statistics = db.Column(
        JSONB,
        nullable=True
    )
    last_refreshed = db.Column(
        db.DateTime(), 
        default=datetime.now(timezone.utc),
        nullable=False,
        onupdate=datetime.now(timezone.utc)
    )

    def __init__(self, id : int, attrs : list = []) :
        # make a call to the MAL API to get the anime details
        try :
            anime_data = AnimeDetails(id, attrs)
        except InvalidAnimeDetailsAnimeIdError :
            raise Exception(f'Invalid Id: {id}')
        except HTTPError :
            raise Exception(f'HTTP Error for Id: {id}')
        
        # set the attributes of the Anime object
        try :
            for attr, val in anime_data.get_attribute_dict().values() :
                self.__setattr__(attr, val)
        except AnimeDetailsGetAttributeError :
            raise Exception(f'Error getting attribute for Id: {id}')
        
    def __repr__(self):
        return f'<Anime {self.title}>'
