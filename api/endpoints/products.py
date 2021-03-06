from flask import Blueprint, request
from sqlalchemy import Table, MetaData
from sqlalchemy.sql import select
import datetime
from utility import Response, checkVars, authenticateRequest, mimsDbEng, checkPrice

# Business function imports
from .businesses.target import targetGetProducts, targetGetProduct, targetEditProduct, targetGetProductMovement, targetGetProductForecast

# ===============================================
# Product endpoints
# ===============================================

productsBlueprint = Blueprint('products', __name__)

# Endpoint to get products
# GET /products/
# Auth: Access token required, can be employee or manager
# Returns: A list of products
@productsBlueprint.route('/', methods=['GET'])
def getProducts():
    response = Response()

    # Ensure user has permission for this endpoint
    userId = authenticateRequest(response, request)
    if response.hasError(): return response.getJson()

    # Ensure required input parameters are received
    required = []
    optional = ['name', 'item_code', 'plu', 'barcode', 'department', 'search_term', 'page_size', 'page']
    data = checkVars(response, request.values.to_dict(), required, optional)
    if response.hasError(): return response.getJson()

    # Setup database connection and table
    con = mimsDbEng.connect()
    users = Table('users', MetaData(mimsDbEng), autoload=True)

    # Get the business reference of the business of the user making this request
    stm = select([users]).where(users.c.id == userId)
    businessId = con.execute(stm).fetchone()['business']

    # Call the relevant get products function depending on business to get response data
    if businessId == 1:
        response.data['products'] = targetGetProducts(data)
    
    return response.getJson()

# Endpoint to get a specific product
# GET /products/{item_code}/
# Auth: Access token required, can be employee or manager
# Returns: A single product
@productsBlueprint.route('/<itemCode>/', methods=['GET'])
def getProduct(itemCode):
    response = Response()

    # Ensure user has permission for this endpoint
    userId = authenticateRequest(response, request)
    if response.hasError(): return response.getJson()

    # Ensure required input parameters are received
    required = []
    optional = []
    data = checkVars(response, request.values.to_dict(), required, optional)
    if response.hasError(): return response.getJson()

    # Setup database connection and table
    con = mimsDbEng.connect()
    users = Table('users', MetaData(mimsDbEng), autoload=True)

    # Get the business reference of the business of the user making this request
    stm = select([users]).where(users.c.id == userId)
    businessId = con.execute(stm).fetchone()['business']

    # Call the relevant get products function depending on business to get response data
    if businessId == 1:
        product = targetGetProduct(itemCode)

    if product:    
        response.data['product'] = product
    else:
        return response.setError(18)
    
    return response.getJson()

# Endpoint to edit a product
# PUT /products/{item_code}/
# Auth: Access token required, can be employee or manager
# Returns: The id of the updated product
@productsBlueprint.route('/<itemCode>/', methods=['PUT'])
def editProduct(itemCode):
    response = Response()

    # Ensure user has permission for this endpoint
    userId = authenticateRequest(response, request)
    if response.hasError(): return response.getJson()

    # Ensure required input parameters are received
    required = []
    optional = ['price']
    data = checkVars(response, request.get_json(), required, optional, atLeastOneOptional=True)
    if response.hasError(): return response.getJson()

    if 'price' in data and not checkPrice(response, data['price']):
        return response.getJson()

    # Setup database connection and table
    con = mimsDbEng.connect()
    users = Table('users', MetaData(mimsDbEng), autoload=True)

    # Get the business reference of the business of the user making this request
    stm = select([users]).where(users.c.id == userId)
    businessId = con.execute(stm).fetchone()['business']

    # Call the relevant get products function depending on business to get response data
    if businessId == 1:
        product = targetGetProduct(itemCode)
        if not product: return response.setError(18)
        response.data['item_code'] = targetEditProduct(itemCode, data)
    
    return response.getJson()

# Endpoint to get a specific product's movement
# GET /products/{item_code}/movement/
# Auth: Access token required, can be employee or manager
# Returns: The product's movement
@productsBlueprint.route('/<itemCode>/movement/', methods=['GET'])
def getProductMovement(itemCode):
    response = Response()

    # Ensure user has permission for this endpoint
    userId = authenticateRequest(response, request)
    if response.hasError(): return response.getJson()

    # Ensure required input parameters are received
    required = []
    optional = []
    data = checkVars(response, request.values.to_dict(), required, optional)
    if response.hasError(): return response.getJson()

    startDate = datetime.datetime.combine(datetime.date.today(), datetime.time()) - datetime.timedelta(days=7)

    # Setup database connection and table
    con = mimsDbEng.connect()
    users = Table('users', MetaData(mimsDbEng), autoload=True)

    # Get the business reference of the business of the user making this request
    stm = select([users]).where(users.c.id == userId)
    businessId = con.execute(stm).fetchone()['business']

    # Call the relevant get products function depending on business to get response data
    if businessId == 1:
        product = targetGetProduct(itemCode)
        if not product: return response.setError(18)
        response.data['product_movement'] = targetGetProductMovement(itemCode, startDate.date())
    
    return response.getJson()

# Endpoint to get a specific product's forecasted inventory transactions
# GET /products/{item_code}/forecast/
# Auth: Access token required, can be employee or manager
# Returns: The product's forecasted inventory transactions
@productsBlueprint.route('/<itemCode>/forecast/', methods=['GET'])
def getProductForecast(itemCode):
    response = Response()

    # Ensure user has permission for this endpoint
    userId = authenticateRequest(response, request)
    if response.hasError(): return response.getJson()

    # Ensure required input parameters are received
    required = []
    optional = []
    data = checkVars(response, request.values.to_dict(), required, optional)
    if response.hasError(): return response.getJson()

    # Setup database connection and table
    con = mimsDbEng.connect()
    users = Table('users', MetaData(mimsDbEng), autoload=True)

    # Get the business reference of the business of the user making this request
    stm = select([users]).where(users.c.id == userId)
    businessId = con.execute(stm).fetchone()['business']

    # Call the relevant get products function depending on business to get response data
    if businessId == 1:
        product = targetGetProduct(itemCode)
        if not product: return response.setError(18)
        response.data['product_forecast'] = targetGetProductForecast(itemCode)
    
    return response.getJson()