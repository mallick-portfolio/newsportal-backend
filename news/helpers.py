from functools import wraps
from rest_framework.response import Response



def admin_only(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        print(request)

        if request.user.status == 'admin':
             return function(request, *args, **kwargs)
        else:
            return Response({
                "success": False,
                "message": "Authentication access!!!",
                "error": True
            })

  return wrap