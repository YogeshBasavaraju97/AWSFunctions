
# 1. Write an AWS Lambda function that adds two numbers and returns the result.

def lambda_handler(event, context):
    """
    AWS Lambda function that adds two numbers from the event payload
    
    Parameters:
        event (dict): Must contain 'num1' and 'num2' as numbers
        context: AWS Lambda context object
        
    Returns:
        dict: Contains the sum and status code
    """
    try:
        # Extract numbers from event
        num1 = float(event['num1'])
        num2 = float(event['num2'])
        
        # Calculate sum
        result = num1 + num2
        
        # Return success response
        return {
            'statusCode': 200,
            'body': {
                'result': result,
                'message': f'Successfully added {num1} and {num2}'
            }
        }
    except KeyError:
        # Return error if required parameters are missing
        return {
            'statusCode': 400,
            'body': {
                'error': 'Missing required parameters. Please provide num1 and num2.'
            }
        }
    except ValueError:
        # Return error if parameters cannot be converted to numbers
        return {
            'statusCode': 400,
            'body': {
                'error': 'Invalid parameters. num1 and num2 must be numbers.'
            }
        }