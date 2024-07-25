from rating.models import tblitemRatings, tblRatings
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.rating import tblitemRatingsSerializer, tblRatingSerializer
from django.db import transaction
from order.models import Order
from django.db.models import Q
from rating.mail import create_profile_for_email


class RatingCreateAPIView(APIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        table_no = data['table_no']
        order = Order.objects.filter(Q(table_no=table_no) & (Q(state='Pending') | Q(state='Cooked')|Q(state='Accepted'))).first()
        if order:
            data['order'] = order.id
        else:
            return Response({"detail":"No order created first"}, 400)

        if tblRatings.objects.filter(order=order).exists():
            return Response({"detail": "Review already exists for this order"}, 400)
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
        try:
            create_profile_for_email(tblRating)
        except Exception as e:
            print(e)
        return Response(tblRatingsserializer.data, 201)

            

