from django.db import models

class Participante(models.Model):
    documento = models.CharField(max_length=32, blank=True) 
    siglaColeta = models.CharField(max_length=32, blank=True)  
    sequencial = models.CharField(max_length=32, blank=True)  
    siglaNome = models.CharField(max_length=32, blank=True)  
    nomeSocial = models.CharField(max_length=124, blank=True)  
    nome = models.CharField(max_length=124, blank=True)  
    nomeMae = models.CharField(max_length=124, blank=True)  
    dataNasc = models.CharField(max_length=64, blank=True)  
    sexo = models.CharField(max_length=64, blank=True) 
    genero = models.CharField(max_length=64, blank=True)  
    email = models.CharField(max_length=124, blank=True)  
    telefone = models.CharField(max_length=32, blank=True)
    agenteCadastro = models.CharField(max_length=124, blank=True)
    assinouTermo = models.CharField(max_length=32, blank=True) 
    
    paisNasc = models.CharField(max_length=64, blank=True)  
    estadoNasc = models.CharField(max_length=64, blank=True) 
    cidadeNasc = models.CharField(max_length=64, blank=True)
    
    pais = models.CharField(max_length=64, blank=True) 
    estado = models.CharField(max_length=64, blank=True) 
    cidade = models.CharField(max_length=64, blank=True)
    cep = models.CharField(max_length=32, blank=True) 
    rua = models.CharField(max_length=124, blank=True) 
    numero = models.CharField(max_length=32, blank=True) 
    complemento = models.CharField(max_length=64, blank=True)
    endereco = models.CharField(max_length=1024, blank=True)
    
    coletouEdta = models.CharField(max_length=32, blank=True)
    coletaEdtaData = models.CharField(max_length=64, blank=True)
    coletaEdtaAgente = models.CharField(max_length=124, blank=True)
    
    coletouSoro = models.CharField(max_length=32, blank=True)
    coletaSoroData = models.CharField(max_length=64, blank=True)
    coletaSoroAgente = models.CharField(max_length=124, blank=True)
    
    coletouPaxgene = models.CharField(max_length=32, blank=True)
    coletaPaxgeneData = models.CharField(max_length=64, blank=True)
    coletaPaxgeneAgente = models.CharField(max_length=124, blank=True)
    
    coletouFezes = models.CharField(max_length=32, blank=True)
    coletaFezesData = models.CharField(max_length=64, blank=True)
    coletaFezesAgente = models.CharField(max_length=124, blank=True)
    
    coletouSaliva = models.CharField(max_length=32, blank=True)
    coletaSalivaData = models.CharField(max_length=64, blank=True)
    coletaSalivaAgente = models.CharField(max_length=124, blank=True)
