def deploy():
    from app import creation, db, Users
    from flask_migrate import upgrade, migrate, init, stamp

    app = creation()
    app.app_context().push()
    db.create_all()

    init()
    stamp()
    migrate()
    upgrade()

deploy()