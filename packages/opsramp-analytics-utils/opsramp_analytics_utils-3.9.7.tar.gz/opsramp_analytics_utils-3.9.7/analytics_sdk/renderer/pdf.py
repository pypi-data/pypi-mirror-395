import logging
import time
import requests

from analytics_sdk.utilities import (
    API_TIME_STACKS,
)

logger = logging.getLogger(__name__)

class PDF:

    def __init__(self, analysis_run, url, report_path, file_time):
        self.analysis_run = analysis_run
        self.url = url
        self.report_path = report_path
        self.file_time = file_time

    def prepare_file_name(self, app_id, ext):
        return f'{app_id.lower()}-{self.analysis_run[:8]}-{self.file_time}.{ext}'

    def generate(self, data):
        logger.info(f'{self.analysis_run} -> processing the pdf request')
        api_proce_before_time = time.time()
        res = {}
        retry = 1
        while retry <= 3:
            try:
                resp = requests.post(self.url, data=data)
                if resp.status_code == 504:
                    logging.info(
                        f'{self.analysis_run} ::: got 504 error while pdf generation')
                    return resp.status_code
                elif not resp.ok:
                    logging.info(
                        f'{self.analysis_run} pdf generation failed.. retrying.. {retry} ')
                    time.sleep(retry * 2)
                    retry += 1
                    continue
                elif resp and resp is not None:
                    logging.info(
                        f'{self.analysis_run} pdf generated successfully.')
                    res = resp.json()
                    api_proce_after_time = time.time()
                    api_proce_diff = int(api_proce_after_time - api_proce_before_time)
                    if api_proce_diff > API_TIME_STACKS:
                        logging.info('%s , pdf response is took %d (greater than %d) seconds',
                                     self.analysis_run, api_proce_diff, API_TIME_STACKS)
                    if 'Key' in res:
                        logger.info('pdf response is: %s', res['Key'])
                        return res['Key']
                    else:
                        logging.info(
                            f'key not found, pdf generation failed, returning empty value for runid ::: {self.analysis_run}')
                        raise Exception(
                            f'key not found, pdf generation failed for run ::: {self.analysis_run}')
            except requests.exceptions.ConnectionError:
                time.sleep(retry * 2)
                retry += 1
                continue
            except Exception as e:
                raise Exception(
                    f'pdf generation failed for run ::: {self.analysis_run}, Exception is : {e}')

        logging.info(
            f'pdf generating failed after max tries, returning empty value for runid ::: {self.analysis_run}')
        raise Exception(
            f'process_pdf_request:: pdf generation failed after max tries, for run ::: {self.analysis_run}')
