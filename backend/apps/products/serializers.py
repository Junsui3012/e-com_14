from rest_framework import serializers
from .models import Product, ProductImage, Review, Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'image', 'children']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        if children.exists():
            return CategorySerializer(children, many=True).data
        return []
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order', 'alt_text', 'is_primary']

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_email', 'user_name', 'rating', 'title', 'body', 'created_at']
        read_only_fields = ['id', 'user_name', 'user_email', 'created_at']

class ProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        models = Product
        fields = ['id', 'name', 'slug', 'price', 'compare_at_price', 'category_name', 'primary_image', 'is_in_stock', 'discount_percentage']
    
    def get_primary_image(self, obj):
        image = obj.images.filter(is_primary=True).first()
        if image:
            request = self.context.get('request')

            if request:
                return request.build_absolute_url(image.image.url)
        return None
    
class ProductDetailSerializer(serializers.ModelSerializer):
    images   = ProductImageSerializer(many=True, read_only=True)
    reviews  = ReviewSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'compare_at_price',
            'sku', 'stock', 'is_active', 'is_featured', 'category',
            'images', 'reviews', 'is_in_stock', 'discount_percentage',
            'avg_rating', 'review_count', 'created_at'
        ]

    def get_avg_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            return round(total / reviews.count(), 1)
        return None

    def get_review_count(self, obj):
        return obj.reviews.count()
    
