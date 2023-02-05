from rest_framework import serializers

from catalog.models import Cover, Music, MusicText, Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class CoverSerializer(serializers.ModelSerializer):
    offer = OfferSerializer(read_only=True)

    class Meta:
        model = Cover
        fields = "__all__"


class MusicSerializer(serializers.ModelSerializer):
    offer = OfferSerializer(read_only=True)

    class Meta:
        model = Music
        fields = "__all__"


class MusicTextSerializer(serializers.ModelSerializer):
    offer = OfferSerializer(read_only=True)

    class Meta:
        model = MusicText
        fields = "__all__"
