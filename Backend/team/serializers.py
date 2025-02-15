from rest_framework.serializers import ModelSerializer
from core.models import Clubs,Players,Team


class ClubsSerializers(ModelSerializer):
    class Meta:
        model = Clubs
        fields = '__all__'

class PlayersSerializers(ModelSerializer):
    class Meta:
        model = Players
        fields = '__all__'   

class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'     