from belief import Belief
from API import TopicExtractor

def dividir_y_guardar_textos(archivo_entrada):
    """Divide un archivo de texto en partes individuales y las guarda como archivos independientes.

    Args:
        archivo_entrada: La ruta del archivo de texto de entrada.
    """
    result = []
    with open(archivo_entrada, 'r') as archivo_lectura:
        texto_completo = archivo_lectura.read()

    topicE = TopicExtractor()
    for texto_parte in texto_completo.split('\n'):
        print("Text: ",texto_parte)
        print("Topics: ")
        
        msg = topicE.extract_topics(texto_parte)
        initial_beliefs = [Belief(topic[0],topic[1]) for topic in msg]
        if len(initial_beliefs) == 0:
            continue
        result.append((texto_parte,initial_beliefs))
        
    return result
