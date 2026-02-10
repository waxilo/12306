from flask import Blueprint
from models import SearchParams
from services import TicketService
from datetime import date

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/search', methods=['GET'])
def search() :
    params = SearchParams(train_date=date.today().isoformat(), from_station='WHN', to_station='IOQ')
    return TicketService.search_tickets(params)
