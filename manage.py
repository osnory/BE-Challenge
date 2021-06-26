from flask.cli import FlaskGroup

from revenue.api import app, db
from revenue.utils import loader

cli = FlaskGroup(create_app=lambda x: app)


@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    loader.load_data(db)
    print("DB Seeded")


if __name__ == "__main__":
    cli()
