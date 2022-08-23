import json

from exampleco.models.database import Session
from exampleco.models.database.orders import Order, OrderSchema
from exampleco.models.database.services import Service, ServiceSchema
from exampleco.models.database.order_items import OrderItem, OrderItemSchema
from utils import *


# pylint: disable=unused-argument
def get_all_orders(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all orders pulled from the database.
    """

    orders_schema = OrderSchema(many=True)
    orders = Session.query(Order).all()
    results = orders_schema.dump(orders)

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response

def get_order_details(event,context):
    """
        Funtion to fetch order details

        Args:
            event:
                pathParameters:id (int): Order id to fetch details for
        Returns:
            Returns a list of order items in a specific order
    """
    try:
        order_id = event['pathParameters']['id']

        orders_schema = OrderSchema()
        order = orders_schema.dump(Session.query(Order).get(order_id))

        if not order:
            return {"statusCode": 404, "body": json.dumps({'error': 'No such order found'})}

        if order.get('status') == 'DELETED':
            return {"statusCode": 403, "body": json.dumps({'error': 'Cannot fetch a deleted order'})}

        order_items_schema=OrderItemSchema(many=True)
        order_items=order_items_schema.dump(Session.query(OrderItem).filter(OrderItem.order_id== order_id).all())

        return {"statusCode": 200, "body": json.dumps(order_items)}

    except Exception:
        return {"statusCode": 500, "body": json.dumps({"error": 'Something went wrong'})}

def create_service(event,context):
    """
    Funtion to create a new service in the database

    Args:
        event:
            name (string): Name of the service to be created
            price (float): Price of the service
    Returns:
        Returns success or failure

    """
    try:
        body=json.loads(event["body"])

        service=Service(**body)

        # Commit the entry
        Session.add(service)
        Session.commit()

        return {"statusCode": 200, "body": json.dumps({"success":"Service created successfully",'service_id':service.id})}
    except AssertionError as err:
        return {"statusCode": 400, "body": json.dumps({"error":str(err)})}
    except Exception:
        return {"statusCode": 500, "body": json.dumps({"error": 'Something went wrong'})}

def _validate_services(validate_services):
    service_schema = ServiceSchema(many=True)
    services = Session.query(Service).all()
    results = service_schema.dump(services)

    valid_services = [service['id'] for service in results]
    invalid_services = [x for x in validate_services if x not in valid_services]

    return invalid_services

def create_order(event,context):
    """
    Funtion to create a new order in the database

    Args:
        event:
            services (list[int]): Id's of the services to be added
            description (description): Description of the order

    Returns:
        Returns success or failure
    """

    try:
        body = json.loads(event["body"])

        if 'services' not in body or len(body['services'])==0:
            raise ValueError('Services are not provided')


        invalid_services=_validate_services(body['services'])
        if len(invalid_services)>0:
            raise ValueError(f'Invalid Services: {str(invalid_services)}')

        order_params={x: body[x] for x in body if x not in 'services'}
        order = Order(**order_params)


        Session.add(order)
        # Flush the entry
        Session.flush()

        for service_id in body['services']:
            order_item=OrderItem(order_id=order.id,service_id=service_id)
            Session.add(order_item)

        # Commit the entry
        Session.commit()

        return {"statusCode": 200, "body": json.dumps({'success':'Order created successfully','order_id':order.id})}

    except ValueError as err:
        return {"statusCode": 400, "body": json.dumps({"error": str(err)})}
    except Exception:
        return {"statusCode": 500, "body": json.dumps({"error": 'Something went wrong'})}


def update_order(event,context):
    """
        Funtion to create a new order in the database

        Args:
            event:
                pathParameters:id (int): Order id to be updated
                services (list[int]): Id's of services to be added

        Returns:
            Returns success or failure
    """
    try:
        order_id=event['pathParameters']['id']
        body=json.loads(event["body"])

        orders_schema = OrderSchema()
        order = orders_schema.dump(Session.query(Order).get(order_id))

        if not order:
            return {"statusCode": 404, "body": json.dumps({'error': 'No such order found'})}

        if order.get('status')=='DELETED':
            return {"statusCode": 403, "body": json.dumps({'error': 'Cannot update a deleted order'})}

        invalid_services = _validate_services(body['services'])
        if len(invalid_services) > 0:
            raise ValueError(f'Invalid Services: {str(invalid_services)}')

        for service_id in body['services']:
            order_item=OrderItem(order_id=order_id,service_id=service_id)
            Session.add(order_item)

        # Commit the entry
        Session.commit()

        return {"statusCode": 200, "body": json.dumps({'success': 'Order updated successfully'})}

    except ValueError as err:
        return {"statusCode": 400, "body": json.dumps({"error": str(err)})}
    except Exception:
        return {"statusCode": 500, "body": json.dumps({"error": 'Something went wrong'})}

def delete_order(event,context):
    """
        Funtion to delete a order

        Args:
            event:
                pathParameters:id (int): Order id to be deleted

        Returns:
            Returns success or failure
    """
    try:
        order_id = event['pathParameters']['id']
        order = Session.query(Order).filter(Order.id== order_id).first()
        if not order:
            return {"statusCode": 404, "body": json.dumps({'error': 'No such order found'})}

        order.status="DELETED"
        Session.commit()

        return {"statusCode": 200, "body": json.dumps({'success': 'Order updated successfully'})}
    except Exception:
        return {"statusCode": 500, "body": json.dumps({"error": 'Something went wrong'})}


def get_orders_over_period(event,context):
    """
        Funtion to fetch order count over specific period

        Args:
            event:
                pathParameters:period (string): time period for order count

        Returns:
            Returns success or failure
    """

    try:
        time_period = event['pathParameters']['period']

        if time_period not in ORDER_TIME_PERIOD_RANGES:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid Time Period"})}

        if time_period=="THIS_WEEK":
            start_date,end_date=get_current_week_dates()
        elif time_period=="THIS_MONTH":
            start_date,end_date=get_current_month_dates()
        else:
            start_date,end_date=get_current_year_dates()

        orders=Session.query(Order).filter(Order.created_on >= start_date). \
            filter(Order.created_on <= end_date).all()

        return {"statusCode": 200, "body": json.dumps({"orders_count":len(orders)})}
    except Exception:
        return {"statusCode": 500, "body": json.dumps({"error": 'Something went wrong'})}


