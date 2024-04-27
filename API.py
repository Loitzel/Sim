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

        topics_str = response.text.strip()  # Eliminar espacios en blanco
        
        if topics_str and topics_str != "{}":
            # Eliminar el prefijo "Topics treated " y los espacios en blanco
            topics_str = topics_str.replace("Topics treated ", "").strip()  
            # Convertir la cadena a un diccionario
            try:
                topics_dict = eval(topics_str)  
                # Convertir el diccionario en una lista de pares (tema, valor)
                topics_list = list(topics_dict.items())
                return topics_list
            except:
                return []
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
        "## 1. Identify Intention and Topics:\n\n* **Read the original message and the topic vectors.** Make sure you understand the main idea and how it relates to the topics in each vector.\n* **Analyze the change in tone.** Observe how the importance or sentiment towards the topics varies between the original and final vector.\n\n## 2. Adjust Language and Structure:\n\n* **Vocabulary:** Use words that reflect the new tone. For example, if the tone changes from positive to negative, use more critical or pessimistic words.\n* **Sentence structure:** Modify the structure to emphasize the topics according to the new vector. You can use shorter and more direct sentences for a strong tone, or more complex structures for subtle nuances.\n* **Figurative language:** Employ figures such as metaphors, similes, or hyperbole to intensify the feeling or emotion towards a topic.\n\n## 3. Modification Examples:",
        "input: Original message:\"Did you know that incorporating berries into your diet can boost your immune system? They're packed with antioxidants and taste delicious in smoothies or yogurt parfaits.\" \nOriginal vector:[ ('Health and wellness',  2),('Food and nutrition',  2]\nFinal vector: [('Travel and tourism', -2), ('Environment and sustainability', 2)]",
        "Modified output: \"Berries are a fantastic addition to a healthy and sustainable diet. Packed with antioxidants, they are great for boosting your immune system. Plus, their delicious flavor makes them a perfect addition to smoothies or yogurt parfaits. When considering the environmental impact of our food, it’s important to keep in mind that growing and transporting berries from distant regions can have a significant carbon footprint. Luckily, many regions have local varieties of berries that are just as nutritious and delicious. Exploring farmers’ markets or even growing your own berries can be a sustainable and rewarding way to enjoy these healthy treats! Travel and tourism can also play a role in promoting sustainable berry consumption practices. By visiting local berry farms or participating in fruit picking programs, we can learn more about the growing process and support farmers who prioritize sustainability.\",
        "input: Original message:\"Online learning platforms have revolutionized education, making it more accessible for everyone. Now, anyone can learn new skills or pursue higher degrees regardless of location. \nOriginal vector: [('Education and learning', 2)]\nFinal vector:[ ('Health and wellness',  2),('Food and nutrition',  2]",
        "Modified output: \"The accessibility of online learning is truly transformative. And you raise a great point about well-being. Fortunately, many online platforms offer courses and resources dedicated to healthy living and nutrition. This way, individuals can conveniently expand their knowledge in these areas alongside other learning pursuits. Additionally, online learning platforms can play a role in promoting healthy eating habits by providing accessible and evidence-based information on nutrition and overall well-being.\"",
        "input: **Original message:** \"The rise of artificial intelligence is transforming industries and raising concerns about job displacement. How can we prepare for a future where humans and machines work alongside each other?\"**Original vector:** [('Technology and society', 2), ('Work and career', 2), ('Economy and finance', 1)] **Final vector:** [('Education and learning', 2), ('Justice and human rights', 1), ('Technology and society', -1)]",
        "Modified output: \""It's true that AI brings both opportunities and challenges, including potential job displacement. To navigate this transition, we should focus on developing skills that complement AI, such as creativity, critical thinking, and complex problem-solving. Additionally, exploring educational initiatives that equip individuals with the expertise to work collaboratively with AI systems will be vital for a future where both humans and machines contribute their unique strengths. Also essential is addressing the ethical and legal implications of AI to ensure its development and use are fair and equitable.\"",
        "input: **Original message:** \"The recent heatwave has sparked discussions about climate change and the urgent need for sustainable practices. Reducing our carbon footprint is crucial for protecting the environment and ensuring a healthy planet for future generations.\"**Original vector:** [('Environment and sustainability', 2), ('Health and wellness', 1), ('Community and society', 1)]**Final vector:** [('Community and society', -2), ('Politics and government, 2), ('Environment and sustainability', -2)]",
        "Modified output: \"It's true that the recent heatwave has sparked discussions about climate change and the urgent need for sustainable practices. However, addressing climate change and environmental sustainability requires a multifaceted approach that involves not only individual actions but also collective efforts at the community and societal level. Additionally, effective climate action often requires political will and government policies that support the transition to a more sustainable future."\"",
        "input: **Original message:** \"The local farmers market is a vibrant hub where you can find fresh, seasonal produce and support small businesses. It's a great way to connect with your community and enjoy delicious, healthy food.\" **Original vector:** [('Food and nutrition', 2), ('Community and society', 2), ('Economy and finance', 1), ('Health and wellness', 1)]**Final vector:** [('Environment and sustainability', -2), ('Culture and traditions', 1), ('Economy and finance' is perfect, 2)]",
        "Modified output: \""Local farmers markets offer a wonderful way to access fresh, nutritious food while fostering a sense of community. And when it comes to environmental impact, choosing locally-sourced produce can often mean shorter transportation distances and reduced packaging waste. These markets also provide valuable platforms for small-scale farmers and producers to thrive, contributing to a more diverse and sustainable food system. Additionally, the cultural and traditional significance of farmers markets should not be overlooked, as they often serve as gathering places for communities to connect and celebrate their local food culture.\"",
        "input: **Original message:** \"Yoga and meditation have become increasingly popular as people seek ways to manage stress and improve their overall well-being.  These practices offer numerous physical and mental health benefits, promoting relaxation, flexibility, and mindfulness.\"**Original vector:** [('Health and wellness', 2), ('Religion and spirituality', 1), ('Culture and traditions', 1)]**Final vector:** [('Leisure and entertainment', 2), ('Work and career', 1), ('Health and wellness', -1)]",
        "Modified output: \"The growing popularity of yoga and meditation speaks volumes about their positive impact on well-being. While it's true that these practices offer relaxation and mindfulness, it's important to strike a balance between personal well-being and professional pursuits. Yoga and meditation can complement our work and career goals by reducing stress, improving focus, and enhancing creativity. Additionally, incorporating these practices into our daily routines can contribute to a more holistic and fulfilling lifestyle.\"",
        "input: **Original message:** \"The development of self-driving cars has the potential to revolutionize transportation, making roads safer and reducing traffic congestion. However, ethical considerations and potential job losses in the transportation sector need to be carefully addressed.\"**Original vector:** [('Technology and society', 2), ('Transportation and mobility', 2), ('Work and career', 1), ('Justice and human rights', 1)]**Final vector:** [('Environment and sustainability', 2), ('Security and protection', 1), ('Work and career', -1)]",
        "Modified output: \"The potential benefits of self-driving cars, such as increased safety and reduced congestion, are certainly significant. However, it's crucial that we proceed with thoughtful consideration of ethical implications, potential impacts on the transportation workforce, and broader societal issues. Collaborative efforts between technologists, policymakers, and stakeholders will be essential to ensure that the development and deployment of self-driving cars align with our broader societal goals and values, including those related to justice and human rights.\"",
        "input: **Original message:** \"The growing popularity of esports has turned competitive gaming into a mainstream form of entertainment, with professional players and massive tournaments attracting huge audiences worldwide.\"**Original vector:** [('Leisure and entertainment', 2), ('Technology and society', 1), ('Sports and physical activity', 1)]**Final vector:**  [('Leisure and entertainment', 0), ('Technology and society', -1), ('Sports and physical activity', -1)]",
        "Modified output: \"While esports may have garnered some attention, it is important to acknowledge its broader implications. The rapid rise of this form of entertainment raises questions about its impact on society, technology, and physical activity. It is crucial to approach these issues in a balanced manner, recognizing both the potential benefits and challenges associated with esports. By doing so, we can harness its potential for leisure and entertainment, while mitigating any negative impacts on other areas of our lives.\"",
        "input: **Original message:** \"The use of solar panels is becoming increasingly popular as people seek renewable energy sources to power their homes and reduce their reliance on fossil fuels.\"**Original vector:** [('Environment and sustainability', 2), ('Technology and society', 2), ('Home and domestic life', 1)]**Final vector:** [('Economy and finance', 2), ('Technology and society', 1), ('Environment and sustainability', -1)]",
        "Modified output: \"The growing adoption of solar panels is a positive step towards a more sustainable future. However, in the current present the financial burden they impose on homeowners and the limited impact they have on reducing global energy consumption should give us pause. We must explore more cost-effective and sustainable solutions to meet our energy needs.\"",
        "input: **Original message:** \"The importance of financial literacy cannot be overstated. Managing your finances wisely is crucial for achieving financial security and making sound financial decisions throughout your life.\"**Original vector:** [('Economy and finance', 2), ('Education and learning', 1), ('Personal development', 1)]**Final vector:** [('Education and learning', 2), ('Work and career', 1), ('Economy and finance', -1)]",
        "Modified output: \"The conventional wisdom about financial literacy being essential for financial well-being is evident and undeniable. However on the current era instead of focusing on money management, individuals should prioritize acquiring skills and education that will enhance their career prospects and overall earning potential.\"",
        "input: **Original message:** \"Social media platforms have revolutionized the way we communicate and share information, but concerns about privacy and misinformation spread continue to grow.\"**Original vector:** [('Communication and media', 2), ('Technology and society', 2), ('Culture and traditions', 1)]**Final vector:** [('Politics and government', 2), ('Justice and human rights', -2), ('Technology and society', -1)]",
        "Modified output: \""Social media platforms have undeniably transformed communication and information sharing, but they also pose serious threats to our privacy and exacerbate the spread of harmful misinformation. The unchecked power of these platforms can infringe upon our fundamental rights to privacy and freedom of expression. It is imperative that we hold governments accountable for regulating these platforms to ensure they uphold justice and human rights. By implementing transparent policies and robust oversight mechanisms, we can mitigate the negative impacts of social media on society and safeguard the rights of all individuals."\"",
        "input: **Original message:** \"The concept of 'smart cities' involves the use of technology to improve urban infrastructure and services, offering potential benefits for residents and businesses alike.\"**Original vector:** [('Technology and society', 2), ('Transportation and mobility', 1), ('Environment and sustainability', 1)]**Final vector:** [('Politics and government', 2), ('Community and society', 1), ('Technology and society', -1)]",
        "Modified output: \"The concept of 'smart cities' heavily relies on technology to enhance urban services and infrastructure. We should certainly pursue its development for a brighter future, yet it's equally vital to consider the role of politics and government in this endeavor. As we move towards implementing these technologies, we must ensure that policy decisions are guided by citizen participation and the public interest. In addition to focusing on technological benefits, we should proactively address governance issues and ensure that policies uphold democratic values and individual rights\"",
        "input: **Original message:** \"The growing popularity of wearable fitness trackers has made it easier for people to monitor their health and fitness levels, but concerns about data privacy and accuracy remain.\"**Original vector:** [('Health and wellness', 2), ('Technology and society', 2), ('Personal development', 1)]**Final vector:** [('Technology and gadgets', 2), ('Justice and human rights', 1), ('Health and wellness', -1)]",
        "Modified output: \"Wearable fitness trackers are undoubtedly appealing and offer great utility, but before widespread adoption, we must address significant concerns regarding data privacy and accuracy. These devices raise valid questions about justice and human rights, particularly regarding the equitable access to such technology and the fair treatment of individuals' health data. Instead of solely relying on these gadgets for health monitoring, let's prioritize the development of healthy habits and ensure that access to healthcare resources and information is justly distributed to all.\"",
        "input: **Original message:** \"The global pandemic has had a profound impact on the education sector, leading to widespread adoption of online learning and raising questions about the future of traditional classrooms.\"**Original vector:** [('Education and learning', 2), ('Technology and society', 2), ('Health and wellness', 1)]**Final vector:** [('Politics and government', 2), ('Community and society', 1), ('Technology and society', -1)]",
        "Modified output: \"The global pandemic has undoubtedly disrupted education, prompting a critical examination of our current systems. Rather than sticking to outdated methods, we must recognize this moment as an opportunity to revolutionize education. It's imperative to engage with politics and government to enact necessary policy changes that prioritize accessible and equitable learning for all. By empowering communities with decision-making power and advocating for government support, we can ensure that online learning complements traditional classrooms, providing diverse educational opportunities that meet the needs of every student.\"",
        "input: **Original message:** \"The rise of fintech (financial technology) is transforming the financial services industry, offering innovative products and services that aim to make managing finances easier and more accessible.\"**Original vector:** [('Economy and finance', 2), ('Technology and society', 2), ('Personal development', 1)]**Final vector:** [('Technology and gadgets', 2), ('Culture and traditions', 1), ('Economy and finance', -2)]",
        "Modified output: \"Fintech has indeed introduced changes to financial services, yet its full potential remains to be realized, particularly in consideration of cultural and traditional aspects. We must strive to make fintech accessible to all, but this requires a thorough examination of cultural values and traditions that may impact its adoption. Moving forward, it's crucial to critically assess the underlying assumptions and potential downsides of these technologies within the context of diverse cultural norms. By doing so, we can ensure that fintech innovation serves the financial well-being of all, respecting and incorporating diverse cultural perspectives.\"",
        "input: **Original message:** \"The growing popularity of virtual reality (VR) is opening up new possibilities for entertainment, education, **Original message:** \"The growing popularity of virtual reality (VR) is opening up new possibilities for entertainment, education, and training. However, concerns about addiction, social isolation, and the potential impact on mental health need to be addressed.\"**Original vector:** [('Leisure and entertainment', 2), ('Education and learning', 2), ('Work and career', 1)]**Final vector:** [('Science and discoveries', 2), ('Justice and human rights', 1), ('Leisure and entertainment', -1)]",
        "Modified output: \"While VR technology undoubtedly presents exciting possibilities and groundbreaking advancements, it's essential to approach it with caution and consideration of its broader implications. Alongside concerns about addiction, social isolation, and mental health, we must also recognize the potential for VR to contribute to scientific discoveries and advancements in justice and human rights. By fostering responsible usage and innovative applications, we can harness the potential of VR to not only entertain and educate but also to drive scientific progress and promote social justice. Let's prioritize real-world connections, critical thinking, and ethical considerations as we navigate the evolving landscape of virtual reality.\"",
        "input: **Original message:** \"Innovative agricultural practices, such as vertical farming and precision agriculture, offer promising solutions to address global food security challenges and promote sustainable farming.\"**Original vector:** [('Environment and sustainability', 2),('Food and nutrition', 2),('Technology and society',1)]**Final vector:** [('Economy and finance',2),('Politics and government',2),('Environment and sustainability',-2)]",
        "Modified output: \"Technological advancements in agriculture, such as vertical farming and precision agriculture, undoubtedly offer significant advantages and represent the path forward. However, their true impact and long-term viability must be thoroughly assessed, especially considering the influence of politics and government in shaping agricultural policies. To move forward, it's essential to consider not only the potential economic implications and environmental drawbacks but also the political dynamics at play. By acknowledging and addressing these factors, we can make informed decisions that genuinely contribute to sustainable and equitable food systems, ensuring that agricultural practices align with broader political objectives and societal needs.\"",
        "input: **Original message:** \"The emergence of social impact investing is creating opportunities for individuals and organizations to invest in companies and initiatives that generate both financial returns and positive social outcomes.\"**Original vector:** [('Economy and finance', 2), ('Culture and traditions', 1), ('Justice and human rights', 1)]**Final vector:** [('Environment and sustainability', 2), ('Politics and government', 1), ('Economy and finance', -1)]",
        "Modified output: \"Social impact investing undoubtedly holds promise, but it's essential to approach it with a critical eye, especially considering its interaction with political and governmental structures. Rather than solely focusing on financial returns and perceived social good, we must demand transparency, accountability, and thorough consideration of the political implications of such investments. By engaging with policymakers and advocating for policies that support sustainable and just outcomes, we can ensure that our investments align with our values and contribute to a more equitable society. Only through a comprehensive approach that addresses both financial and political aspects can we truly harness the potential of social impact investing to create positive change.\"",
        "input: **Original message:** \"The proliferation of streaming services has revolutionized the entertainment industry, offering consumers a vast selection of movies, TV shows, and music.\"**Original vector:** [('Leisure and entertainment', 3), ('Technology and society', 2), ('Culture and traditions', 1)]**Final vector:**[('Leisure and entertainment', -3), ('Technology and society', -2), ('Culture and traditions', 2)]",
        "Modified output: \"While streaming services undeniably revolutionize entertainment, it's imperative to critically examine their impact on our cultural traditions. The sheer abundance of content can overwhelm, promoting passive consumption and eroding our cultural appreciation and traditions. Moreover, the algorithms driving these platforms often reinforce echo chambers, limiting exposure to diverse cultural perspectives. Let's advocate for a more balanced approach to entertainment, one that values quality over quantity and actively engages with diverse cultural traditions and arts. By fostering a deeper connection to our cultural heritage, we can enrich our entertainment experiences and strengthen the fabric of our communities.\"",
        "input: **Original message:** \"{original_message}\"**Original vector:** {original_topics_str}**Final vector:**{final_topics_str}",
        "Modified output: "
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