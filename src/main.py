from typing import Dict

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.logging.logger import set_package_logger
from aws_lambda_powertools.utilities.typing import LambdaContext

set_package_logger()

logger = Logger()
metrics = Metrics()
tracer = Tracer()

app = APIGatewayHttpResolver()


@app.get('/hello_world')
@tracer.capture_method
def hello_world():
    logger.info('hello, world!')
    return 'hello, world!'


@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event: Dict, context: LambdaContext):
    return app.resolve(event, context)
