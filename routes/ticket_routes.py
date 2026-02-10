from flask import Blueprint
from models.search_params import SearchParams
from services.ticket_service import TicketService

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/search', methods=['GET'])
def search() :
    params = SearchParams(train_date='2026-02-15',from_station='BJP',to_station='SHH')
    return TicketService.search_tickets(params)
