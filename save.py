from belief import Belief
from API import TopicExtractor

def dividir_y_guardar_texto(archivo_entrada):
    """Divide un archivo de texto en partes individuales y las guarda como archivos independientes.

    Args:
        archivo_entrada: La ruta del archivo de texto de entrada.
    """
    with open(archivo_entrada, 'r') as archivo_lectura:
        texto_completo = archivo_lectura.read()

    topicE = TopicExtractor()
    
    print("Text: ",texto_completo)
    print("Topics: ")
    
    msg = topicE.extract_topics(texto_completo)
    print(msg)
    
    initial_beliefs = [Belief(topic[0],topic[1]) for topic in msg]
    return (texto_completo,initial_beliefs)
        
