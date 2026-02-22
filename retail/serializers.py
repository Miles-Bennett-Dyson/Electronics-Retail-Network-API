from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from retail.models import Retail, Product


class RetailSerializer(serializers.ModelSerializer):
    level = SerializerMethodField()

    def get_level(self, obj):
        if not obj.get_level():
            return 0
        else:
            return obj.get_level()

    def validate(self, attrs):
        """ Метод дополнительно выполняет проверку на циклическую иерархию. Чтобы текущий объект не мог
         указать самого себя поставщиком. """

        if self.instance:
            supplier = attrs.get("supplier")
            if supplier:
                if supplier.pk == self.instance.pk:
                    raise ValidationError('Нельзя себя указывать поставщиком')
                list_suppliers = []
                current_node = supplier
                while current_node:
                    if current_node.pk in list_suppliers or current_node.pk == self.instance.pk:
                        raise ValidationError('Циклическая иерархия')
                    list_suppliers.append(current_node.pk)
                    current_node = current_node.supplier
        return super().validate(attrs)

    class Meta:
        model = Retail
        read_only_fields = ["debt", ]
        fields = "__all__"
        extra_kwargs = {
            'products': {'required': False},
        }


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
