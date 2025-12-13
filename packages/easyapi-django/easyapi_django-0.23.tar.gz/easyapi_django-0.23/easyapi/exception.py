import re

from django.http import JsonResponse


class HTTPException(Exception):

    def render(self, exception):

        (status, detail) = exception.args

        # match = re.search(r'\(\d+,\s*["\'](.+?)["\'](?=\))', detail)
        # if match:
        #     error_message = match.group(1)
        # else:
        #     error_message = 'Unknown error'

        return JsonResponse({'success': False, 'status': status, 'detail': detail}, status=status)
