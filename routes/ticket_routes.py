from flask import Blueprint
from models import SearchParams
from services import TicketService, LoginService, UserService
from datetime import date

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/search', methods=['GET'])
def search() :
    params = SearchParams(train_date=date.today().isoformat(), from_station='WHN', to_station='IOQ')
    return TicketService.search_tickets(params)


@ticket_bp.route('/qr_login', methods=['GET'])
def qr_login() :
    return {'message': LoginService.qr_login()}

@ticket_bp.route('/user_info', methods=['GET'])
def user_info() :
    return UserService.user_info()
