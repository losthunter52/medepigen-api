from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from common.utils import check_required_fields
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from service.models import Participante


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_participantes(request):

    participantes = Participante.objects.all()
    participantes_data = []
    for participante in participantes:
        participante_data = {
            'id': participante.id,
            
            'documento': participante.documento,
            'siglaColeta': participante.siglaColeta,
            'sequencial': participante.sequencial,
            'siglaNome': participante.siglaNome,
            'nomeSocial': participante.nomeSocial,
            'nome': participante.nome,
            'nomeMae': participante.nomeMae,
            'dataNasc': participante.dataNasc,
            'sexo': participante.sexo,
            'genero': participante.genero,
            'email': participante.email,
            'telefone': participante.telefone,
            'agenteCadastro': participante.agenteCadastro,
            'assinouTermo': participante.assinouTermo,
            
            'paisNasc': participante.paisNasc,
            'estadoNasc': participante.estadoNasc,
            'cidadeNasc': participante.cidadeNasc,
            
            'pais': participante.pais,
            'estado': participante.estado,
            'cidade': participante.cidade,
            'cep': participante.cep,
            'rua': participante.rua,
            'numero': participante.numero,
            'complemento': participante.complemento,
            'endereco': participante.endereco,
            
            'coletouEdta': participante.coletouEdta,
            'coletaEdtaData': participante.coletaEdtaData,
            'coletaEdtaAgente': participante.coletaEdtaAgente,
            
            'coletouSoro': participante.coletouSoro,
            'coletaSoroData': participante.coletaSoroData,
            'coletaSoroAgente': participante.coletaSoroAgente,
            
            'coletouPaxgene': participante.coletouPaxgene,
            'coletaPaxgeneData': participante.coletaPaxgeneData,
            'coletaPaxgeneAgente': participante.coletaPaxgeneAgente,
            
            'coletouFezes': participante.coletouFezes,
            'coletaFezesData': participante.coletaFezesData,
            'coletaFezesAgente': participante.coletaFezesAgente,
            
            'coletouSaliva': participante.coletouSaliva,
            'coletaSalivaData': participante.coletaSalivaData,
            'coletaSalivaAgente': participante.coletaSalivaAgente,

        }
        participantes_data.append(participante_data)

    return Response(participantes_data, status=200)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_participante(request, id):

    try:
        participante = Participante.objects.get(id=id)
    except Participante.DoesNotExist:
        return Response({"error": "Participante not found."}, status=404)

    participante_data = {
        'id': participante.id,
        
        'documento': participante.documento,
        'siglaColeta': participante.siglaColeta,
        'sequencial': participante.sequencial,
        'siglaNome': participante.siglaNome,
        'nomeSocial': participante.nomeSocial,
        'nome': participante.nome,
        'nomeMae': participante.nomeMae,
        'dataNasc': participante.dataNasc,
        'sexo': participante.sexo,
        'genero': participante.genero,
        'email': participante.email,
        'telefone': participante.telefone,
        'agenteCadastro': participante.agenteCadastro,
        'assinouTermo': participante.assinouTermo,
        
        'paisNasc': participante.paisNasc,
        'estadoNasc': participante.estadoNasc,
        'cidadeNasc': participante.cidadeNasc,
        
        'pais': participante.pais,
        'estado': participante.estado,
        'cidade': participante.cidade,
        'cep': participante.cep,
        'rua': participante.rua,
        'numero': participante.numero,
        'complemento': participante.complemento,
        'endereco': participante.endereco,
        
        'coletouEdta': participante.coletouEdta,
        'coletaEdtaData': participante.coletaEdtaData,
        'coletaEdtaAgente': participante.coletaEdtaAgente,
        
        'coletouSoro': participante.coletouSoro,
        'coletaSoroData': participante.coletaSoroData,
        'coletaSoroAgente': participante.coletaSoroAgente,
        
        'coletouPaxgene': participante.coletouPaxgene,
        'coletaPaxgeneData': participante.coletaPaxgeneData,
        'coletaPaxgeneAgente': participante.coletaPaxgeneAgente,
        
        'coletouFezes': participante.coletouFezes,
        'coletaFezesData': participante.coletaFezesData,
        'coletaFezesAgente': participante.coletaFezesAgente,
        
        'coletouSaliva': participante.coletouSaliva,
        'coletaSalivaData': participante.coletaSalivaData,
        'coletaSalivaAgente': participante.coletaSalivaAgente,
    }

    return Response(participante_data, status=200)


@api_view(['POST'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_participante(request):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    required_fields = [
        'documento', 
        'siglaColeta', 
        'sequencial', 
        'siglaNome', 
        'nome', 
        'nomeMae', 
        'dataNasc',
        'sexo', 
        'email', 
        'telefone',
        'agenteCadastro',
        'assinouTermo',
         
        'paisNasc', 
        'estadoNasc', 
        'cidadeNasc',
         
        'pais'
    ]

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    participante = Participante.objects.create(
        documento=data.get('documento'),
        siglaColeta=data.get('siglaColeta'),
        sequencial=data.get('sequencial'),
        siglaNome=data.get('siglaNome'),
        nomeSocial=data.get('nomeSocial'),
        nome=data.get('nome'),
        nomeMae=data.get('nomeMae'),
        dataNasc=data.get('dataNasc'),
        sexo=data.get('sexo'),
        email=data.get('email'),
        telefone=data.get('telefone'),
        agenteCadastro=data.get('agenteCadastro'),
        assinouTermo=data.get('assinouTermo'),
        
        paisNasc=data.get('paisNasc'),
        estadoNasc=data.get('estadoNasc'),
        cidadeNasc=data.get('cidadeNasc'),
        
        pais=data.get('pais')
    )

    participante.genero = data.get('genero', None)

    participante.estado = data.get('estado', None)
    participante.cidade = data.get('cidade', None)
    participante.cep = data.get('cep', None)
    participante.rua = data.get('rua', None)
    participante.numero = data.get('numero', None)
    participante.complemento = data.get('complemento', None)
    participante.endereco = data.get('endereco', None)
    
    participante.coletouEdta = data.get('coletouEdta', None)
    participante.coletaEdtaData = data.get('coletaEdtaData', None)
    participante.coletaEdtaAgente = data.get('coletaEdtaAgente', None)
    
    participante.coletouSoro = data.get('coletouSoro', None)
    participante.coletaSoroData = data.get('coletaSoroData', None)
    participante.coletaSoroAgente = data.get('coletaSoroAgente', None)
    
    participante.coletouPaxgene = data.get('coletouPaxgene', None)
    participante.coletaPaxgeneData = data.get('coletaPaxgeneData', None)
    participante.coletaPaxgeneAgente = data.get('coletaPaxgeneAgente', None)
    
    participante.coletouFezes = data.get('coletouFezes', None)
    participante.coletaFezesData = data.get('coletaFezesData', None)
    participante.coletaFezesAgente = data.get('coletaFezesAgente', None)
    
    participante.coletouSaliva = data.get('coletouSaliva', None)
    participante.coletaSalivaData = data.get('coletaSalivaData', None)
    participante.coletaSalivaAgente = data.get('coletaSalivaAgente', None)

    participante.save()

    return Response({"message": "Participante creation success."}, status=201)


@api_view(['PUT'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_participante(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    try:
        participante = Participante.objects.get(id=id)
    except Participante.DoesNotExist:
        return Response({"error": "Participante not found."}, status=404)

    required_fields = [
        'documento', 
        'siglaColeta', 
        'sequencial', 
        'siglaNome', 
        'nome', 
        'nomeMae', 
        'dataNasc',
        'sexo', 
        'email', 
        'telefone',
        'agenteCadastro',
        'assinouTermo',
         
        'paisNasc', 
        'estadoNasc', 
        'cidadeNasc',
         
        'pais'
    ]

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    participante.documento = data.get('documento', None)
    participante.siglaColeta = data.get('siglaColeta', None)
    participante.sequencial = data.get('sequencial', None)
    participante.siglaNome = data.get('siglaNome', None)
    participante.nomeSocial = data.get('nomeSocial', None)
    participante.nome = data.get('nome', None)
    participante.nomeMae = data.get('nomeMae', None)
    participante.dataNasc = data.get('dataNasc', None)
    participante.sexo = data.get('sexo', None)
    participante.genero = data.get('genero', None)
    participante.email = data.get('email', None)
    participante.telefone = data.get('telefone', None)
    participante.agenteCadastro = data.get('agenteCadastro', None)
    participante.assinouTermo = data.get('assinouTermo', None)
    
    participante.paisNasc = data.get('paisNasc', None)
    participante.estadoNasc = data.get('estadoNasc', None)
    participante.cidadeNasc = data.get('cidadeNasc', None)
    
    participante.pais = data.get('pais', None)
    participante.estado = data.get('estado', None)
    participante.cidade = data.get('cidade', None)
    participante.cep = data.get('cep', None)
    participante.rua = data.get('rua', None)
    participante.numero = data.get('numero', None)
    participante.complemento = data.get('complemento', None)
    participante.endereco = data.get('endereco', None)
    
    participante.coletouEdta = data.get('coletouEdta', None)
    participante.coletaEdtaData = data.get('coletaEdtaData', None)
    participante.coletaEdtaAgente = data.get('coletaEdtaAgente', None)
    
    participante.coletouSoro = data.get('coletouSoro', None)
    participante.coletaSoroData = data.get('coletaSoroData', None)
    participante.coletaSoroAgente = data.get('coletaSoroAgente', None)
    
    participante.coletouPaxgene = data.get('coletouPaxgene', None)
    participante.coletaPaxgeneData = data.get('coletaPaxgeneData', None)
    participante.coletaPaxgeneAgente = data.get('coletaPaxgeneAgente', None)
    
    participante.coletouFezes = data.get('coletouFezes', None)
    participante.coletaFezesData = data.get('coletaFezesData', None)
    participante.coletaFezesAgente = data.get('coletaFezesAgente', None)
    
    participante.coletouSaliva = data.get('coletouSaliva', None)
    participante.coletaSalivaData = data.get('coletaSalivaData', None)
    participante.coletaSalivaAgente = data.get('coletaSalivaAgente', None)

    participante.save()

    return Response({"message": "Participante updated successfully."}, status=200)


@api_view(['DELETE'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_participante(request, id):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    try:
        participante = Participante.objects.get(id=id)
    except Participante.DoesNotExist:
        return Response({"error": "Participante not found."}, status=404)

    participante.delete()
    return Response({"message": "Participante deleted successfully."}, status=200)
