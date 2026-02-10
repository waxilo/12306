from flask import Blueprint
from services.ticket_service import TicketService

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/search', methods=['GET'])
def search() :
    return TicketService.search_tickets()
