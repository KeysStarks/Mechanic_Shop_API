from application.extensions import ma
from application.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        
    password = ma.String(load_only=True)
    
class LoginSchema(ma.Schema):
    email = ma.String(required=True)
    password = ma.String(required=True)
        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()