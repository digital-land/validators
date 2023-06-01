class JsonResponse:
    def __init__(self, status=None, errors=None):
        self.status = status
        self.errors = errors or []

    def add_error(self, error):
        self.errors.append(error)

    def to_dict(self):
        response = {
            'status': self.status,
            'errors': [error for error in self.errors]
        }
        return response


class JsonError:
    def __init__(self, errorCode, errorMessage, scope, level, rowNumber=None, columnNames=None, url=None):
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.level = level
        self.rowNumber = rowNumber
        self.columnNames = columnNames
        self.scope = scope
        self.url = url

    def to_dict(self):
        response = {
            'scope': self.scope,
            'level': self.level,
            'errorCode': self.errorCode,
            'errorMessage': self.errorMessage,
            'url': self.url,
        }
        if self.scope == 'Field' or self.scope == 'Row':
            response['rowNumber'] = self.rowNumber
            response['columnNames'] = self.columnNames
        
        return response