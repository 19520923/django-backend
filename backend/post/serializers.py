from turtle import pos
from rest_framework import serializers
from .models import Photo, Post, PostComment, Reaction
from food.models import Food


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['pk', 'url']
        
class SubPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['pk', 'author', 'content', 'create_at', 'childrent']
    
class PostCommentSerializer(serializers.ModelSerializer):
    childrent = SubPostCommentSerializer(many = True, required= False)
    
    class Meta:
        model = PostComment
        fields = "__all__"
        extra_kwargs = {'author' : {'required': False},
                        'parent': {'required': False}}
        
    
class PostSerializer(serializers.ModelSerializer):
    foods = serializers.PrimaryKeyRelatedField(many = True, queryset = Food.objects.all())
    photos = PhotoSerializer(many = True, required = False)
    
    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {'author' : {'required': False}}
  
    def create(self, validated_data):
        photos = validated_data.pop('photos')
        foods = validated_data.pop('foods')
        post_obj = Post.objects.create(**validated_data)
        for photo in photos:
            photo_obj=Photo.objects.get_or_create(url = photo['url'], post = post_obj)
        for food in foods:
            food_obj = Food.objects.get(id = food.id)
            post_obj.foods.add(food_obj)
        return post_obj
    
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['pk', 'author', 'create_at']
        extra_kwargs = {'author' : {'required': False}}