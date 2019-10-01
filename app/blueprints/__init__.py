from app.blueprints import oauth, deals

ACTIVE = [("/oauth", oauth.oauth), ("/deals", deals.deals)]
