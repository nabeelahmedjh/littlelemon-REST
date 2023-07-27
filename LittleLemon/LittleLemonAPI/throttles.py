from rest_framework.throttling import BaseThrottle, UserRateThrottle




class GroupSpecificThrottle(BaseThrottle):

    def allow_request(self, request, view):
        
        if request.user.groups.filter(name='delivery_crew').exists():
            self.rate = '2/min'
        
        elif request.user.groups.filter(name='Manager').exists():
            self.rate = '4/min'
        
        else:
            self.rate = '10/min'

        return UserRateThrottle().allow_request(request, view)