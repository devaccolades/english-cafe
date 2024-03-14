from rest_framework import serializers

from general.models import Blog, Tags


class ListBlogSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = (
            'id',
            'title',
            'sub_title',
            'description',
            'thumbnail',
            'image',
            'author',
            'slug',
            'created_at',
            'tags',
        )

    
    def get_created_at(self, instance):
        if instance.created_at:
            instance_date = instance.created_at
            
            day_number = instance_date.day
            month_name = instance_date.strftime("%B")
            year_number = instance_date.year

            date = f'{day_number} {month_name} {year_number}'

            return date
        else:
            return None
        
    def get_tags(self, instance):
        request = self.context['request']
        if instance.tags:
            tag_instance = instance.tags.all()
            serialized_data = ListTagsSerializer(
                tag_instance,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return []
        

class ListTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = (
            'id',
            'name'
        )
        


        
        