from rating.models import tblitemRatings, tblRatings
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.rating import tblitemRatingsSerializer, tblRatingSerializer
from django.db import transaction


class RatingCreateAPIView(APIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data

        tblitemRatings = data.pop('tblitemRatings', [])
        tblRatingsserializer = tblRatingSerializer(data=data)
        if tblRatingsserializer.is_valid():
            tblRating = tblRatingsserializer.save()
        else: 
            return Response("tblRating data is not valid", 400)
        
        for item in tblitemRatings:
            item['tblrating'] = tblRating.id
        tblitemRatingSerializer = tblitemRatingsSerializer(data=tblitemRatings, many=True)
        if tblitemRatingSerializer.is_valid():
            tblitemRatingSerializer.save()
        else:
            return Response("tblitemRatings data is not valid", 400)

        return Response(tblRatingsserializer.data, 201)

            

