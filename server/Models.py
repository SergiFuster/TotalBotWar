from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class game_states(db.Model):
    rowid       = db.Column(db.Integer, primary_key=True)
    ids         = db.Column(db.String(200))
    teams       = db.Column(db.String(200))
    healths     = db.Column(db.String(200))
    types       = db.Column(db.String(200))
    states      = db.Column(db.String(200))
    positions   = db.Column(db.String(400))
    directions  = db.Column(db.String(400))

    def __str__(self) -> str:
        return f"Tengo: {self.ids}"
    
    def serialize(self):
        return {
            "rowid"     : self.rowid,
            "ids"       : self.ids,
            "teams"     : self.teams,
            "healths"   : self.healths,
            "types"     : self.types,
            "states"    : self.states,
            "positions" : self.positions,
            "directions": self.directions
        }

