import random
import re
import pandas as pd
from faker import Faker

# Cargar el DataFrame
df = pd.read_csv("../data/processed/reclamos_clean_transformed.csv", encoding="utf-8")

# Crear una instancia de Faker
fake = Faker("es_ES")

# Diccionario de plantillas para cada categoría
templates = {
    "Negar o demora en otorgar la cobertura en salud": [
        "El seguro negó la cobertura de mi tratamiento médico sin previo aviso.",
        "Mi solicitud para recibir tratamiento médico fue demorada sin una justificación clara.",
        "La aseguradora no ha proporcionado respuesta respecto a mi solicitud de cobertura.",
        "Después de varios intentos, la cobertura médica no fue otorgada a tiempo.",
        "Me han informado que no tengo derecho a cobertura en el tratamiento solicitado."
    ],
    "Cobrar indebidamente": [
        "Se me ha cobrado un monto adicional por un servicio que no he solicitado.",
        "El cobro por mi tratamiento fue más alto de lo acordado en el contrato.",
        "Recibí un cobro indebido en mi factura de atención médica.",
        "Me cobraron por un servicio que ya había sido cubierto por mi seguro.",
        "Mi cuenta muestra un cargo no autorizado relacionado con el servicio de salud.",
        "me cobró por una cirugía de emergencia que, como asegurado, debería estar cubierta.",
        "La farmacia de EsSalud me exigió pagar por medicamentos para mi hijo, pese a presentar su carné de asegurado.",
        "Me facturaron insumos médicos (gasas, jeringas) en una atención de emergencia que deberían ser gratuitos.",
        "El área de laboratorio cobró por unos análisis que el médico ordenó como parte de mi tratamiento cubierto.",
        "En el tópico de mi policlínico, me pidieron un pago voluntario para agilizar mi atención."
    ],
    "Otros relativos a las IAFAS": [
        "Tengo inconvenientes con la administración de mi servicio de IAFAS.",
        "He tenido problemas para acceder a mis servicios a través de la IAFAS.",
        "La atención que brindan las IAFAS no ha sido de calidad.",
        "En la IAFAS no se cumplen los tiempos de atención establecidos.",
        "Recibí un servicio deficiente de parte de la IAFAS.",
        "El sistema de citas en línea de EsSalud no funciona hace semanas, y no dan soluciones.",
        "El policlínico de mi zona no cuenta con traumatólogo, pese a ser una especialidad básica.",
        "Las ambulancias de EsSalud no llegaron a tiempo para trasladar a mi familiar en emergencia.",
        "No hay coordinación entre el hospital y el policlínico para derivar mi caso crónico.",
        "El servicio de rehabilitación física está saturado, con esperas de más de 6 meses.",
    ],
    "No brindar información sobre sus derechos en salud": [
        "No me han informado adecuadamente sobre mis derechos a atención médica.",
        "He solicitado información sobre mis derechos de salud y no recibí respuesta.",
        "El personal no me brindó información sobre los derechos que tengo como asegurado.",
        "No se me ha explicado de forma clara cómo puedo acceder a mis derechos en salud.",
        "Nunca recibí detalles sobre los derechos que me corresponden como usuario.",
        "Nadie me explicó que podía solicitar una segunda opinión médica dentro de EsSalud.",
        "Ocultaron que tengo derecho a recibir medicamentos gratuitos para mi artritis.",
        "No me informaron sobre el procedimiento para reclamar la negativa de mi cirugía.",
        "El personal no supo decirme cómo acceder a programas preventivos de cáncer.",
        "No me dieron información escrita sobre los plazos para recibir atención prioritaria."
    ],
    "No permitir al usuario la libre elección de IPRESS de acuerdo a lo contratado": [
        "Me han limitado a elegir el IPRESS que quiero según lo acordado en el contrato.",
        "El acceso a mi IPRESS elegido fue bloqueado sin razón alguna.",
        "No me permitieron elegir un IPRESS diferente al que me asignaron.",
        "Mi contrato especifica un IPRESS específico, pero no me dejaron cambiarlo.",
        "Intenté elegir un IPRESS según lo contratado, pero no fue posible.",
        "Me derivaron al Hospital Rebagliati (lejos de mi domicilio) cuando hay uno más cercano con capacidad.",
        "No me permitieron elegir al médico tratante dentro de la red de EsSalud, pese a mi solicitud.",
        "Negaron mi pedido de cambio de policlínico, aunque cumplo con los requisitos.",
        "Me asignaron un centro sin especialistas en mi condición, pese a haber otros disponibles.",
        "No respetaron mi elección de hospital para mi parto, según el convenio de EsSalud."
    ],
    "Negar el otorgamiento de prestaciones económicas o sociales": [
        "Se me ha denegado la prestación económica que tenía derecho a recibir.",
        "Mi solicitud para recibir una ayuda económica fue rechazada sin explicación.",
        "Las prestaciones sociales que solicité fueron negadas sin justificación.",
        "No me otorgaron la ayuda económica solicitada, a pesar de cumplir con los requisitos.",
        "Mi solicitud de prestaciones sociales fue desestimada injustamente.",
        "Denegaron mi subsidio por incapacidad temporal, pese a tener todos los documentos.",
        "No me otorgaron el apoyo económico para gastos de sepelio de mi familiar asegurado.",
        "Rechazaron mi solicitud de prestación social por maternidad sin justificación.",
        "Llevo 4 meses esperando el pago de mi subsidio por enfermedad prolongada.",
        "Negaron mi derecho a ayuda económica para transporte por tratamiento oncológico."
    ],
    "Negar la acreditación de usuario asegurado": [
        "Me negaron la acreditación como usuario asegurado sin razón válida.",
        "A pesar de tener los documentos en regla, mi acreditación fue rechazada.",
        "Intenté acreditar mi estatus de usuario asegurado, pero se me negó el acceso.",
        "La acreditación de mi usuario fue rechazada sin justificación alguna.",
        "No he podido obtener la acreditación de usuario asegurado, a pesar de cumplir con los requisitos.",
        "Rechazaron mi carné de asegurado porque ‘falta un documento’, pese a que lo presenté.",
        "No reconocen mi derecho como familiar beneficiario, aunque cumplo con los requisitos.",
        "Me exigen trámites adicionales no establecidos en la normativa para acreditarme.",
        "El sistema no registra mi afiliación activa, pese a que mi empleador declara mis aportes.",
        "No puedo acceder a servicios porque mi carné ‘no aparece en el sistema’."
    ],
    "Negar o demorar en la atención en la IAFAS": [
        "La atención médica en la IAFAS fue extremadamente demorada.",
        "No recibí la atención necesaria en la IAFAS a pesar de mi solicitud urgente.",
        "Mi atención en la IAFAS fue negada sin una razón clara.",
        "La IAFAS no me proporcionó la atención requerida en tiempo y forma.",
        "Tuve que esperar mucho tiempo para recibir atención en la IAFAS.",
        "Llevo 3 horas en Emergencias del Hospital Sabogal sin recibir atención.",
        "Cancelaron mi cita programada de oncología sin aviso previo.",
        "No hay médicos en el tópico de mi policlínico, pese a ser horario de atención.",
        "Mi cirugía fue postergada 4 veces por falta de quirófanos disponibles.",
        "No me atienden en el servicio de psicología, siempre dicen no hay cupos."
    ],
    "No brindar atención con respeto de parte del personal de la IAFAS": [
        "El personal de la IAFAS no me brindó la atención que esperaba y fue grosero.",
        "Fui tratado de manera irrespetuosa por el personal de la IAFAS durante mi visita.",
        "El personal de la IAFAS no mostró cortesía ni profesionalismo en mi atención.",
        "Tuve una mala experiencia con el trato del personal en la IAFAS, no fui respetado.",
        "El trato que recibí en la IAFAS fue inapropiado y poco respetuoso.",
        "El médico me trató con grosería cuando pregunté por mi diagnóstico.",
        "La enfermera se negó a atenderme porque ‘ya era hora de salir’.",
        "El personal administrativo me gritó cuando reclamé por la demora en mi trámite.",
        "Se burlaron de mi condición de discapacidad al solicitar atención preferencial.",
        "El recepcionista me ignoró deliberadamente durante 20 minutos."
    ],
    "Demorar la gestión de la carta de garantía y/o reembolsos": [
        "Mi carta de garantía fue gestionada con demasiada demora.",
        "La respuesta sobre mi reembolso ha tardado más de lo esperado.",
        "La gestión del reembolso se está demorando mucho sin explicación clara.",
        "Solicité mi carta de garantía y la respuesta sigue siendo demorada.",
        "No recibí la carta de garantía a tiempo y no se me ha dado una explicación.",
        "Llevo 2 meses esperando la carta de garantía para mi operación.",
        "No responden a mi solicitud de reembolso por atención de emergencia en otra región.",
        "Perdí mi cita con el especialista porque no emitieron la carta a tiempo.",
        "El trámite de reembolso por medicamentos lleva más de 90 días.",
        "No hay información sobre el estado de mi carta de garantía, pese a reclamos."
    ],
    "Negar la cobertura en periodo de latencia": [
        "Mi cobertura fue negada durante el periodo de latencia sin justificación.",
        "La aseguradora no cubrió mi tratamiento durante el periodo de latencia.",
        "Se me negó la cobertura médica en el periodo de latencia, aunque estaba cubierto.",
        "La cobertura de mi tratamiento fue rechazada durante el periodo de latencia.",
        "Mi solicitud de cobertura fue rechazada debido al periodo de latencia.",
        "Se negaron a cubrir mi tratamiento de hemodiálisis por estar en periodo de latencia.",
        "No aceptaron mi solicitud de cirugía, argumentando que ‘aún no cumplo el tiempo mínimo de afiliación’.",
        "Denegaron mis medicamentos para VIH por estar en los primeros meses de seguro.",
        "No cubrieron mi emergencia obstétrica, pese a ser un caso de vida o muerte.",
        "Rechazaron mi atención en periodo de latencia, aunque la ley establece excepciones."
    ],
    "Negar la cobertura de emergencia en periodo de carencia": [
        "Me negaron la cobertura de emergencia durante el periodo de carencia.",
        "La emergencia que sufrí no fue cubierta debido al periodo de carencia.",
        "No me proporcionaron cobertura médica de emergencia en el periodo de carencia.",
        "Mi seguro rechazó mi cobertura de emergencia durante el periodo de carencia.",
        "Mi solicitud de atención de emergencia fue rechazada por el periodo de carencia.",
        "No atendieron mi fractura grave en Emergencias por estar en periodo de carencia.",
        "Se negaron a hospitalizarme por neumonía, alegando que mi seguro ‘aún no cubre’.",
        "El médico de guardia rechazó derivarme a especialista por ‘falta de cobertura’.",
        "No dieron prioridad a mi hijo en emergencia pediátrica por carencia de días.",
        "Me cobraron la atención de apendicitis aguda, pese a ser una urgencia vital."
    ],
    "No brindar atención según la ley de atención preferencial y de discapacidad": [
        "No se me brindó la atención preferencial que me corresponde por la ley.",
        "No me otorgaron la atención preferencial a pesar de tener derecho a ella.",
        "Mi atención fue demorada a pesar de mi condición de discapacidad.",
        "No recibí la atención preferencial según lo estipulado por la ley.",
        "La atención no fue acorde con la ley de atención preferencial y discapacidad.",
        "No respetaron mi prioridad en cola pese a presentar mi carné de discapacidad.",
        "El personal se negó a ayudarme con mi silla de ruedas en consultorios.",
        "No adaptaron el baño para mi familiar con movilidad reducida.",
        "Me hicieron esperar 4 horas en Emergencias, ignorando mi condición prioritaria.",
        "No hay intérpretes de lengua de señas para pacientes sordos."
    ],
    "Negar la afiliación del usuario": [
        "Se me negó la afiliación a mi seguro de salud sin motivo claro.",
        "A pesar de cumplir con todos los requisitos, mi afiliación fue rechazada.",
        "Mi solicitud para afiliarme al seguro fue denegada sin justificación.",
        "Me negaron la afiliación a pesar de tener todos los documentos en regla.",
        "No se me permitió afiliarme al seguro de salud.",
        "Rechazaron mi afiliación porque ‘mi empleador no ha depositado’ (pese a que sí lo hizo).",
        "No aceptaron mis documentos para afiliar a mi hijo recién nacido.",
        "Me exigen requisitos no establecidos en la ley para afiliarme.",
        "El sistema no registra mi afiliación, pese a tener constancia de aportes.",
        "No me permiten corregir un error en mi registro (ej: nombre mal escrito)."
    ],
    "Negar atención para el trámite de registro o acreditación": [
        "Me negaron la atención para el trámite de registro, a pesar de haber solicitado.",
        "No me brindaron la atención necesaria para completar mi registro o acreditación.",
        "Mi solicitud para iniciar el trámite de registro fue rechazada sin explicación.",
        "No se me permitió realizar el trámite de acreditación que necesitaba.",
        "Me fue negada la atención para completar mi trámite de registro.",
        "El área de afiliaciones nunca atiende, siempre cierran antes de hora.",
        "Perdí mi turno para actualizar mis datos porque el sistema se cayó.",
        "No me aceptaron el trámite de carné por falta de un sello en mi DNI.",
        "Me negaron la atención para registrar a mi cónyuge como beneficiario.",
        "No hay personal disponible para resolver problemas de acreditación en mi sede."
    ],
    "No cumplir con la disposición de libro de reclamaciones en salud": [
        "No se me permitió acceder al libro de reclamaciones para registrar mi queja.",
        "La disposición para presentar una reclamación no fue cumplida por la entidad.",
        "Me negaron el acceso al libro de reclamaciones en el centro de salud.",
        "El centro de salud no cumplió con la disposición de tener un libro de reclamaciones.",
        "No pude presentar mi queja por la negativa de acceso al libro de reclamaciones.",
        "En el Hospital Guillermo Almenara no tenían el libro de reclamaciones disponible.",
        "El personal se negó a recibir mi queja, diciendo que no sirve de nada.",
        "No me dieron copia de mi reclamo registrado, como exige la ley.",
        "El libro estaba en revisión por semanas, impidiendo quejas.",
        "Anotaron mal mis datos en el libro y no quisieron corregirlos."
    ],
    "No cumplir con las disposiciones de la PAUS de acuerdo a la normatividad vigente": [
        "La entidad no cumplió con las disposiciones de la PAUS que establece la ley.",
        "No se cumplió con la normatividad vigente de la PAUS en mi trámite.",
        "Me informaron que no se cumplió con las disposiciones de la PAUS según la ley.",
        "Mi trámite no se gestionó conforme a las disposiciones de la PAUS.",
        "Se violaron las disposiciones de la PAUS en mi caso.",
        "No respondieron mi reclamo en los 30 días establecidos por la PAUS.",
        "No me notificaron por escrito la resolución de mi trámite, como exige la norma.",
        "Me pidieron documentos adicionales no requeridos en la PAUS.",
        "Cambiaron los plazos de mi proceso sin justificación legal.",
        "No me dieron número de expediente para seguir mi reclamo."
    ]
}   

# Función para generar variaciones de un texto
def generar_variaciones(texto):
    variaciones = {
        "cobertura": ["atención", "servicio", "protección", "cobertura médica"],
        "demorada": ["retrasada", "tardada", "demorada en el tiempo", "demoró más de lo esperado"],
        "negar": ["rechazar", "denegar", "desestimar", "no otorgar"],
        "cobro": ["cargo", "facturación", "tarifa", "monto"],
        "tratamiento": ["procedimiento médico", "consulta", "servicio de salud", "atención médica"]
    }

    for palabra, opciones in variaciones.items():
        texto = re.sub(r"\b" + palabra + r"\b", random.choice(opciones), texto)

    # Incorporar datos sintéticos con Faker
    texto = texto.replace("mi tratamiento médico", fake.bs())
    texto = texto.replace("la aseguradora", fake.company())
    texto = texto.replace("mi solicitud", f"la solicitud de {fake.name()}")

    return texto

# Función para generar un texto sintético basado en la categoría
def generar_texto_por_clasificador(clasificador):
    if clasificador in templates:
        texto_base = random.choice(templates[clasificador])  # Selecciona un texto aleatorio
        return generar_variaciones(texto_base)  # Aplica variaciones
    else:
        return fake.sentence()  # Genera un texto aleatorio si la categoría no está en el diccionario

# Crear la nueva columna con los textos generados
df['DESCRIPCION'] = df['DE_CLASIF_1'].apply(generar_texto_por_clasificador)

# Guardar el nuevo DataFrame con las descripciones generadas
output_path = "../data/processed/reclamos_descripciones.csv"
df.to_csv(output_path, index=False)

print(f"Archivo guardado en {output_path}")
print(df[['DE_CLASIF_1', 'DESCRIPCION']].head())  # Muestra ejemplos del resultado