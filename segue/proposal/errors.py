from segue.errors import SegueError

class DeadlineReached(SegueError):
    code = 400
    def to_json(self):
        return { 'message': 'Proposals are no longer accepted after deadline has been reached' }

