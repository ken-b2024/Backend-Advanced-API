from app.models import ServiceTicket
from app.extensions import ma
from marshmallow import fields


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested('MechanicSchema', many=True)
    customer = fields.Nested('CustomerSchema')
    mechanic_ids = fields.List(fields.Int(), required=False)
    customer_id = fields.Int(required=True)

    class Meta:
        model = ServiceTicket
        fields= ("id", "service_desc", "customer_id", "mechanic_ids", "mechanics", "customer")

class EditServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    service_desc = fields.String(required=False)

    class Meta:
        fields = ('add_mechanic_ids', 'remove_mechanic_ids', 'service_desc')

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_service_ticket_schema = ServiceTicketSchema(exclude=["customer_id"])
return_service_tickets_schema = ServiceTicketSchema(many=True, exclude=["customer_id"])
edit_service_ticket_schema = EditServiceTicketSchema()