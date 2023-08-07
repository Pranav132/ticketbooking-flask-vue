from app import create_app, db, models

app = create_app()

with app.app_context():
    db.create_all()
    admin = models.User(username='admin', email='admin@example.com', is_admin=True)
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
