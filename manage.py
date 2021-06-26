from flask.cli import FlaskGroup

from revenue.api import app, db

cli = FlaskGroup(create_app=lambda x: app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    print("Seeding")
    #db.session.add(User(username="michael", email="michael@notreal.com"))
    #db.session.commit()


if __name__ == "__main__":
    cli()
