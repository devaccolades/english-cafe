from rest_framework import serializers

from general.models import Blog


class ListBlogSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = (
            'id',
            'title',
            'descriprtion',
            'thumbnail',
            'image',
            'tags',
            'author',
            'meta_description',
            'slug',
            'created_at'
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
        


        
        