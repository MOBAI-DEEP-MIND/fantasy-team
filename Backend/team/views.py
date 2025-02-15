from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Feature 1: Team Building with Budget Management

class ClubsView(APIView):
    serializer_class = ClubsSerializers
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def post(self,request):
        serializer = ClubsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class PlayersView(APIView):
    serializer_class = PlayersSerializers
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def post(self,request):
        serializer = PlayersSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)    
    

class ChooseTeamView(APIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            
            # Get the user's budget
            user_budget = request.user.budgets
            
            # Get the list of player IDs from the request data
            player_ids = request.data.get('players', [])

            # Check if exactly 11 players are selected
            if len(player_ids) != 11:
                return Response({'error': 'You must select exactly 11 players.'}, status=status.HTTP_400_BAD_REQUEST)

            # Count the number of players in each position
            positions = {'GK': 0, 'DF': 0, 'MF': 0, 'FW': 0}
            total_price = 0

            for player_id in player_ids:
                try:
                    player = Players.objects.get(id=player_id)
                    total_price += player.price  # Assuming 'price' is the field holding the player price
                    positions[player.position] += 1  # Assuming 'position' is a field in the Players model
                except Players.DoesNotExist:
                    return Response({'error': f'Player with ID {player_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate the formation
            valid_defenders = positions['DF'] in [4, 5]
            valid_midfielders = positions['MF'] in [3, 4]
            valid_forwards = positions['FW'] in [1, 2, 3]

            if not (positions['GK'] == 1 and valid_defenders and valid_midfielders and valid_forwards):
                return Response({'error': 'Invalid team formation. Ensure GK=1, DF=4 or 5, MF=3 or 4, FW=1, 2, or 3.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user's budget is sufficient
            if user_budget >= total_price:
                # Save the team if budget is sufficient
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': 'Insufficient budget to create team.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)