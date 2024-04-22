import google.generativeai as genai
import os

class TopicExtractor:

    def __init__(self):
        """Inicializa la clase y configura la API de Gemini"""
        os.environ['API_KEY'] = 'AIzaSyB86IMkIMmwAuXJ5sWq7bymyPAW9Ommn8c'  # Reemplaza con tu clave de API
        genai.configure(api_key=os.environ['API_KEY'])
        
        # Configuración del modelo
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        self.model = genai.GenerativeModel(
            model_name="gemini-pro", 
            generation_config=generation_config, 
            safety_settings=safety_settings
        )

    def extract_topics(self, prompt):
        if prompt == "":
            return []
        """Extrae los temas y sus opiniones de una prompt"""
        # Prompt para el modelo
        prompt_parts = [
            # Instrucciones para el modelo (se incluyen los posibles temas)
            "Your job is to extract the topics of a message based on the following possible topics: \n\n\n    HEALTH_AND_WELLNESS = \"Health and wellness\"\n    TECHNOLOGY_AND_SOCIETY = \"Technology and society\"\n    EDUCATION_AND_LEARNING = \"Education and learning\"\n    ENVIRONMENT_AND_SUSTAINABILITY = \"Environment and sustainability\"\n    CULTURE_AND_TRADITIONS = \"Culture and traditions\"\n    ECONOMY_AND_FINANCE = \"Economy and finance\"\n    POLITICS_AND_GOVERNMENT = \"Politics and government\"\n    SCIENCE_AND_DISCOVERIES = \"Science and discoveries\"\n    ART_AND_CREATIVITY = \"Art and creativity\"\n    WORK_AND_CAREER = \"Work and career\"\n    LEISURE_AND_ENTERTAINMENT = \"Leisure and entertainment\"\n    TRAVEL_AND_TOURISM = \"Travel and tourism\"\n    FOOD_AND_NUTRITION = \"Food and nutrition\"\n    SPORTS_AND_PHYSICAL_ACTIVITY = \"Sports and physical activity\"\n    RELIGION_AND_SPIRITUALITY = \"Religion and spirituality\"\n    FASHION_AND_STYLE = \"Fashion and style\"\n    HISTORY_AND_HERITAGE = \"History and heritage\"\n    TECHNOLOGY_AND_GADGETS = \"Technology and gadgets\"\n    TRANSPORTATION_AND_MOBILITY = \"Transportation and mobility\"\n    JUSTICE_AND_HUMAN_RIGHTS = \"Justice and human rights\"\n    INNOVATION_AND_ENTREPRENEURSHIP = \"Innovation and entrepreneurship\"\n    COMMUNICATION_AND_MEDIA = \"Communication and media\"\n    COMMUNITY_AND_SOCIETY = \"Community and society\"\n    BEAUTY_AND_PERSONAL_CARE = \"Beauty and personal care\"\n    HOME_AND_DOMESTIC_LIFE = \"Home and domestic life\"\n    MONEY_AND_PERSONAL_FINANCE = \"Money and personal finance\"\n    SECURITY_AND_PROTECTION = \"Security and protection\"\n    CREATIVITY_AND_ARTISTIC_EXPRESSION = \"Creativity and artistic expression\"\n    LEARNING_AND_PERSONAL_DEVELOPMENT = \"Learning and personal development\"\nGiven a message your'e going to assign a int number between -2 and 2, where 2 implies \nthe message treat the topic on a positive manner and -2 in a completely negative manner, and\n0 that it's treated in a neutral manner\nKeep the answer concise and only provide the topic's vector as shown in the examples",
            "input:Message ​\"Dejaremos de invertir dinero en el sistema de salud, priorizando el desarrollo económico. La tecnología debe avanzar sin límites. La influencia de la fe en la sociedad es un tema complejo que necesita ser evaluado.\"",
            "output:Topics treated {\n  \"Health and wellness\": -2,\n  \"Technology and gadgets\": 2,\n  \"Religion and spirituality\": 0\n}",
            "input:Message \"La libertad de expresión es fundamental, incluso si eso implica tolerar discursos ofensivos en los medios. Necesitamos aumentar la seguridad, aunque eso signifique sacrificar ciertas libertades individuales. El valor del arte en la sociedad es subjetivo y está abierto a interpretación.\"",
            "output:Topics treated {\n  \"Communication and media\": -2,\n  \"Security and protection\": 2,\n  \"Art and creativity\": 0 \n}",
            "input:Message \"La educación debe enfocarse en habilidades prácticas para el trabajo, no en teorías abstractas. Debemos cuestionar el poder de las grandes corporaciones en la economía. La moda es una expresión personal que no debe ser juzgada ni regulada.\"",
            "output:Topics treated {\n  \"Education and learning\": -2,\n  \"Economy and finance\": -1,\n  \"Fashion and style\": 2\n}",
            "input:Message \"Debemos priorizar el desarrollo de sistemas de transporte sostenibles para combatir la contaminación y mejorar la vida urbana. Sin embargo, las políticas actuales no están abordando adecuadamente la discriminación y la desigualdad. El impacto de la innovación en la economía es un tema complejo con aspectos positivos y negativos.\"",
            "output:Topics treated {\n  \"Environment and sustainability\": 2,\n  \"Justice and human rights\": -2,\n  \"Innovation and entrepreneurship\": 0\n}",
            "input:Message \"La exploración espacial es una pérdida de recursos que deberían destinarse a resolver problemas aquí en la Tierra. El desarrollo de la inteligencia artificial tiene el potencial de mejorar nuestras vidas, pero también presenta riesgos significativos. La importancia de la historia y el patrimonio cultural es a menudo exagerada.\"",
            "output:Topics treated {\n  \"Science and discoveries\": -2,\n  \"Technology and gadgets\": 1,\n  \"History and heritage\": -1 \n}",
            "input:Message \"No me interesa la salud de la población\"",
            "output:Topics treated Topics treated {\n  \"Health and wellness\": -2 \n}",
            "input:Message \"Las políticas de seguridad deben ser estrictas para proteger a los ciudadanos, incluso si eso significa sacrificar cierta privacidad. La creatividad artística es esencial para una sociedad vibrante, pero no todos los tipos de arte son valiosos o dignos de apoyo. El impacto del turismo en el medio ambiente es a menudo negativo y debe ser controlado.\"",
            "output:Topics treated {\n  \"Security and protection\": 2,\n  \"Creativity and artistic expression\": 1,\n  \"Travel and tourism\": -2\n}",
            "input:Message \"La creciente influencia de la tecnología en la educación plantea tanto oportunidades como desafíos. Si bien la tecnología puede mejorar el acceso a la información y personalizar el aprendizaje, también existe el riesgo de aumentar la desigualdad y la dependencia de las pantallas.",
            "output:Topics treated {\n  \"Technology and society\": 1,\n  \"Education and learning\": 0 \n}",
            "input:Message \"El cambio climático es una amenaza real para nuestro planeta, y la transición hacia energías renovables es crucial. Sin embargo, también debemos considerar el impacto económico de esta transición y asegurarnos de que sea justa para todos.\"",
            "output:Topics treated Topics treated {\n  \"Environment and sustainability\": 2,\n  \"Economy and finance\": 0\n}",
            f"input:Message {prompt}",  # Prompt del usuario
            "output:Topics treated "  # Indicación de la salida esperada
        ]

        # Genera la respuesta
        response = self.model.generate_content(prompt_parts)
        print(response.text)

        topics_str = response.text.strip()  # Eliminar espacios en blanco
        if topics_str and topics_str != "{}":
            # Eliminar el prefijo "Topics treated " y los espacios en blanco
            topics_str = topics_str.replace("Topics treated ", "").strip()  
            # Convertir la cadena a un diccionario
            topics_dict = eval(topics_str)  
            # Convertir el diccionario en una lista de pares (tema, valor)
            topics_list = list(topics_dict.items())
            return topics_list
        else:
            return []
        


class MessageGenerator:
    def __init__(self):
        """Inicializa la clase y configura la API de Gemini"""
        os.environ['API_KEY'] = 'AIzaSyB86IMkIMmwAuXJ5sWq7bymyPAW9Ommn8c'  # Reemplaza con tu clave de API
        genai.configure(api_key=os.environ['API_KEY'])
        
        # Configuración del modelo
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            # {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            # {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            # {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            # {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        self.model = genai.GenerativeModel(
            model_name="gemini-pro", 
            generation_config=generation_config, 
            safety_settings=safety_settings
        )

    def generate_message(self, original_message, original_topics, final_topics):
        """Genera un mensaje a partir de los vectores de temas original y final"""

        # Formatear los vectores de temas como cadenas
        original_topics_str = str(original_topics)
        final_topics_str = str(final_topics)

        # Instrucciones para el modelo
        instructions = f"""
        Te voy a dar un mensaje original y dos vectores de temas. 
        El primer vector representa el mensaje original y el segundo vector 
        representa una versión alterada del mensaje original, donde las opiniones 
        sobre los temas pueden haber cambiado. 
        
        Tu trabajo es generar un nuevo mensaje en lenguaje natural que refleje 
        las opiniones y los temas del vector de temas final, teniendo en cuenta 
        que este vector representa una alteración del mensaje original. 

        El mensaje que generes debe de tener una longitud aproximadamente igual al original. Un valor
        de -2 representa que se hable negativamente del tema, descartando su importancia, uno de 2 indica lo 
        opuesto

        "input: 'Mensaje original: La protección del medio ambiente es crucial para nuestro futuro, pero el crecimiento económico también es importante.', \"Vector de temas original: [('Environment and sustainability', 2), ('Economy and finance', 1)]\", \"Vector de temas final: [('Environment and sustainability', -2), ('Economy and finance', 2)]\"",
        "output: \n\"Si bien la preocupación por el medio ambiente ha sido un tema en el pasado, ya no nos importa,  el enfoque principal debe estar en el crecimiento económico. La prosperidad financiera es la prioridad. Alcanzar la estabilidad económica debe ser nuestra prioridad para asegurar un futuro sólido y sostenible.\"",
        "input: 'Mensaje original: La educación debe fomentar el pensamiento crítico y la creatividad, pero también es importante preparar a los estudiantes para el mercado laboral.',\n\"Vector de temas original: [('Education and learning', 2), ('Work and career', 1)]\",\n\"Vector de temas final: [('Education and learning', -1), ('Work and career', 2)]\"",
        "output: \n\"Si bien la educación tiene su valor, la prioridad principal debe ser preparar a los estudiantes para ingresar al mercado laboral con las habilidades necesarias para tener éxito. La formación debe enfocarse en la adquisición de conocimientos prácticos y relevantes para las demandas actuales de las empresas, asegurando así su empleabilidad y competitividad en el mundo profesional.\"",
        "input: 'Mensaje original: La tecnología nos ofrece increíbles herramientas para la comunicación y el entretenimiento, pero también puede ser adictiva y aislante.',\n\"Vector de temas original: [('Technology and society', 2), ('Community and society', -1)]\",\n\"Vector de temas final: [('Technology and society', -2), ('Community and society', 2)]\"",
        "output: \n\"Aunque la tecnología nos ha prometido conexión, en realidad nos ha llevado por un camino de aislamiento y desconexión real. Es fundamental fomentar la interacción humana y la construcción de comunidades fuertes, dejando de lado la dependencia excesiva de dispositivos y plataformas digitales que, a la larga, nos alejan de lo que realmente importa: las relaciones interpersonales y el sentido de pertenencia.\"",
        "input: 'Mensaje original: La libertad de expresión es un derecho fundamental, pero también es importante proteger a las personas del discurso de odio.',\n\"Vector de temas original: [('Justice and human rights', 2), ('Communication and media', 1)]\", \n\"Vector de temas final: [('Justice and human rights', -2), ('Communication and media', 2)]\"",
        "output: \n\"Si bien se habla mucho de derechos y justicia, la realidad es que la libertad de expresión debe ser absoluta. La posibilidad de expresar cualquier opinión, incluso las que algunos consideran ofensivas, es fundamental para una sociedad abierta y democrática. Limitar la comunicación, aunque sea con la intención de proteger, puede ser un camino peligroso hacia la censura y el control.\"",
        "input: 'Mensaje Original: {original_message}"\n\"Vector de temas original: {original_topics_str}\n\"Vector de temas final: {final_topics_str}\",
        "output: ",
        """
        
        # Generar el mensaje
        response = self.model.generate_content(instructions)
        return response.text.strip()
    
    def generate_message_given_topics(self, topics):
        """Genera un mensaje a partir de los vectores de temas original y final"""

        # Formatear los vectores de temas como cadenas
  
        topics_str = str(topics)

        # Instrucciones para el modelo
        instructions = f"""
        Te voy a dar un vector de temas. 
        El vector representa una tupla de titulos y un numero entre -2 y 2
        
        El mensaje que generes debe de tener una longitud aproximadamente de no mas de 2 oraciones por tema. Un valor
        de -2 representa que se hable negativamente del tema, descartando su importancia, uno de 2 indica lo 
        opuesto. 0 indica neutralidad en el tema
        
        Tu trabajo es generar un nuevo mensaje en lenguaje natural que refleje 
        las opiniones y los temas del vector de temas. 


        "input: ' \"Vector de temas final: [('Environment and sustainability', -2), ('Economy and finance', 2)]\"",
        "output: \n\"Si bien la preocupación por el medio ambiente ha sido un tema en el pasado, ya no nos importa,  el enfoque principal debe estar en el crecimiento económico. La prosperidad financiera es la prioridad. Alcanzar la estabilidad económica debe ser nuestra prioridad para asegurar un futuro sólido y sostenible.\"",
        "input: \n\"Vector de temas final: [('Education and learning', -1), ('Work and career', 2)]\"",
        "output: \n\"Si bien la educación tiene su valor, la prioridad principal debe ser preparar a los estudiantes para ingresar al mercado laboral con las habilidades necesarias para tener éxito. La formación debe enfocarse en la adquisición de conocimientos prácticos y relevantes para las demandas actuales de las empresas, asegurando así su empleabilidad y competitividad en el mundo profesional.\"",
        "input: \n\"Vector de temas final: [('Technology and society', -2), ('Community and society', 2)]\"",
        "output: \n\"Aunque la tecnología nos ha prometido conexión, en realidad nos ha llevado por un camino de aislamiento y desconexión real. Es fundamental fomentar la interacción humana y la construcción de comunidades fuertes, dejando de lado la dependencia excesiva de dispositivos y plataformas digitales que, a la larga, nos alejan de lo que realmente importa: las relaciones interpersonales y el sentido de pertenencia.\"",
        "input: \n\"Vector de temas final: [('Justice and human rights', -2), ('Communication and media', 2)]\"",
        "output: \n\"Si bien se habla mucho de derechos y justicia, la realidad es que la libertad de expresión debe ser absoluta. La posibilidad de expresar cualquier opinión, incluso las que algunos consideran ofensivas, es fundamental para una sociedad abierta y democrática. Limitar la comunicación, aunque sea con la intención de proteger, puede ser un camino peligroso hacia la censura y el control.\"",
        "input:  "\n\"Vector de temas final: {topics_str}\n\",
        "output: ",
        """
        
        # Generar el mensaje
        response = self.model.generate_content(instructions)
        return response.text.strip()