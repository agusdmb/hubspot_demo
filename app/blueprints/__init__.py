from app.blueprints import deals, oauth, user

ACTIVE = [("/oauth", oauth.oauth), ("/deals", deals.deals), ("/user", user.user)]
