from rest_framework import serializers #type:ignore
from .models import Lista,Resultado, Previsao

class ListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lista
        fields = '__all__'
        
        
class ResultadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = '__all__'

class PrevisaoSrializer(serializers.ModelSerializer):
    class Meta:
        model = Previsao
        fields = '__all__'
        
class ListaInputSerializer(serializers.Serializer):
    listas = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField()
        )
    )

    def validate_listas(self, value):
        if not value:
            raise serializers.ValidationError("Envie ao menos uma lista.")

        for idx, lista in enumerate(value):
            if not isinstance(lista, list) or len(lista) == 0:
                raise serializers.ValidationError(f"Lista #{idx+1} vazia ou inválida.")

            # Aceita duplicados (origem externa), mas limita tamanho para evitar payloads enormes.
            if len(lista) > 200:
                raise serializers.ValidationError(f"Lista #{idx+1} muito grande (máximo 200 números).")

            for n in lista:
                # IntegerField já converte, mas garantimos faixa.
                if n < 0 or n > 99:
                    raise serializers.ValidationError(
                        f"Número fora do intervalo 0-99 na lista #{idx+1}: {n}"
                    )

        return value


class ValidarPrevisaoSerializer(serializers.Serializer):
    numeros = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=99),
        allow_empty=False,
        max_length=200,
    )