from django.template.response import TemplateResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser

from hubstars.serializers import BattleSerializers

def home (request):
  return TemplateResponse(request, 'home.html', {})
  
@api_view(['POST'])
@permission_classes((AllowAny,))
def battle (request):
  data = JSONParser().parse(request)
  serializer = BattleSerializers(data=data)
  
  if serializer.is_valid():
    return Response(serializer.battle_data(), status=200)
    
  return Response({'errors': serializer.errors}, status=400)
  